import numpy as np
from sys import version_info
import argparse
import json
import matplotlib.pyplot as plt


# Clean up the queries of period 
def clean_queries(queries):

	cleaned_queries = []

	for query in queries:
		cleaned_queries.append(query.replace(' .', ''))

	return cleaned_queries



# Retrieve Queries from Cranfield Database (this will act
# as the Query Log).
def ret_queries():

	# Read queries
	queries_json = json.load(open("./cranfield/cran_queries.json", 'r'))[:]
	query_ids, queries = [item["query number"] for item in queries_json], \
								[item["query"] for item in queries_json]

	# Clean Queries
	queries = clean_queries(queries)

	return query_ids, queries



def candidate_generation():

	# get cleaned up queries
	query_ids, queries = ret_queries()

	# creating for json dump
	candidates = {}
	candidates['data'] = []

	# create all possible n-grams of end of each query
	# and add as possible candidate
	for query in queries:
		for index,letter in enumerate(query):
			if letter == ' ':
				candidates['data'].append(query[index+1:])

	# save all canndidates in a json file
	with open('./cranfield/ngrams_cran_queries.json', 'w') as outfile:
		json.dump(candidates, outfile)

if __name__ == '__main__':
	candidate_generation()