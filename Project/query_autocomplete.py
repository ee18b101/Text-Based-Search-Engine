import numpy as np
from sys import version_info
import argparse
import json
import matplotlib.pyplot as plt
import os
import subprocess
import pathlib

from candidate_generation import candidate_generation

class Query_AutoComplete:
	def __init__(self):
		candidate_generation()


	# generate possible candidates for the given query by choosing
	# queries that start with the last term of given query
	def gen_query_candidates(self, query):

		# getting last term of query
		last_term = query.split()[-1]

		# if the query is just one word, the last_term_flag
		# is set to True
		last_term_flag = False
		if len(query.split()) == 1:
			last_term_flag = True

		# list of query candidates
		query_candidates = []

		# getting those candidates whose first letters start with
		# the last term of the given query
		for c in self.candidates:
			if last_term == c[:len(last_term)]:
				query_candidates.append(c)

		return query_candidates, last_term, last_term_flag

	# Calls the generate candidate function and calculates
	# relevance scores for each based on the CDDSM Model and
	# returns the sorted list of possible suggestions in descending
	# order of relevance score
	def candidate_ranking(self, query):

		# import the candidates into list
		candidates_json = json.load(open("./cranfield/ngrams_cran_queries.json", 'r'))
		self.candidates = candidates_json['data']

		# retrieve the candidates for given query
		query_candidates, last_term, last_term_flag = self.gen_query_candidates(query)

		# query_revised is the query without the incomplete last term
		if not last_term_flag:
			query_revised = query[:-len(last_term)]
		else:
			query_revised = query

		# deleting and opening file pairs.txt to give as input to
		# the CDDSM Model
		PATH = "./Sent2VecV2/Sent2Vec/sample/sent2vec/"
		if os.path.exists(PATH+'pairs.txt'):
			os.remove(PATH+'pairs.txt')

		# writing into the pairs.txt file the query and the possible
		# candidates
		f = open(PATH+'pairs.txt', "w")
		for qc in query_candidates:
			f.write(query_revised+'\t'+qc+'\n')
		f.close()

		# Running the CDDSM to get relevence scores
		p = pathlib.PureWindowsPath(os.getcwd())
		filepath = str(p.as_posix()) + "/Sent2VecV2/Sent2Vec/sample/sent2vec/run.bat"
		p = subprocess.Popen(filepath, shell=True, stdout=subprocess.PIPE)
		stdout, stderr = p.communicate()

		# Reading the relevance scores by the CDDSM for each pair of
		# query and candidate
		f = open(PATH+'cdssm_out.score.txt', 'r')
		scores = f.read().split('\n')[:-1]

		candidate_scores = []

		# storing in dictonary format each suggestion and it's score
		for i, qc in enumerate(query_candidates):
			if last_term_flag == True:
				candidate_scores.append({'query':qc, 'score':float(scores[i])})
			else:
				candidate_scores.append({'query': query_revised + qc, 'score': float(scores[i])})

		# sorting all the candidate suggestions in descending order
		# as per relevance scores
		candidate_scores.sort(reverse=True, key=lambda x: x['score'])

		# return sorted list
		return candidate_scores



"""
In case you want to test the query_autcomplete module alone, 
uncomment and enter your query here
"""
# obj = Query_AutoComplete()
# candidate_scores = obj.candidate_ranking('structural and aero')
# print(candidate_scores[:5])