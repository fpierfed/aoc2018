"""Solution to day 07 of Advent of Code 2018."""
import re
import sys
# from collections import deque
# from queue import PriorityQueue
from functools import total_ordering


PARSE_RE = re.compile(r'Step (?P<name>[A-Z]) must be finished before ' +
                      r'step (?P<child>[A-Z]) can begin.')
CACHE = {}


def cached(fn):
    """Memoization."""
    def wrapper(sleeping, available, done):
        key = ''.join(sorted(done))
        if key not in CACHE:
            CACHE[key] = fn(sleeping, available, done)
        return CACHE[key]
    return wrapper


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

    def execute(self):
        """Return the list of the steps in the dag, in execution order."""
        unprocessed = self._nodes[:]            # copy
        while unprocessed:
            ready = sorted([n for n in unprocessed if not n.parents])
            if not ready:
                raise Exception('Ready queue is empty!')

            node = ready.pop(0)
            unprocessed.remove(node)
            yield node

            for child in node.children:
                child.parents.remove(node)
                child.retired_parents.append(node)


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


def execute(dag):
    """Return the list of the steps in the dag, in execution order."""
    return ''.join(str(n) for n in dag.execute())


if __name__ == '__main__':
    try:
        fname = sys.argv[1]
    except IndexError:
        print(f'usage: {sys.argv[0]} <input file>', file=sys.stderr)
        sys.exit(1)

    with open(fname) as f:
        data = f.readlines()

    print(execute(parse(data)))
