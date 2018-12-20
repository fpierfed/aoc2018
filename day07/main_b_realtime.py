"""Solution to day 07 of Advent of Code 2018."""
import asyncio
import re
import sys
import time
from functools import total_ordering
from string import ascii_uppercase


PARSE_RE = re.compile(r'Step (?P<name>[A-Z]) must be finished before ' +
                      r'step (?P<child>[A-Z]) can begin.')
BASE_DELAY = 60
DELAYS = {l: BASE_DELAY + 1 + d
          for l, d in zip(ascii_uppercase, range(len(ascii_uppercase)))}


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

    async def execute(self, nworkers=1):
        """Return the list of the steps in the dag, in execution order."""
        async def _worker(inq, outq, tmpq):
            while True:
                node = await inq.get()
                print(f'Got {node.name} at {time.time()}')

                await tmpq.put(node)
                await asyncio.sleep(DELAYS[node.name])
                print(f'{node.name} done at {time.time()}')

                inq.task_done()
                await outq.put(node)
                await tmpq.get()
                tmpq.task_done()

        unprocessed = self._nodes[:]            # copy
        inq = asyncio.Queue()
        outq = asyncio.Queue()
        tmpqs = [asyncio.Queue() for _ in range(nworkers)]

        [asyncio.ensure_future(_worker(inq, outq, tmpqs[i]))
         for i in range(nworkers)]

        while unprocessed:
            ready = sorted([n for n in unprocessed if not n.parents])
            for node in ready:
                unprocessed.remove(node)
                await inq.put(node)

            while not outq.empty():
                node = await outq.get()
                for child in node.children:
                    child.parents.remove(node)
                    child.retired_parents.append(node)
                outq.task_done()

            await asyncio.sleep(0)

        while any([not q.empty() for q in tmpqs]):
            await asyncio.sleep(0)
        return


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

    loop = asyncio.get_event_loop()
    loop.run_until_complete(dag.execute(5))
