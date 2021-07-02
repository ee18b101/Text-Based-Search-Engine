from util import *

# Add your import statements here
import nltk

class SentenceSegmentation():

	def naive(self, text):
		"""
		Sentence Segmentation using a Naive Approach

		Parameters
		----------
		arg1 : str
			A string (a bunch of sentences)

		Returns
		-------
		list
			A list of strings where each string is a single sentence
		"""

		segmentedText = None

		#Fill in code here

		# The most naive approach would be to split sentences at the end of punctuations
		# such as '.', '?', '!'
		# Whenever one of these punctuations appear, we break the sentence.

		segmentedText = []

		# The list of punctuations are as follows (comma not included as sentences 
		# don't end on commas.)

		punctuation = ['.', '?', '!']


		prev_i = 0
		for i in range(len(text)):
			if text[i] in punctuation:
				segmentedText.append(text[prev_i:i+1])
				prev_i = i+1

		return segmentedText





	def punkt(self, text):
		"""
		Sentence Segmentation using the Punkt Tokenizer

		Parameters
		----------
		arg1 : str
			A string (a bunch of sentences)

		Returns
		-------
		list
			A list of strings where each strin is a single sentence
		"""

		segmentedText = None

		#Fill in code here

		# importing the pre-trained punkt tokenizer from the punkt package
		sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

		# segmenting the text using punkt tokenizer
		segmentedText = sent_detector.tokenize(text.strip())

		return segmentedText