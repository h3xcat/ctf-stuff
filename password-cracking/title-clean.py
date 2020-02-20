#!/usr/bin/env python3
import sys
import re
import unidecode

re_parenthesis = re.compile(r'\([^\)]*\)|\[[^\]]*\]')
re_specialchars = re.compile(r'[^A-Za-z0-1\s]+')
re_spaces = re.compile(r'\s+')

def process_title(words, title):
    # Remove text in parenthesis
    title = re_parenthesis.sub('',title)

    # Remove apastrophes
    title = title.replace('&', 'and')

    # Remove apastrophes
    title = title.replace('\'', '')

    # Replace dashes with spaces
    title = title.replace('-', ' ')

    # Ignore content after collon
    title = title.split(':', 1)[0]

    # Process titles without THE
    if title[0:4].lower() == 'the ':
        process_title(words, title[4:])

    # Split comma into seperate processing, with and without contents after comma
    if title.count(',') > 0:
        process_title(words, title.replace(',', ' '))
        title = title.split(',',1)[0]

    # Remove special chars
    title = re_specialchars.sub('', title)
    
    # Remove extra spaces
    title = re_spaces.sub(' ', title)

    # Strip spaces from endings
    title = title.strip()


    words.add(title)

if __name__ == "__main__":
    for line in sys.stdin:
        line = unidecode.unidecode(line)

        words = set()

        process_title(words, line)

        for w in words:
            sys.stdout.write(w)
            sys.stdout.write('\n')

        sys.stdout.flush()
