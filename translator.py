#! /usr/bin/env python2.7
from nltk.corpus import cmudict
from string import digits
from neighbor_metric import NeighborGroups
SKIP = ''

class Translator(object):
	def _flatten_list(self, l):
		l = reduce(lambda x,y: x.extend(y), l)
		return l

	# remove digits from pronounciation
	def __clean_one__(self, p):
		return p.translate(None, digits)

	def __clean_pronounce__(self, p):
		return [pp.translate(None, digits) for pp in p]

	def __init__(self):
		self.d = cmudict.dict()

		self.to_plaintext = {}
		self.neighbors = NeighborGroups()
		for key, pronounce_list in self.d.iteritems():
			for pronounce in pronounce_list:
				pronounce = self.__clean_pronounce__(pronounce)
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
	def get_plaintext(self, pronounciation, budget=None):
		if budget:
			raw_results = self.__get_plaintext_rec_budget(pronounciation, budget=budget)
			if raw_results:
				return sorted(list(set(raw_results)), key=lambda x: x[1])
			else:
				return None
		else:
			return sorted(list(set(self.__get_plaintext_rec(pronounciation))))
		
	def __make_plaintext_word(self, current_word_list):
		return self.to_plaintext.get(tuple(current_word))

	# if budget is given, returns a list, where each element is a tuple with a word and a *cost* for that word
	# if budget is not given, then just returns a lit of possible words that can be formed with the pronounication
	def attempt_finish(self, pron, budget=None):
		if budget:
			#import pdb; pdb.set_trace()
			SKIP_GROUP = self.get_neighbors(SKIP, budget)
			words_and_cost = []
			for skip_element, cost in (SKIP_GROUP + [(SKIP, 0)]):
				if cost > budget:
					continue

				pron_tuple = tuple(pron)
				if skip_element != '':
					pron_tuple = tuple(pron + [skip_element])
				possible_words = self.to_plaintext.get(pron_tuple, [])

				words_and_cost += zip(possible_words, [cost] * len(possible_words))
			return words_and_cost

		else:
			SKIP_GROUP = self.get_neighbors(SKIP)
			words = []
			for skip_element in (SKIP_GROUP + [SKIP]):
				
				pron_tuple = tuple(pron)	
				if skip_element != '':
					pron_tuple = tuple(pron + [skip_element])
				

				possible_words = self.to_plaintext.get(pron_tuple, [])
				for word in possible_words:
					words += [word]
				
			return words


	# i is the 'next' syllable to consider
	# current_word is the list of pronounciations that's being built up right now.
	# current_prefix are the words built up so far
	# if budget is set, then will return tuples with distance metrics
	def get_neighbors(self, syll, budget=None):
		if not budget:
			return [item[0] for item in self.neighbors.get_neighbors(syll)]
		else:
			return self.neighbors.get_neighbors(syll, budget)



	def __get_plaintext_rec_budget(self, pronou, current_prefix='', i=0, current_word=[], budget=-1):
		if budget and budget<0:
			return None


		iteration_results = []
		appended = []
		debug = False

		words_and_cost = self.attempt_finish(current_word,budget)
	 	if len(words_and_cost) > 0:
	 		if len(current_prefix) > 0:
	 			appended = [(current_prefix + " " + word, budget-cost) for (word, cost) in words_and_cost]
	 		else:
	 			appended = [(word, budget-cost) for (word,cost) in words_and_cost]


	 	# end of the utterance
	 	if i >= len(pronou):	
	 		if len(appended) > 0:
	 			return appended
	 		else:
	 			return None

	 	else:
	 		# make recursive calls for each new prefix (if any)
	 		for prefix, remaining_budget in appended:
	 			attempted_recursion_result = self.__get_plaintext_rec_budget(pronou, prefix, i, [], remaining_budget)
	 			if attempted_recursion_result:
	 				iteration_results += attempted_recursion_result
	 		
	 		# also try not finishing the word and produce recursive call
	 		syllable = self.__clean_one__(pronou[i])

	 		syllable_group = self.get_neighbors(syllable, budget) + [(syllable,0)]
	 
	 		
	 		for syllable, cost in syllable_group:
	 			next_word = None
	 			if syllable != SKIP:
	 				next_word = current_word + [syllable]
	 			else:
	 				next_word = current_word

 				rec_result = self.__get_plaintext_rec_budget(pronou, current_prefix, i+1, next_word, budget-cost)
	 			

	 			if rec_result:
	 				iteration_results += rec_result

	 		if len(current_word) == 0:
	 			# assume silent letters only at the beginning, ignore SKIP
	 			silent_group = self.get_neighbors(SKIP, budget)
	 			for silent_syl, cost in silent_group:
	 				rec_result = self.__get_plaintext_rec_budget(pronou, current_prefix, i, current_word + [silent_syl], budget-cost)
	 			if rec_result:
	 				iteration_results += rec_result

	 		if len(iteration_results) > 0:
	 			return iteration_results
	 		else:
	 			return None



	def __get_plaintext_rec(self, pronou, current_prefix='', i=0, current_word=[]):
		# current syllable + replacements
		# attempt to make a word by calling attempt_finish
		# make a recursive call on each possible result + "skip" group
		# make a recursive call by not finishing a word for every combination
		# base case: if finish word works with possible "skips"
		#          if works, then resturn the prefix
		# one level up. get all the results that are not None and return them.
		# if i==3:
		# 	passimport pdb; pdb.set_trace()
		iteration_results = []
		appended = []
		debug = False

		words = self.attempt_finish(current_word,debug)
	 	if len(words) > 0:
	 		if len(current_prefix) > 0:
	 			appended = [current_prefix + " " + word for word in words]
	 		else:
	 			appended = words



	 	if i >= len(pronou):	 		
	 		if len(appended) > 0:
	 			return appended
	 		else:
	 			return None

	 	else:
	 		# make recursive calls for each new prefix (if any)
	 		for prefix in appended:
	 			attempted_recursion_result = self.__get_plaintext_rec(pronou, prefix, i, [])
	 			if attempted_recursion_result:
	 				iteration_results += attempted_recursion_result
	 		
	 		# also try not finishing the word and produce recursive call
	 		syllable = self.__clean_one__(pronou[i])
	 		syllable_group = self.get_neighbors(syllable) + [syllable]

	 		for syllable in syllable_group:
	 			next_word = None
	 			if syllable != SKIP:
	 				next_word = current_word + [syllable]
	 			else:
	 				next_word = current_word

 				rec_result = self.__get_plaintext_rec(pronou, current_prefix, i+1, next_word)
	 			

	 			if rec_result:
	 				iteration_results += rec_result

	 		if len(current_word) == 0:
	 			# assume silent letters only at the beginning
	 			silent_group = self.get_neighbors(SKIP)
	 			for silent_syl in silent_group:
	 				rec_result = self.__get_plaintext_rec(pronou, current_prefix, i, current_word + [silent_syl])
	 			if rec_result:
	 				iteration_results += rec_result

	 		if len(iteration_results) > 0:
	 			return iteration_results
	 		else:
	 			return None


	