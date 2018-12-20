"""Solution to day 07 of Advent of Code 2018."""
import re
import sys
from collections import defaultdict
from functools import total_ordering
from queue import Empty, Queue
from string import ascii_uppercase


PARSE_RE = re.compile(r'Step (?P<name>[A-Z]) must be finished before ' +
                      r'step (?P<child>[A-Z]) can begin.')
NWORKERS = 5
BASE_DELAY = 60
DELAYS = {l: BASE_DELAY + 1 + d
          for l, d in zip(ascii_uppercase, range(len(ascii_uppercase)))}
LOOP = None
CLOCK = 0


class Loop:
    """Coroutine scheduler."""

    def __init__(self):
        """Create tasks, schedules etc."""
        self.tasks = []
        self.ready_at = defaultdict(list)
        self.stop = False

    def schedule(self, task, at=0):
        """Schedule the given Task at the given time."""
        if at is None or at < CLOCK:
            # Schedule immediately
            at = CLOCK

        if task not in self.ready_at[at]:
            self.ready_at[at].append(task)
        if task not in self.tasks:
            self.tasks.append(task)
        print(f'Scheduled Task {task.id} at {at}')

    def create_task(self, coroutine):
        """Wrap the coroutine into a Task and schedule it ASAP."""
        task = Task(coroutine)
        self.schedule(task, at=CLOCK)
        return task

    def remove(self, task):
        """Mark task as complete and remove it from self.tasks."""
        if task in self.tasks:
            self.tasks.remove(task)

    def run_until_complete(self, coroutine):
        """Run until the coroutine is done."""
        task = self.create_task(coroutine)
        task.add_done_callback(self._stop_callback)
        self.run_forever()
        task.remove_done_callback(self._stop_callback)
        return task

    def execute(self, dag, inq, outq):
        """Run until the dag is done."""
        global CLOCK

        unprocessed = dag._nodes[:]            # copy
        while unprocessed or [tsk
                              for t in self.ready_at
                              for tsk in self.ready_at[t] if t > CLOCK]:
            print(f'The time is {CLOCK}')

            # First check if any new DAG node is available for execution.
            # print('Checking DAG nodes')

            added = False
            ready_nodes = sorted([n for n in unprocessed if not n.parents])
            for node in ready_nodes:
                unprocessed.remove(node)
                inq.put(node)
                added = True

            # if not added:
            #     print('No DAG node is ready')

            # Now see if any worker is available to pick up any work.
            # print('Checking ready tasks')
            ready = [(t, tsk)
                     for t in self.ready_at
                     for tsk in self.ready_at[t]
                     if t <= CLOCK]
            # print(ready, self.ready_at)
            if not ready:
                # print('No task is ready')
                CLOCK += 1
                continue

            for t, task in sorted(ready, key=lambda e: e[0]):
                run_after = 0
                try:
                    run_after = next(task.coroutine)
                except StopIteration:
                    for callback in task.callbacks:
                        callback(task)
                    self.remove(task)
                else:
                    next_run = CLOCK + run_after
                    self.schedule(task, at=next_run)
                finally:
                    if run_after > 0:
                        self.ready_at[t].remove(task)
                    for t in self.ready_at:
                        if t < CLOCK:
                            self.ready_at[t] = []

            # And finally see if any worker is done
            # print('Checking outq')
            added = False
            while not outq.empty():
                node = outq.get()
                # print(f'Adding {", ".join([n.name for n in node.children])}')
                for child in node.children:
                    child.parents.remove(node)
                    child.retired_parents.append(node)
                added = True
                outq.task_done()
            if not added:
                CLOCK += 1
        print(f'The time is {CLOCK}')

    def _stop_callback(self, task):
        """Stop the loop."""
        self.stop = True


