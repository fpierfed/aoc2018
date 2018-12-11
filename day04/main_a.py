"""Solution to day 04 of Advent of Code 2018."""
import datetime
import re
import sys
from collections import Counter, defaultdict


PARSE_RE = re.compile(r'\[(?P<year>\d+)-(?P<month>\d+)-(?P<day>\d+) ' +
                      r'(?P<hour>\d+):(?P<minutes>\d+)\] ' +
                      r'(?P<msg>.+)')
GUARD_RE = re.compile(r'Guard #(?P<gid>\d+) begins shift')


try:
    fname = sys.argv[1]
except IndexError:
    print(f'usage: {sys.argv[0]} <input file>', file=sys.stderr)
    sys.exit(1)

with open(fname) as f:
    data = f.readlines()

journal = []
for lineno, line in enumerate(data):
    line = line.strip()
    m = PARSE_RE.match(line)
    if not m:
        print(f'Warning line {lineno + 1} malformed ("{line}")',
              file=sys.stderr)
        continue

    journal.append((datetime.datetime(*(int(x) for x in m.groups()[:-1])),
                    m.group('msg')))

journal.sort(key=lambda e: e[0])

start = None
guards = defaultdict(Counter)
for t, msg in journal:
    m = GUARD_RE.match(msg)
    if m:
        # New guard begins shift.
        gid = m.group('gid')
    elif msg == 'falls asleep':
        # Start counting
        start = t
    elif msg == 'wakes up':
        slept = range(start.minute, t.minute)
        guards[gid].update(slept)

# Find the one who sleeps the most
gid, n = sorted([(gid, len(list(c.elements()))) for gid, c in guards.items()],
                key=lambda e: e[1])[-1]
minute = guards[gid].most_common(1)[0][0]
print(int(gid) * minute)
