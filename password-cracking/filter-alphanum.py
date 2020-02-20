#!/usr/bin/env python3
import sys
import string

if __name__ == "__main__":
    filterSet = set([ord(c) for c in (string.ascii_letters + string.digits)])

    #line = readline()
    for line in sys.stdin.buffer:

        line = line.strip()

        if all( c in filterSet for c in line):
            sys.stdout.buffer.write(line)
            sys.stdout.buffer.write(b"\n")
            sys.stdout.flush()
