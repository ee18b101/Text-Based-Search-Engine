from sentenceSegmentation import SentenceSegmentation
from tokenization import Tokenization
from inflectionReduction import InflectionReduction
from stopwordRemoval import StopwordRemoval
from ESA_Wiki import InformationRetrieval
from evaluation import Evaluation

from sys import version_info
import argparse
import json
import matplotlib.pyplot as plt
import numpy as np

from query_autocomplete import Query_AutoComplete

import contextualSpellCheck
import spacy

# Input compatibility for Python 2 and Python 3
if version_info.major == 3:
    pass
elif version_info.major == 2:
    try:
        input = raw_input
    except NameError:
        pass
else:
    print("Unknown python version - input function not safe")

import warnings

warnings.filterwarnings("ignore")


class SearchEngine:

    def __init__(self, args):
        self.args = args

        self.tokenizer = Tokenization()
        self.sentenceSegmenter = SentenceSegmentation()
        self.inflectionReducer = InflectionReduction()
        self.stopwordRemover = StopwordRemoval()

        self.informationRetriever = InformationRetrieval()
        self.evaluator = Evaluation()
        self.autocomplete = Query_AutoComplete()

        print('Retrieveing Spacy Model...')
        self.nlp = spacy.load("en_core_web_sm")
        self.nlp.add_pipe("contextual spellchecker")
        print('Finished Retrieval')

        self.N = 6

    def segmentSentences(self, text):
        """
		Call the required sentence segmenter
		"""
        if self.args.segmenter == "naive":
            return self.sentenceSegmenter.naive(text)
        elif self.args.segmenter == "punkt":
            return self.sentenceSegmenter.punkt(text)

    def tokenize(self, text):
        """
		Call the required tokenizer
		"""
        if self.args.tokenizer == "naive":
            return self.tokenizer.naive(text)
        elif self.args.tokenizer == "ptb":
            return self.tokenizer.pennTreeBank(text)

    def reduceInflection(self, text):
        """
		Call the required stemmer/lemmatizer
		"""
        return self.inflectionReducer.reduce(text)

    def removeStopwords(self, text):
        """
		Call the required stopword remover
		"""
        return self.stopwordRemover.fromList(text)

    def spell_correction(self, text):
        """
		Correct all Spelling Errors
		"""
        return self.nlp(text)._.outcome_spellCheck

    def preprocessQueries(self, queries):
        """
		Preprocess the queries - segment, tokenize, stem/lemmatize and remove stopwords
		"""

        # Segment queries
        segmentedQueries = []
        for query in queries:
            if args.spellcheck or args.spellcheck_query:
                spell_corrected_query = self.spell_correction(query)
            else:
                spell_corrected_query = query
            segmentedQuery = self.segmentSentences(spell_corrected_query)
            segmentedQueries.append(segmentedQuery)
        json.dump(segmentedQueries, open(self.args.out_folder + "segmented_queries.txt", 'w'))
        # Tokenize queries
        tokenizedQueries = []
        for query in segmentedQueries:
            tokenizedQuery = self.tokenize(query)
            tokenizedQueries.append(tokenizedQuery)
        json.dump(tokenizedQueries, open(self.args.out_folder + "tokenized_queries.txt", 'w'))
        # Stem/Lemmatize queries
        reducedQueries = []
        for query in tokenizedQueries:
            reducedQuery = self.reduceInflection(query)
            reducedQueries.append(reducedQuery)
        json.dump(reducedQueries, open(self.args.out_folder + "reduced_queries.txt", 'w'))
        # Remove stopwords from queries
        stopwordRemovedQueries = []
        for query in reducedQueries:
            stopwordRemovedQuery = self.removeStopwords(query)
            stopwordRemovedQueries.append(stopwordRemovedQuery)
        json.dump(stopwordRemovedQueries, open(self.args.out_folder + "stopword_removed_queries.txt", 'w'))

        preprocessedQueries = stopwordRemovedQueries
        return preprocessedQueries

    def preprocessDocs(self, docs):
        """
		Preprocess the documents
		"""

        # Segment docs
        segmentedDocs = []
        for doc in docs:
            if args.spellcheck or args.spellcheck_doc:
                spell_corrected_doc = self.spell_correction(doc)
            else:
                spell_corrected_doc = doc
            segmentedDoc = self.segmentSentences(spell_corrected_doc)
            segmentedDocs.append(segmentedDoc)
        json.dump(segmentedDocs, open(self.args.out_folder + "segmented_docs.txt", 'w'))
        # Tokenize docs
        tokenizedDocs = []
        for doc in segmentedDocs:
            tokenizedDoc = self.tokenize(doc)
            tokenizedDocs.append(tokenizedDoc)
        json.dump(tokenizedDocs, open(self.args.out_folder + "tokenized_docs.txt", 'w'))
        # Stem/Lemmatize docs
        reducedDocs = []
        for doc in tokenizedDocs:
            reducedDoc = self.reduceInflection(doc)
            reducedDocs.append(reducedDoc)
        json.dump(reducedDocs, open(self.args.out_folder + "reduced_docs.txt", 'w'))
        # Remove stopwords from docs
        stopwordRemovedDocs = []
        for doc in reducedDocs:
            stopwordRemovedDoc = self.removeStopwords(doc)
            stopwordRemovedDocs.append(stopwordRemovedDoc)
        json.dump(stopwordRemovedDocs, open(self.args.out_folder + "stopword_removed_docs.txt", 'w'))

        preprocessedDocs = stopwordRemovedDocs
        return preprocessedDocs

    def evaluateDataset(self):
        """
		- preprocesses the queries and documents, stores in output folder
		- invokes the IR system
		- evaluates precision, recall, fscore, nDCG and MAP 
		  for all queries in the Cranfield dataset
		- produces graphs of the evaluation metrics in the output folder
		"""

        # Read queries
        queries_json = json.load(open(args.dataset + "cran_queries.json", 'r'))[:]
        query_ids, queries = [item["query number"] for item in queries_json], \
                             [item["query"] for item in queries_json]
        # Process queries
        print('Preprocessing Queries...')
        processedQueries = self.preprocessQueries(queries)
        # len_queries = []
        # for query in processedQueries:
        # 	len_queries.append(len(query[0]))
        # print('Average Length of queries: ', np.mean(np.array(len_queries)))
        print('Queries Preprocessed')
        # Read documents
        docs_json = json.load(open(args.dataset + "cran_docs.json", 'r'))[:]
        doc_ids, docs = [item["id"] for item in docs_json], \
                        [item["body"] for item in docs_json]
        # Process documents
        print('Preprocessing Documents...')
        processedDocs = self.preprocessDocs(docs)
        print('Documents Preprocessed')
        # Build document concept vectors
        print('Building Document Concept Vectors...')
        self.informationRetriever.build_concept_vectors(processedDocs, doc_ids)
        print('Done!')
        # Rank the documents for each query
        print('Ranking Documents for Queries...')
        doc_IDs_ordered = self.informationRetriever.rank(processedQueries)
        print('Done!')

        # Read relevance judements
        print('Calculating nDCG scores and generating plots')
        qrels = json.load(open(args.dataset + "cran_qrels.json", 'r'))[:]

        # Calculate precision, recall, f-score, MAP and nDCG for k = 1 to 10
        precisions, recalls, fscores, MAPs, nDCGs = [], [], [], [], []
        for k in range(1, 11):
            precision = self.evaluator.meanPrecision(
                doc_IDs_ordered, query_ids, qrels, k)
            precisions.append(precision)
            recall = self.evaluator.meanRecall(
                doc_IDs_ordered, query_ids, qrels, k)
            recalls.append(recall)
            fscore = self.evaluator.meanFscore(
                doc_IDs_ordered, query_ids, qrels, k)
            fscores.append(fscore)
            print("Precision, Recall and F-score @ " +
                  str(k) + " : " + str(precision) + ", " + str(recall) +
                  ", " + str(fscore))
            MAP = self.evaluator.meanAveragePrecision(
                doc_IDs_ordered, query_ids, qrels, k)
            MAPs.append(MAP)
            nDCG = self.evaluator.meanNDCG(
                doc_IDs_ordered, query_ids, qrels, k)
            nDCGs.append(nDCG)
            print("MAP, nDCG @ " +
                  str(k) + " : " + str(MAP) + ", " + str(nDCG))

        # Plot the metrics and save plot
        plt.plot(range(1, 11), precisions, label="Precision")
        plt.plot(range(1, 11), recalls, label="Recall")
        plt.plot(range(1, 11), fscores, label="F-Score")
        plt.plot(range(1, 11), MAPs, label="MAP")
        plt.plot(range(1, 11), nDCGs, label="nDCG")
        plt.legend()
        plt.title("Evaluation Metrics - Cranfield Dataset")
        plt.xlabel("k")
        plt.savefig(args.out_folder + "eval_plot.png")

    def evaluate_query_autocomplete(self):
        """
		Evaluates the Query Autocomplete System based on queries
		from the Cranfild Dataset.
		"""

        # Read queries
        queries_json = json.load(open(args.dataset + "cran_queries.json", 'r'))[:]
        query_ids, queries = [item["query number"] for item in queries_json], \
                             [item["query"] for item in queries_json]

        # records success rate at k
        success_at_k = np.zeros((5,), dtype=float)

        # used to count number of iterations without skipping
        count_iterations = 0

        # iterate over every query and feed the first N words
        # into the QAC system and calculate the success rate at k score
        for i, query in enumerate(queries):
            print(i + 1, '/', len(queries), ' done')
            query_split = query.split()

            # if length of query is less than N then ignore query
            if len(query_split) <= self.N:
                continue

            count_iterations += 1

            # first N words of the query
            shortened_query = ' '.join(query_split[:self.N])

            # recieve the candidate list and scores
            query_ranks = self.autocomplete.candidate_ranking(shortened_query)
            candidate_list = [x['query'] for x in query_ranks]

            # calculate the success rate at k score
            for k in range(5):
                if query in candidate_list[:k + 1]:
                    success_at_k[k] += 1
        success_at_k = success_at_k / count_iterations * 100

        for k in range(5):
            print('Success rate@', k + 1, ': ', success_at_k[k])

    def handleCustomQuery(self):
        """
		Take a custom query as input and return top five relevant documents
		"""

        # Get query
        print("Enter query below")
        query = input()
        # Process documents
        processedQuery = self.preprocessQueries([query])[0]

        # Read documents
        docs_json = json.load(open(args.dataset + "cran_docs.json", 'r'))[:]
        doc_ids, docs = [item["id"] for item in docs_json], \
                        [item["body"] for item in docs_json]
        # Process documents
        processedDocs = self.preprocessDocs(docs)

        # Build document index
        self.informationRetriever.build_concept_vectors(processedDocs, doc_ids)
        # Rank the documents for the query
        doc_IDs_ordered = self.informationRetriever.rank([query])[0]

        # Print the IDs of first five documents
        print("\nTop five document IDs : ")
        for id_ in doc_IDs_ordered[:5]:
            print(id_)


