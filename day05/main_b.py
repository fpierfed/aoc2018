"""Solution to day 05 of Advent of Code 2018."""
import sys


def process(start, data):
    """Recursively remove all pairs of letters differing in capitalizaton."""
    while True:
        new_start, new_data = _process(start, data)
        if not new_data or new_data == data:
            break
        else:
            start = new_start
            data = new_data
    return new_data


def _process(start, data):
    i = start
    while data and i < len(data) - 1:
        first = data[i]
        second = data[i + 1]

        if first != second and first.lower() == second.lower():
            new_data = data[:i] + data[i + 2:]
            return (max(0, i - 1), new_data)
        else:
            i += 1
    return (start, data)


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

    lengths = []
    lengths.append(len(process(0, data)))

    letters = set(data.lower())
    for letter in letters:
        test = data.replace(letter, '')
        test = test.replace(letter.upper(), '')
        lengths.append(len(process(0, test)))
    print(min(lengths))
