#!/usr/bin/env python3
import re
import sys


PARSE_PTRN = re.compile(r'#(?P<_id>\d+) @ (?P<x>\d+),(?P<y>\d+): ' +
                        r'(?P<dx>\d+)x(?P<dy>\d+)')
WIDTH = 1001
HEIGHT = 1001


def parse(fname='input.txt', pattern=PARSE_PTRN):
    """Parse the input file into a sequence of pixel sets."""
    with open(fname) as f:
        data = f.readlines()

    raw_areas = []
    for lineno, line in enumerate(data):
        line = line.strip()
        if not line:
            break

        match = pattern.match(line)
        if not match:
            print(f'WARNING: line {lineno + 1} "{line}" - malformed spec',
                  file=sys.stderr)
            continue

        kwargs = {k: int(match.group(k))
                  for k in ('_id', 'x', 'y', 'dx', 'dy')}
        raw_areas.append(compute_area_pixels(**kwargs))

    areas = [(_id, set(s)) for _id, s in sorted(raw_areas, key=lambda a: a[1])]
    return areas


def compute_area_pixels(_id, x, y, dx, dy, w=WIDTH):
    """Given a set specification, return (id, {pixels})."""
    pixels = [w * _y + _x
              for _y in range(y, y + dy)
              for _x in range(x, x + dx)]
    return (_id, pixels)


def find_non_overlapping_area(areas):
    nareas = len(areas)
    ids = set([_id for _id, _ in areas])
    overlapping = []

    for i in range(nareas - 1):
        for j in range(i + 1, nareas):
            if set.intersection(areas[i][1], areas[j][1]):
                overlapping.append(areas[i][0])
                overlapping.append(areas[j][0])
    return ids - set(overlapping)


if __name__ == '__main__':
    try:
        fname = sys.argv[1]
    except IndexError:
        print(f'usage: {sys.argv[0]} <input file>', file=sys.stderr)
        sys.exit(1)

    print(find_non_overlapping_area(parse(fname)))
