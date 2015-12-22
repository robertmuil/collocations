# Collocation Frequency Patterns as a way to bootstrap Meaning

Determine collocation frequencies in a message or corpus and use these collocations to:

1. suggest next word
1. suggest spelling corrections.
1. determine vocabulary size:
 - collocations can be reduced to single-word frequencies easily (group by 1st of pair and sum frequencies)
1. constrain vocabulary size:
 - when vocabulary size exceeded:
  1. find least-used word
  1. determine synonym phrase that exists in current vocabulary (e.g. by asking user)
  1. replace least-used word by synonym phrase in text
1. determine (and suggest) synonyms
 - this could lead to an automatic way of simplifying text: an automated way to reduce vocabulary to commonly used words.
  - this idea comes from Randall Monroe's 'Thing Explainer'
1. graph word relationships
 - this could be done in realtime, while writing

# Implementation

Maintain a list of ordered pairs.

One list per collocation-order.

Must be ordered because word order matters, and we're storing the frequencies of occurrences in the seen text.

## Example

This example text should help to picture what I mean here and to allow me to make my idea clearer. I want to make this as simple as possible. I want to give an example of the basic idea I am writing about.

##Collocation Frequencies

### 1st-order

(<Capital>,	i)	2
(<Capital>,	this)	1
(<S>,	i)	2
(<S>,	this)	1
(about,	<S>)	1
(allow,	me)	1
(am,	writing)	1
(am,	example)	1
(and,	to)	1
(as,	simple)	1
(as,	possible)	1
(basic,	idea)	1
(clearer,	<S>	1
(example,	text)	1
(example,	of)	1
(give,	an)	1
(i,	am)	1
(i,	mean)	1
(i,	want)	2
(idea,	clearer)	1
(idea,	i)	1
(help,	to)	1
(here,	and)	1
(make,	my)	1
(make,	this)	1
(me,	to)	1
(mean,	here)	1
(my,	idea)	1
(of,	the)	1
(picture,	what)	1
(possible,	<S>)	1
(should,	help)	1
(simple,	as)	1
(text,	should)	1
(the,	basic)	1
(this,	as)	1
(this,	example)	1
(to,	allow)	1
(to,	make)	2
(to,	picture)	1
(to,	give)	1
(want,	to)	2
(what,	I)	1
(writing,	about)	1

# Determining Synonyms from collocations

With just a list of collocation frequencies, can we start to determine possible synonyms?

In other words are a word's meaning defined by or at least constrained by its collocation frequency pattern?

- would require at mininum a very large training corpus, because many words will have similar collocation frequency patterns but very different meanings.
 - The cat ate the rat. - could this be detected as an outlier based on its other collocation frequencies?
 - The cat scared the rat.
 - The cat frightened the rat.

# Special words

## Sentence Position

Could represent position of a word within the sentence with some special words in the collocation lists:

- <Start> = start of sentence
- <End> = end of sentence
- <Bound> = start or end
- <S> = Bound (just shorter, for Sentence)

Do we need <Start> and <End>? If <Bound> is first of pair, it is the start, if second, it is end...

## POS

Could even represent parts-of-speech suchly:

- <Noun>
- <Proper Noun>
- <Verb>
- <Noun Phrase>
- <Verb Phrase>
- <Adjective>
- <Adverb>
- <Pronoun>

This would allow reconstruction of the grammar: In principle, if the POS scanner works reliably, then 

But this may even be useable to *create* the part-of-speech scanner, by essentially bootstrapping itself.
 - start with a word being classified as an unknwn POS, and slowly build up frequencies of positions... hmm but how would an unknown POS be matched to another unknown POS?
  - have a guess at what it is, estimate the probability of this guess (in Bayesian sence of our 'knowledge', rather than frequency) and then update the collocation frequencies with a weighted increase:
   - e.g. if jump comes along, we classify it as .5 noun and .5 verb, then we look at collocations around jump to see which is more likely?
 - could begin by putting our own knowledge in in the form of constraints: 
  - adjectives proceed nouns...
   - are there any solid constraints such as this, that do not involve full specification of a chomskian grammar?

## Punctuation

May even make sense to represent punctuation, including capitalisation. This only makes sense for punctuations that can change the meaning of the words with regard to their frequencies. Not sure if question mark, for example, has a different collocation pattern with the words that precede it than a standard full-stop.

### In any position
- <Comma> - this signifies the end of a phrase or a list, and in both cases, the collocation meaning, in terms of the words before and after the comma is not the same as it would have been if no comma had existed...

### As first of pair
- <Capital> - means the first character of the 2nd word in the collocation is capitalised.
- <Capitals> - means the whole of the 2nd word in the collocation is capitalised.

### As second of pair
- <Question>	the first word is followed by a question mark

# Minimum Vocabulary Size: the Axiomatic Words?

If we replace rarely-used words with synonymous phrases constructed of commonly-used words, and do this repeatedly to reduce the size of the used vocabulary, will we eventually hit a list of words that form the basic atoms of the language? Words with which all other words can be represented in meaning - words which the language can on no account do without.

This of course is not a real possibility in that almost no synonym phrase will perfectly capture a single word's meaning - certainly at the very least it will lose the aesthetic aspects: one must be seriously poetically deprived to consider, for example, 'very very big' to be synonymous with 'enormous'.

However, this concept of Axiomatic Words is interesting from a theoretically point of view, to understand language - not to propose a new Orwellian sort of restyling of peoples' expression.

## Hypothesis: several such axiomatic word lists would exist

If it is possible to do such a search which terminates in a list of axiomatic words, it may be the case that this list is not unique, but that several lists of the same size exist which fit the same constraints.

Indeed, it could very well be that the style in which one does the reduction (the order of synonym replacement, for example) may dictate the size of the resulting list of axiomatic words.

## Homonyms

For such a vocabulary reduction, it would seem at least desireable, if not necessary, to store not simply store words but store homonyms: i.e. store the words separately depending on their use. It is possible, for example, to replace 'train' with 'automobile on tracks' in some circumstances but obviously not in the sentence 'Train every day and an expert you shall become.'

Maybe this could partially be dealt with by splitting the word into two homonyms in the collocation list whenever a synonym replacement is rejected.

# Context-Free Grammar

Does context freedom mean that you do not need to know the context of a sentence to determine / and indeed to confirm the grammatical structure of that sentence?

I.e. is the largest unit of grammatical analysis always the sentence?
This would make it different from a statistial approach, in that this approach allows global statistics to influence sentences.

# vim: filetype=markdown:tabstop=20
