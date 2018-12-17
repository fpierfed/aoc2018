"""Solution to day 05 of Advent of Code 2018."""
# import random
import sys


def distance(p1, p2):
    """Manhattan distance between points p1 and p2."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def safe_area(points, maxd):
    """Compute the size area of pixels within maxd of all points."""
    # All Points to the outside have infinite areas. They can be ignored.
    xs = [c[0] for c in points]
    ys = [c[1] for c in points]
    maxx = max(xs)
    maxy = max(ys)

    area = set()
    for y in range(0, maxy + 2):
        for x in range(0, maxx + 2):
            ds = [distance((x, y), p) for p in points]
            if sum(ds) >= maxd:
                continue

            area.add((x, y))
    return len(area)


if __name__ == '__main__':
    try:
        fname = sys.argv[1]
    except IndexError:
        print(f'usage: {sys.argv[0]} <input file>', file=sys.stderr)
        sys.exit(1)

    with open(fname) as f:
        data = f.readlines()

    coords = []
    for line in data:
        line = line.strip()
        if not line:
            continue

        x, y = line.split(',')
        coords.append((int(x.strip()), int(y.strip())))

    print(safe_area(coords, maxd=10000))
