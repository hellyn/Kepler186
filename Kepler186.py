from textblob import TextBlob
import math
import random
import sys


# Radius of the text circle.  The actual number of lines printed will be
# 2 * RADIUS + 1.
DIAMETER = 20

# How much the text circle should be stretched in the horizontal direction to
# compensate for the fact that the cursor with is less than the cursor height.
WIDTH_SCALE = 2.0


#read txt file from command-line argument
textFile=sys.argv[1]

#read text from first file
with file(textFile) as f:
    text = f.read().decode('ascii', errors="replace")

def separateWordsByLength(words):
	# example:
	#   if words = ["hi", "cat", "hat"]
	#   then separateWordsByLength(words) returns
	#     {2: ["hi"], 3: ["cat", "hat"]} 
	wordsByLength = {}
	for word in words:
		if len(word) not in wordsByLength:
			wordsByLength[len(word)] = []
		wordsByLength[len(word)].append(word)
	return wordsByLength

class WordSet():
	def __init__(self, words):
		self.words = words
		self.wordsByLength = separateWordsByLength(words)

	def getWord(self, maxLength):
		if maxLength <= 6:
			if maxLength in self.wordsByLength.keys():
				word = random.choice(self.wordsByLength[maxLength])
				assert len(word) == maxLength, '%s does not have length %d' % (word, maxLength)
				return word
			else:
				return '#' * maxLength
		word = random.choice(self.words)
		if len(word) == maxLength - 1 or len(word) > maxLength:
			return '#' * maxLength
		else:
			return word

		
		


#parse nouns
nouns = list()
for word, tag in TextBlob(text).tags:
	if tag == 'NN':
		nouns.append(word.lemmatize())
nounSet = WordSet(nouns)

#parse adjectives
adjectives = list()
for word, tag in TextBlob(text).tags:
	if tag == 'JJ':
		adjectives.append(word.lemmatize())
adjectiveSet = WordSet(adjectives)

#parse adverbs
adverbs = list()
for word, tag in TextBlob(text).tags:
	if tag == 'RB':
		adverbs.append(word.lemmatize())
adverbSet = WordSet(adverbs)

#parse verbs
verbs = list()
for word, tag in TextBlob(text).tags:
	if tag == 'VB':
		verbs.append(word.lemmatize())
verbSet = WordSet(verbs)

spaceNames=('Kepler-186', 'Planet', 'Neptune', 'Triton', 'Nix', 'Hydra', 'Despina', 'Pandora')
spaceNameSet = WordSet(spaceNames)


# spaceNames (adverbs) verbs ((adverbs) adjectives) nouns

wordTypeSequence = [spaceNameSet, adverbSet, verbSet, adverbSet, adjectiveSet, nounSet]
wordTypeIndex = 0

def nextWordSet():
	global wordTypeIndex
	wordSet = wordTypeSequence[wordTypeIndex]
	wordTypeIndex = (wordTypeIndex + 1) % len(wordTypeSequence)
	return wordSet

# Returns a line of text of the desired length.
def makeLine(desiredLength):
	wordSet = nextWordSet()
	line = wordSet.getWord(desiredLength)
	while len(line) < desiredLength:
		line += ' '
		remainingLength = desiredLength - len(line)
		wordSet = nextWordSet()
		line += wordSet.getWord(remainingLength)
	return line

# Computes the proper line length for the given line number.  It should be the
# case that `0 <= line_num < diameter`.  The result will be multiplied by
# `scale` before being converted to an integer.
def textCircleLineLength(diameter, line_num, scale):
  radius = diameter / 2.0
  # We add 0.5 to `line_num` so that the expected range of line numbers will be
  # centered between 0 and `diameter`.
  line_endpoint_y = line_num + 0.5 - radius
  # We use some basic trig to compute the x coordinate from the y coordinate.
  line_endpoint_x = math.cos(math.asin(line_endpoint_y / radius)) * radius
  return math.trunc(2.0 * scale * line_endpoint_x)

for i in xrange(DIAMETER):
  length = textCircleLineLength(DIAMETER, i, WIDTH_SCALE)
  # The circle will be a bit skewed to one side since you can't perfectly center
  # an odd number of characters on a even-length line (or vice versa) and the
  # center() method below will always round things in the same direction.
  print makeLine(length).center(math.trunc(DIAMETER * WIDTH_SCALE)) + "....."

#print
#for i in range(12):
#	print makeLine(i)
#print

