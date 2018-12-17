"""Solution to day 05 of Advent of Code 2018."""
# import random
import sys
from collections import defaultdict

# from PIL import Image


def distance(p1, p2):
    """Manhattan distance between points p1 and p2."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def compute_areas(points):
    """Compute Voronoi-like finite areas for the given coordinates."""
    # All Points to the outside have infinite areas. They can be ignored.
    xs = [c[0] for c in points]
    ys = [c[1] for c in points]
    maxx = max(xs)
    maxy = max(ys)

    # img = Image.new("RGB", (maxx + 2, maxy + 2))

    # colors = [(random.randrange(255),
    #            random.randrange(255),
    #            random.randrange(255)) for _ in points]
    # white = (255, 255, 255)
    # black = (0, 0, 0)

    areas = defaultdict(set)
    not_useful = []
    # While at it, remove all points whose areas are unbound. This means points
    # whose areas touch the boundaries of the diagram.
    for y in range(0, maxy + 2):
        for x in range(0, maxx + 2):
            ds = [(i, distance((x, y), p)) for i, p in enumerate(points)]
            ds.sort(key=lambda index_dist: index_dist[1])
            if ds[0][1] == ds[1][1]:
                # At least two points can clame (x, y). Discarded.
                # print('.', end='')
                # img.putpixel((x, y), white)
                continue

            index = ds[0][0]
            # print(index, end='')
            # img.putpixel((x, y), colors[index])

            chosen = points[index]
            areas[chosen].add((x, y))

            if chosen not in not_useful and \
               (x in (0, maxx + 1) or y in (0, maxy + 1)):
                not_useful.append(chosen)
        # print()

    # for point in points:
    #     img.putpixel(point, black)

    # img.save('test.png', 'PNG')

    useful = set(points) - set(not_useful)
    return [len(areas[p]) for p in useful]


def largest_area(coords):
    """Compute the size of the largest non-infinite area."""
    areas = compute_areas(coords)
    return sorted(areas)[-1]


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

    print(largest_area(coords))
