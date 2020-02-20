#!/usr/bin/env python3
import sys

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        sys.stderr.write("{} [<keywords> ...]\n".format(sys.argv[0]))
        sys.exit(1)

    keywords = []
    for file in sys.argv[1:]:
        with open(file) as f:
            for line in f.buffer:
                keywords += [line.strip().lower()]
    

    for line in sys.stdin.buffer:
        line = line.strip()

        if any(k in line for k in keywords):
            sys.stdout.buffer.write(line)
            sys.stdout.buffer.write(b"\n")
            sys.stdout.flush()
