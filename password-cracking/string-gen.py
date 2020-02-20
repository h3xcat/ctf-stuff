#!/usr/bin/env python3

import math
import re
import pprint
import itertools
import sys
from enum import Enum

re_curly = re.compile(r"^\s*(\d*)\s*(,?)\s*(\d*)\s*$")

##################################################################
##################################################################

class Node():
	def __repr__(self):
		return (f'{self.__class__.__name__}')

class NodeRepeat(Node):
	def __init__(self, min, max, node=None):
		self.min = min
		self.max = max
		self.node = node

	def set_node(self, node):
		self.node = node

	def __iter__(self):	
		for i in range(self.min,self.max+1):
			for v in itertools.product(self.node,repeat=i):
				yield v

	def __repr__(self):
		return (f'{self.__class__.__name__}( {self.min}, {self.max}, {self.node} )')

class NodeSpecialDigit(Node):
	def __iter__(self):	
		for i in range(0,10):
			yield str(i)

class NodeCSet(Node):
	def __init__(self, s=None):
		if not s:
			s = []
		self.s = set(s)
	
	def __repr__(self):
		return (f'{self.__class__.__name__}( {self.s} )')

	def __iter__(self):
		for c in self.s:
			yield c

	pass

class NodeCSetRange(Node):
	def __init__(self, prev=None, next=None):
		self.prev = prev
		self.next = next
		pass
	def __iter__(self):
		for i in range(ord(self.prev.val()),ord(self.next.val())+1):
			print(chr(i))
			yield chr(i)

	def set_next(self, next):
		self.next = next
		
	def set_prev(self, prev):
		self.prev = prev
		
	def __repr__(self):
		return (f'{self.__class__.__name__}( \'{self.prev.val()}\', \'{self.next.val()}\' )')

class NodeGroup(Node):
	def __init__(self, l=None):
		if not l:
			l = []
		self.l = l
	
	def add(self, v):
		self.l.append(v)

	def pop(self):
		return self.l.pop()

	def __iter__(self):
		for p in itertools.product(*self.l):
			yield p


	def __repr__(self):
		return (f'{self.__class__.__name__}( {self.l} )')
	pass
class NodeWordlist(Node):
	def __init__(self, wordlist, stdin_wordlist):
		self.wordlist = wordlist
		self.stdin_wordlist = stdin_wordlist
	
	def __iter__(self):
		if self.wordlist == "-":
			for w in self.stdin_wordlist:
				yield w
		else:
			with open(self.wordlist, "r") as wf:
				for w in wf:
					yield w.strip()

##################################################################
##################################################################

class InvalidPattern(Exception): pass

##################################################################
##################################################################

class Token():
	def __repr__(self):
		return (f'{self.__class__.__name__}()')

class TokenLiteral(Token):
	def __init__(self, c):
		self.c = c
	def val(self):
		return self.c
	def __iter__(self):
		yield self.c

class TokenCSetBegin(Token): pass
class TokenCSetEnd(Token): pass
class TokenCSetRange(Token): pass
class TokenGroupBegin(Token): pass
class TokenGroupEnd(Token): pass
class TokenSpecialDigit(Token): pass
class TokenWordlist(Token):
	def __init__(self, index):
		self.index = int(index)
class TokenRepeat(Token):
	def __init__(self, min, max):
		self.min = min
		self.max = max

##################################################################
##################################################################
def unpack_tuples(tup):
	ret = []
	for v in tup:
		if isinstance(v,tuple):
			ret += unpack_tuples(v)
		else:
			ret.append(v)

	return ret
	
