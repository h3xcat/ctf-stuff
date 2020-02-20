#!/usr/bin/env python3
import sys

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        sys.stderr.write("{} <length>\n".format(sys.argv[0]))
        sys.exit(1)

    limit = int(sys.argv[1])

    for line in sys.stdin.buffer:
        line = line.strip()

        lineLen = len(line)
        if lineLen > limit:
            continue

        sys.stdout.buffer.write(line)
        sys.stdout.buffer.write(b"\n")
        sys.stdout.flush()