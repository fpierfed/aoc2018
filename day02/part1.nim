import os
import sugar
import strutils
import tables


if paramCount() < 1:
    echo "usage: ", paramStr(0), " input_file"
    quit(1)

var npairs: int = 0
var ntriplets: int = 0
var seen_two = false
var seen_three = false

let input = open(paramStr(1))
for line in input.lines:
    var chars = lc[x | (x <- line), char]
    var counts = chars.toCountTable

    seen_two = false
    seen_three = false
    for c, n in counts:
        if n == 2 and not seen_two:
            npairs += 1
            seen_two = true
        elif n == 3 and not seen_three:
            ntriplets += 1
            seen_three = true
        if seen_two and seen_three:
            break
input.close()

echo "Result: ", npairs * ntriplets
