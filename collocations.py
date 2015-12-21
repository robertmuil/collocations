import pandas as pd

dbg_lvl = 3
def dbg(lvl,msg):
	if lvl <= dbg_lvl:
		print 'D{:d}|{}'.format(lvl,msg)

replacements = {
			'.': '<End>'
			}

def count_collocations(text, order=1):
	pairs = {}

	dbg(3, 'text: {}'.format(text))
	words = text.lower().split()
	
	words = [replacements.get(w, w) for w in words]
	dbg(2, '{:d} words'.format(len(words)))
	
	dbg(3, '|'.join(words[:-1]))

	for w1,w2 in zip(['<Start>']+words,words+['<End>']):
		dbg(3, 'pair: {},	{}'.format(w1,w2))
		p1 = pairs.get(w1, {})
		p2 = p1.get(w2, 0)
		p1[w2] = p2 + 1
		pairs[w1]=p1

	return pairs

if __name__ == '__main__':
	import sys

	text = "This is just an example. Really just an example."

	if len(sys.argv) > 1:
		fpath = sys.argv[1]
		with open(fpath, 'r') as f:
			text = f.read()
	
	pairs = count_collocations(text)

	print pairs
