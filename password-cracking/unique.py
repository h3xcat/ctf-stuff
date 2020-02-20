#!/usr/bin/env python3
import sys
from string import ascii_letters
import itertools

words = set()

if __name__ == "__main__":
    for line in sys.stdin:
  
        if not line in words:
            words.add(line)
            sys.stdout.write(line)
            sys.stdout.flush()