class StringGenerator():
	def __init__(self, pattern, wordlist=None):
		self.pattern = pattern
		
		if wordlist is None:
			self.wordlist = []
		elif isinstance(wordlist, str):
			self.wordlist = [wordlist]
		else:
			self.wordlist = wordlist

		self.stdin_wordlist = []
		if "-" in self.wordlist:
			for line in sys.stdin:
				self.stdin_wordlist.append(line.strip())

		t_cset = False

		t_repeat = False
		t_repeat_str = []
		
		t_escape = False
		tokens = self._get_tokens(pattern)
		root_node = self._get_nodes(tokens)

		self.root = root_node
	
	def _get_tokens(self, pattern):

		ipattern = iter(pattern)

		tokens = []
		escaped = False

		nest_stack = []
		for c in ipattern:
			if c == "\\":
				c = next(ipattern)

				if c=='d':
					tokens.append(TokenSpecialDigit())
				elif c.isdigit():
					tokens.append(TokenWordlist(c))
				elif c=='n':
					tokens.append(TokenLiteral('\n'))
				elif c=='r':
					tokens.append(TokenLiteral('\r'))
				elif c=='t':
					tokens.append(TokenLiteral('\t'))
				elif c=='s':
					tokens.append(TokenLiteral(' '))
				else:
					tokens.append(TokenLiteral(c))
			
			elif c == '(':
				if len(nest_stack) > 0 and nest_stack[-1] == '[':
					raise InvalidPattern("No grouping inside character sets")
				
				nest_stack.append('(')
				tokens.append(TokenGroupBegin())

			elif c == ')':
				if nest_stack[-1] != '(':
					raise InvalidPattern("Unexpected ')'")
				nest_stack.pop()

				tokens.append(TokenGroupEnd())

			elif c == '[':
				if len(nest_stack) > 0 and nest_stack[-1] == '[':
					raise InvalidPattern("Unexpected '['")

				nest_stack.append('[')
				tokens.append(TokenCSetBegin())

			elif c == ']':
				if nest_stack[-1] != '[':
					raise InvalidPattern("Unexpected ']'")
				
				nest_stack.pop()
				tokens.append(TokenCSetEnd())

			elif c == '-' and len(nest_stack) > 0 and nest_stack[-1] == '[':
				tokens.append(TokenCSetRange())
			elif c == '{':

				repeat_str = []
				cr = next(ipattern)
				while cr != '}':
					repeat_str.append(cr)
					cr = next(ipattern)
					

				repeat_str = ''.join(repeat_str)
				matches = re_curly.match(repeat_str)
				if not matches:
					raise InvalidPattern("Invalid repeat parameter '{}'!".format(repeat_str))


				repeat_min = matches.group(1) and int(matches.group(1)) or 0
				repeat_max = repeat_min
				if matches.group(2):
					repeat_max = matches.group(3) and int(matches.group(3)) or 20

				tokens.append( TokenRepeat(repeat_min, repeat_max) )
				
			elif c == '}':
				raise InvalidPattern("Unexpected '}'")

			else:
				tokens.append(TokenLiteral(c))	
		if len(nest_stack) > 0:
			raise InvalidPattern("Incomplete nesting")
		
		return tokens

	def _get_nodes(self, tokens):

		root_group = NodeGroup()
		groups = [root_group]

		itokens = iter(tokens)
		for token in itokens:
			
			if isinstance( token, TokenGroupBegin):
				new_group = NodeGroup()
				groups[-1].add(new_group)
				groups.append(new_group)

			elif isinstance( token, TokenGroupEnd):
				groups.pop()
			
			elif isinstance( token, TokenCSetBegin):

				cset = []

				token = next(itokens)
				while not isinstance(token,TokenCSetEnd):
					if isinstance(token,TokenLiteral):
						cset.append(token)
					elif isinstance(token, TokenCSetRange):
						if len(cset) == 0:
							raise InvalidPattern("Invalid range")

						prev_token = cset.pop()
						next_token = next(itokens)
						if not isinstance(prev_token, TokenLiteral) or not isinstance(next_token, TokenLiteral):
							raise InvalidPattern("Invalid range")


						for i in range(ord(prev_token.val()),ord(next_token.val())+1):
							cset.append(TokenLiteral(chr(i)))
					elif isinstance(token, TokenSpecialDigit):
						for i in range(0,10):
							cset.append(TokenLiteral(str(i)))
					else:
						raise InvalidPattern(f"Invalid token inside cset {token}")

					token = next(itokens)

				groups[-1].add(NodeCSet([t.val() for t in cset]))

			elif isinstance( token, TokenRepeat):
				rep_node = groups[-1].pop()
				groups[-1].add(NodeRepeat(token.min, token.max, rep_node))
			elif isinstance( token, TokenWordlist):
				groups[-1].add(NodeWordlist(self.wordlist[token.index], self.stdin_wordlist))
			elif isinstance( token, TokenSpecialDigit):
				groups[-1].add(NodeSpecialDigit())
			else:
				groups[-1].add(token)
		return root_group

	def fetchall(self):
		return list(self)

	def __iter__(self):
		for val in self.root:
			yield ''.join( unpack_tuples(val) )


##################################################################
##################################################################

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print(f"Usage: {sys.argv[0]} <pattern> [<wordlist> ...]")
	else:
		gen = StringGenerator(sys.argv[1],sys.argv[2:])
		c = 0
		for v in gen:
			sys.stdout.write(v)
			sys.stdout.write("\n")
			sys.stdout.flush()
