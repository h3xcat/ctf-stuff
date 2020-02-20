#!/usr/bin/env python3
import sys
import unidecode


if __name__ == "__main__":
    for line in sys.stdin:
        sys.stdout.write(unidecode.unidecode(line))
        sys.stdout.flush()
