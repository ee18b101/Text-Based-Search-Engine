from util import *

# Add your import statements here
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer



class InflectionReduction:

	def reduce(self, text):
		"""
		Stemming/Lemmatization

		Parameters
		----------
		arg1 : list
			A list of lists where each sub-list a sequence of tokens
			representing a sentence

		Returns
		-------
		list
			A list of lists where each sub-list is a sequence of
			stemmed/lemmatized tokens representing a sentence
		"""

		reducedText = None

		#Fill in code here

		
		# # Stemming via Porter's Algorithm
		# stemmer = PorterStemmer()

		# for sentence in text:
		# 	for i in range(len(sentence)):
		# 		sentence[i] = stemmer.stem(sentence[i])

		# reducedText = text

		reducedText = []
		# Lemmatizer from NLTK Package
		lemmatizer = WordNetLemmatizer()

		for sentence in text:
			for i in range(len(sentence)):
				sentence[i] = lemmatizer.lemmatize(sentence[i])
			reducedText.append(sentence)

		return reducedText


