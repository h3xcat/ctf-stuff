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

def includeLeetSpeak(charSet):
    # TODO: make this more beautiful 
    charSet[ord("a")] |= set([ord("@"),ord("4")])
    charSet[ord("A")] |= set([ord("@"),ord("4")])
    
    charSet[ord("e")] |= set([ord("3")])
    charSet[ord("E")] |= set([ord("3")])
    
    charSet[ord("s")] |= set([ord("$"),ord("5")])
    charSet[ord("S")] |= set([ord("$"),ord("5")])
    
    charSet[ord("l")] |= set([ord("1")])
    charSet[ord("L")] |= set([ord("1")])
    
    charSet[ord("i")] |= set([ord("!"),ord("1")])
    charSet[ord("I")] |= set([ord("!"),ord("1")])



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

    #includeInvertedCases(charSet)

    includeLeetSpeak(charSet)
    for line in sys.stdin.buffer:

        findCombinations(line, charSet)
