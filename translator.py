#! /usr/bin/env python2.7
from nltk.corpus import cmudict

class Translator(object):
	def _flatten_list(self, l):
		l = reduce(lambda x,y: x.extend(y), l)
		return l

	def __init__(self):
		self.d = cmudict.dict()
		self.to_plaintext = {}
		self.neighbors = NeighborGroups()
		for key, pronounce_list in self.d.iteritems():
			for pronounce in pronounce_list:
				p = tuple(pronounce)
				plaintext_list = self.to_plaintext.get(p, [])
				plaintext_list += [key]
				self.to_plaintext[p] = plaintext_list

	# Todo: find the best match for phrase alignment before computing
	# Todo: score proximity of syllables
	def distance(self, phrase1, phrase2):
		phrase1_pr = self.get_pronounciation(phrase1)
		phrase2_pr = self.get_pronounciation(phrase2)
		phrase_together = zip(phrase1_pr, phrase2_pr)
		overrun_length = abs(len(phrase1_pr) - len(phrase2_pr))
		correct = len([x for x in phrase_together if x[0] == x[1]])
		false = len(phrase_together) - correct
		score = float(correct) / (len(phrase_together) + overrun_length)
		return score	
	
	def __getitem__(self,key):
		return self.d.get(key,"")

	def get_pronounciation(self, phrase, separated=False):
		phrase_list = phrase.lower().strip().split()
		spoken = []
		for word in phrase_list:
			pronounce = self.d.get(word,None)
			if pronounce and not separated:
				spoken += pronounce[0]
			elif pronounce and separated:
				spoken += pronounce
			else:
				raise Exception("word not pronounceable:", word)
		return spoken

	# returns a sorted list by distance to the supplied pronounciation
	def get_plaintext(self, pronounciation)
		return self.__get_plaintext_rec(pronounciation, 0, '')
		

	def __get_plaintext_rec(self, pronou, i=0, current_word)
	 	if i >= len(pronou):
	 		return []
		current_syllable = pronou[i]
		neighbors = self.neighbors.get_neighbors(current_syllable)
		neighbors += [(current_syllable,0)]

		iteration_results = []
		for neighbor, distance in neighbors:
			# case 1. try to make a word
			plaintext = tuple(current_word[:] + [neighbor])
			self.to_plaintext.
			current_key = tuple(current_word)



		# for each possible syllable interpretation
		# case 1. we make a word and start a new one
		# case 2. we make a continue building the word



	# def get_plaintext(self, pronounciation, syllable = 0, readings = []):
	# 	if syllable >= len(pronounciation):
	# 		return readings

	# 	new_syllable = pronounciation[syllable]
	# 	if syllable == 0:
	# 		potential_words = words
	# 		readings += [[current_syllable]]
	# 	for reading in readings:







