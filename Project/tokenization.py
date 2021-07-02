from util import *

# Add your import statements here
from nltk.tokenize import TreebankWordTokenizer



class Tokenization():

	def naive(self, text):
		"""
		Tokenization using a Naive Approach

		Parameters
		----------
		arg1 : list
			A list of strings where each string is a single sentence

		Returns
		-------
		list
			A list of lists where each sub-list is a sequence of tokens
		"""

		tokenizedText = None

		#Fill in code here

		tokenizedText = []

		# The most Naive way to tokenize each sentence would be to split
		# the words seperated by a ' ' (space).

		tokenizedText = [text[i].split(' ') for i in range(len(text))]

		# The problem with such a tokenization is that punctuations
		# carry over as a part of the word. To avoid this,

		punctuation = ['.', '?', '!', '\n']

		text_new = text

		for punct in punctuation:
			text_new = [text[i].replace(punct, ' ' + punct) for i in range(len(text))]

		tokenizedText = [text_new[i].split(' ') for i in range(len(text_new))]

		return tokenizedText



	def pennTreeBank(self, text):
		"""
		Tokenization using the Penn Tree Bank Tokenizer

		Parameters
		----------
		arg1 : list
			A list of strings where each string is a single sentence

		Returns
		-------
		list
			A list of lists where each sub-list is a sequence of tokens
		"""

		tokenizedText = None

		#Fill in code here

		tokenizedText = []
		# The Treebank tokenizer uses regular expressions to tokenize text as in Penn Treebank.
		# Using the Penn Treebank tokenizer present in the nltk package
		for sentence in text:
			tokenizedText.append(TreebankWordTokenizer().tokenize(sentence))


		return tokenizedText