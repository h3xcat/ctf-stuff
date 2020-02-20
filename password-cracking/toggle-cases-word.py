#!/usr/bin/env python3
import sys
from string import ascii_letters
import itertools



if __name__ == "__main__":
    for line in sys.stdin:
        line = line.strip()

        
        combinations = []
        for word in line.split(' '):
            if not word:
                continue
            combinations.append([word[0].lower(),word[0].upper()])
            combinations.append([word[1:]])

        for w in itertools.product(*combinations):
            sys.stdout.write(' '.join(w))
            sys.stdout.write('\n')

        sys.stdout.flush()
