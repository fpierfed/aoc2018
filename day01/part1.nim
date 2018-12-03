import os
import strutils


if paramCount() < 1:
    echo "usage: ", paramStr(0), " input_file"
    quit(1)

let input = open(paramStr(1))
var freq = 0
var delta = 0

for line in input.lines:
    delta = parseInt($line)
    freq += delta
input.close()

echo "Result: ", freq
