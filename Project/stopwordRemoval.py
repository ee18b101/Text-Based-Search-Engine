from util import *

# Add your import statements here
from nltk.corpus import stopwords



class StopwordRemoval():

	def fromList(self, text):
		"""
		Sentence Segmentation using the Punkt Tokenizer

		Parameters
		----------
		arg1 : list
			A list of lists where each sub-list is a sequence of tokens
			representing a sentence

		Returns
		-------
		list
			A list of lists where each sub-list is a sequence of tokens
			representing a sentence with stopwords removed
		"""

		stopwordRemovedText = None

		#Fill in code here

		stopwordRemovedText = []

		stop_words = set(stopwords.words('english'))

		for sentence in text:
			removed_sentence = [word for word in sentence if word not in stop_words]
			stopwordRemovedText.append(removed_sentence)
		
		return stopwordRemovedText




	