class Task:
    """Coroutine wrapper."""

    num_instances = 0

    def __init__(self, coroutine):
        """Wrap the coroutine into a Task."""
        self.coroutine = coroutine
        self.id = Task.num_instances
        Task.num_instances += 1

        self.callbacks = []

    def __str__(self):
        """Print the ID."""
        return str(self.id)

    __repr__ = __str__

    def add_done_callback(self, callback):
        """Add callback to the Task callbacks."""
        self.callbacks.append(callback)

    def remove_done_callback(self, callback):
        """Remove callback from the Task callbacks."""
        if callback in self.callbacks:
            self.callbacks.remove(callback)


def ensure_future(coroutine, loop=None):
    """Wrap input into a Task."""
    if loop is None:
        loop = get_event_loop()
    if not isinstance(coroutine, Task):
        return loop.create_task(coroutine)
    return coroutine


def sleep(t):
    """Reschedule the caller after t seconds."""
    # print(f'Sleeping for {t} seconds')
    yield t


def get_event_loop():
    """Return the event loop for the current thread."""
    global LOOP
    if LOOP is None:
        LOOP = Loop()
    return LOOP


def _worker(inq, outq, tmpq):
    while True:
        try:
            node = inq.get(block=False)
        except Empty:
            # print(f'Noting to do: going back to sleep')
            yield from sleep(0)
            continue
        else:
            print(f'Got {node.name} at {CLOCK}')

        tmpq.put(node)
        yield from sleep(DELAYS[node.name])
        print(f'{node.name} done at {CLOCK}')

        inq.task_done()
        outq.put(node)
        tmpq.get()
        tmpq.task_done()


class Dag:
    """Directed Acyclic Graph."""

    def __init__(self, root):
        """Create a DAG by specifying its root Node."""
        self.root = root
        self._nodes = []

    @classmethod
    def from_nodes(cls, nodes):
        """Create a DAG instance from a list of Nodes."""
        node_names = list(nodes.keys())

        root = nodes[node_names[0]]
        for node in nodes.values():
            if root in node.children:
                root = node
        obj = cls(root)
        obj._nodes = list(nodes.values())
        return obj


@total_ordering
class Node:
    """A Node in a DAG."""

    def __init__(self, name, children=None, parents=None):
        """Create a Node with its children, if any and parents if known."""
        self.name = name
        if children is None:
            children = []
        self.children = children
        if parents is None:
            parents = []
        self.parents = parents
        self.retired_parents = []

    def __str__(self):
        """Just print the node name."""
        return self.name

    def __repr__(self):
        """Just print the node name."""
        return self.__str__()

    def __eq__(self, other):
        """Implement total ordering based on name."""
        return self.name == other.name

    def __lt__(self, other):
        """Implement total ordering based on name."""
        return self.name < other.name


def parse(data, ptn=PARSE_RE):
    """Return the DAG described textually in the data."""
    nodes = {}
    for lineno, line in enumerate(data):
        line = line.strip()
        if not line:
            continue

        m = ptn.match(line)
        if not m:
            print(f'Cannot parse line {lineno + 1}: "{line}"!')
            continue

        node_name = m.group('name')
        child_name = m.group('child')
        # print(f'{node_name} -> {child_name}')

        if node_name not in nodes:
            nodes[node_name] = Node(node_name)
        if child_name not in nodes:
            nodes[child_name] = Node(child_name)

        nodes[node_name].children.append(nodes[child_name])
        nodes[child_name].parents.append(nodes[node_name])
    return Dag.from_nodes(nodes)


if __name__ == '__main__':
    try:
        fname = sys.argv[1]
    except IndexError:
        print(f'usage: {sys.argv[0]} <input file>', file=sys.stderr)
        sys.exit(1)

    with open(fname) as f:
        data = f.readlines()

    dag = parse(data)

    loop = get_event_loop()

    inq = Queue()
    outq = Queue()
    tmpqs = [Queue() for _ in range(NWORKERS)]

    [ensure_future(_worker(inq, outq, tmpqs[i]))
        for i in range(NWORKERS)]

    loop.execute(dag, inq, outq)
