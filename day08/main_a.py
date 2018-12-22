"""Solution to day 08 of Advent of Code 2018."""
from __future__ import annotations

import sys
from dataclasses import dataclass


@dataclass(repr=False)
class Node:
    """Tree Node."""

    instances = 0

    children: list(Node)                                                # noqa
    metas: list(int)

    def __post_init__(self):
        """Set instance name."""
        self.name = Node.instances
        Node.instances += 1

    def __str__(self):
        """Return the node name."""
        return str(self.name)

    __repr__ = __str__


def parse(data):
    """Parse the flatten tree data structure."""
    # The tree is flattened:
    #   <num children> <num metadata entries> [child1]... [metadata1]...
    numbers = [int(x) for x in data.split()]
    return _parse(numbers)


def _parse(xs):
    return _parse_node(xs)


def _parse_node(xs):
    # breakpoint()
    nchildren = xs.pop(0)
    nmeta = xs.pop(0)
    # print(f'Node with {nchildren} children and {nmeta} metas')
    if nchildren:
        children = _parse_children(xs, n=nchildren)
    else:
        children = []
    metas = [xs.pop(0) for _ in range(nmeta)]
    node = Node(children, metas)
    # print(f'{node} children = {node.children} metas = {node.metas}')
    return node


def _parse_children(xs, n):
    return [_parse_node(xs) for _ in range(n)]


def sum_metadata(root, tot=0):
    """Sum up all metadata nodes."""
    # print(root, tot)

    tot += sum(root.metas)
    # print(root.metas)
    for node in root.children:
        tot = sum_metadata(node, tot)
    # print(root, tot)
    return tot


if __name__ == '__main__':
    try:
        fname = sys.argv[1]
    except IndexError:
        print(f'usage: {sys.argv[0]} <input file>', file=sys.stderr)
        sys.exit(1)

    with open(fname) as f:
        data = f.readlines()

    assert len(data) == 1
    data = data.pop().strip()

    print(sum_metadata(parse(data)))
