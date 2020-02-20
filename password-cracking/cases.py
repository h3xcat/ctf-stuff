#!/usr/bin/env python3
import sys
from string import ascii_letters
import itertools

def includeDefault(charSet):
    for i in range(0,256):
        charSet[i] = set([i])

def includeInvertedCases(charSet):
    for c in ascii_letters:
        charSet[ord(c)] |= set([ord(c.lower()) if c.isupper() else ord(c.upper())])


def findCombinations(word, charSet):

    wordCombinations = []
    # Transform string to list of set of characters
    for i, c in enumerate(word):
        wordCombinations += [charSet[c]]
    
    for newWord in itertools.product(*wordCombinations):
        sys.stdout.buffer.write(bytearray(newWord))
    sys.stdout.flush()



if __name__ == "__main__":
    charSet = dict()
    includeDefault(charSet)
    includeInvertedCases(charSet)
    
    for line in sys.stdin.buffer:
        findCombinations(line, charSet)