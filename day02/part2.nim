import algorithm
import os
import strutils
import sugar


if paramCount() < 1:
    echo "usage: ", paramStr(0), " input_file"
    quit(1)

let input = open(paramStr(1))
var lines: seq[string] = lc[s | (s <- input.lines), string]
input.close()

sort(lines, system.cmp)
var i: int = 0
while i < lines.len - 1:
    if editDistance(lines[i], lines[i+1]) <= 1:
        var j:int = 0
        var res:string = ""
        while j < lines[i].len:
            # This assumes that all strings have the same length!!!!!!!!!!
            if lines[i][j] == lines[i + 1][j]:
                res.add(lines[i][j])
            j += 1
        echo res
        quit(0)
    i += 2
