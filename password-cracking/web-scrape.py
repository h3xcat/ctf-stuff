#!/usr/bin/env python3
import urllib.request
import sys
import re

re_word = re.compile(r"[A-Za-z]{1,}")
if __name__ == "__main__":
	if len(sys.argv) < 2:
		print(f"Usage: {sys.argv[0]} <url>")
	else:
		page = urllib.request.urlopen(sys.argv[1])
		
		matches = set([w.lower() for w in re_word.findall(page.read().decode())])
		for word in matches:
			sys.stdout.write(word)
			sys.stdout.write("\n")
			sys.stdout.flush()
