import intsets
import os
import strutils


if paramCount() < 1:
    echo "usage: ", paramStr(0), " input_file"
    quit(1)

let input = open(paramStr(1))
var deltas: seq[int] = @[]

for line in input.lines:
    deltas.add(parseInt($line))
input.close()

var freq:int = 0
var freqs = initIntSet()
freqs.incl(freq)

while true:
    for delta in deltas:
        freq += delta
        if freqs.contains(freq):
            echo "Repeting freq: ", freq
            quit(0)
        else:
            incl(freqs, freq)