if __name__ == "__main__":

    # Create an argument parser
    parser = argparse.ArgumentParser(description='main.py')

    # Tunable parameters as external arguments
    parser.add_argument('-dataset', default="cranfield/",
                        help="Path to the dataset folder")
    parser.add_argument('-out_folder', default="output/",
                        help="Path to output folder")
    parser.add_argument('-segmenter', default="punkt",
                        help="Sentence Segmenter Type [naive|punkt]")
    parser.add_argument('-tokenizer', default="ptb",
                        help="Tokenizer Type [naive|ptb]")
    parser.add_argument('-custom', action="store_true",
                        help="Take custom query as input")
    parser.add_argument('-spellcheck', action='store_true',
                        help="Enable Spellcheck")
    parser.add_argument('-spellcheck_doc', action='store_true',
                        help="Enable Spellcheck for Documents only")
    parser.add_argument('-spellcheck_query', action='store_true',
                        help="Enable Spellcheck for Queries only")
    parser.add_argument('-eval_query', action='store_true',
                        help="Evaluate Query Autocomplete")

    # Parse the input arguments
    args = parser.parse_args()

    # Create an instance of the Search Engine
    searchEngine = SearchEngine(args)

    # Either handle query from user or evaluate the Query Autocomplete System
    # or evaluate the Information Retrieval System
    if args.custom:
        args.spellcheck_query = True
        searchEngine.handleCustomQuery()
    elif args.eval_query:
        searchEngine.evaluate_query_autocomplete()
    else:
        searchEngine.evaluateDataset()
