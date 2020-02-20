#!/usr/bin/env python3
import sys
import unidecode


if __name__ == "__main__":
    for line in sys.stdin:
        line = line.replace(' ', '')
        line = line.replace('\t', '')
        line = line.replace('\n', '')
        line = line.replace('\r', '')

        sys.stdout.write(unidecode.unidecode(line))
        sys.stdout.write('\n')
        sys.stdout.flush()
