import pandas as pd
import networkx as nx
import matplotlib.pyplot as pp
import seaborn

dbg_lvl = 2
def dbg(lvl,msg):
	if lvl <= dbg_lvl:
		print 'D{:d}|{}'.format(lvl,msg)

punctuation = {
			'.': ' <S>',
			'?': ' <S>',
			',': ' ',
			';': ' ',
			"'": ' ',
			'"': ' ',
			'-': ' ',
			}

replacements = punctuation.copy()

def _count_collocations(text, order=1,
		pairs=None):

	if pairs is None:
		pairs = {}

	dbg(3, 'text: {}'.format(text))
	_text = text.lower()
	for k,v in punctuation.iteritems():
		_text = _text.replace(k,v)
	words = _text.split()
	
	#words = [replacements.get(w, w) for w in words]
	dbg(2, '{:d} words'.format(len(words)))
	
	dbg(3, '|'.join(words))
	if words[0] == '<S>':
		words.pop(0)
	if words[-1] == '<S>':
		words.pop(-1)

	for w1,w2 in zip(['<S>']+words,words+['<S>']):
		dbg(3, 'pair: {},	{}'.format(w1,w2))
		p1 = pairs.get(w1, {})
		p2 = p1.get(w2, 0)
		p1[w2] = p2 + 1
		pairs[w1]=p1

	return pairs

def _pairs_dict_to_df(pairs):
	"""TODO: this can be more efficient, I'm sure"""
	ret = pd.DataFrame.from_dict(pairs, orient='index').stack().astype(int)
	ret = ret.sortlevel(sort_remaining=True) #TODO: this doesn't seem to sort the second level... wtf?
	return ret

def extract_collocations(text,
		order=1,
		pairs=None):
	return _pairs_dict_to_df(_count_collocations(text,order,pairs))

def create_network(pairs):
	"""expect a pairs DF"""
	net = nx.DiGraph()
	#net.add_nodes(pairs.index.levels[0])
	#net.add_nodes(pairs.index.levels[1])
	net.add_weighted_edges_from(pairs.reset_index().to_records(index=False))

	return net

def net_weights(net):
	"is this really necessary?"
	return pd.DataFrame.from_records(
			[(a,b,c['weight']) for a,b,c in net.edges(data=True)],
			columns=('word1','word2','weight'),
			index=('word1','word2'),
			)

def plot_net(net,
		MaxLineWidth=10,
		MinLineWidth=1):
	pp.figure(facecolor='Grey')

	pos = nx.graphviz_layout(net)

	font = {'fontname'   : 'Helvetica',
            'font_color'      : 'white',
            #'fontweight' : 'bold',
            'font_size'   : 36}
	weights = net_weights(net)['weight']
	widths = np.log(weights)
	widths -= widths.min()-MinLineWidth
	widths /= widths.max()
	widths *= MaxLineWidth
	nx.draw_networkx_edges(net, pos,
			width=widths,
			arrows=True
			)

	nx.draw_networkx_labels(net, pos,
			**font)

	ax = pp.gca()

	# Remove grid lines (dotted lines inside plot)
	ax.grid(False)
	# Remove plot frame
	ax.set_frame_on(False)
	pp.axis('off')
	# Pandas trick: remove weird dotted line on axis
	#ax.lines[0].set_visible(False)
 
	# Customize title, set position, allow space on top of plot for title
	#ax.set_title(ax.get_title(), fontsize=26, alpha=a, ha='left')
	#plt.subplots_adjust(top=0.9)
	#ax.title.set_position((0,1.08))
 
	# Set x axis label on top of plot, set label text
	#ax.xaxis.set_label_position('top')
	#xlab = 'Population (in millions)'
	#ax.set_xlabel(xlab, fontsize=20, alpha=a, ha='left')
	#ax.xaxis.set_label_coords(0, 1.04)
 
# Position x tick labels on top
#ax.xaxis.tick_top()
# Remove tick lines in x and y axes
#ax.yaxis.set_ticks_position('none')
#ax.xaxis.set_ticks_position('none')
 
# Customize x tick lables
#xticks = [5,10,20,50,80]
#ax.xaxis.set_ticks(xticks)
#ax.set_xticklabels(xticks, fontsize=16, alpha=a)
 
# Customize y tick labels
#yticks = [item.get_text() for item in ax.get_yticklabels()]
#ax.set_yticklabels(yticks, fontsize=16, alpha=a)
#ax.yaxis.set_tick_params(pad=12)

	pp.show()

if __name__ == '__main__':
	import sys

	text = """This example text should help to picture what I mean here and to allow me to make my idea clearer. I want to make this as simple as possible. I want to give an example of the basic idea I am writing about."""

	if len(sys.argv) > 1:
		fpath = sys.argv[1]
		with open(fpath, 'r') as f:
			text = f.read()
	
	recreate_net=False
	try:
		pairs
	except NameError:
		pairs = extract_collocations(text, order=2)
		recreate_net = True
		dbg(1, 'pairs:\n'+str(pairs))
	
	try:
		net
	except NameError:
		recreate_net = True

	dbg(0, 'median collocation frequency: {:d}'.format(int(pairs.median())))
	dbg(0, 'mean collocation frequency: {:.1f}'.format(int(pairs.mean())))
	dbg(0, 'max collocation frequency: {:d}'.format(int(pairs.max())))

	if recreate_net:
		net = create_network(pairs[pairs>30])

	plot_net(net)
