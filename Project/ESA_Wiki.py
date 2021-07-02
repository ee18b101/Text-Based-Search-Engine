from util import *
from esa_wiki.cunning_linguistics import SemanticAnalyser
import numpy as np
import operator
import json
import datetime as dt
from numpy import dot
from numpy.linalg import norm
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore")


class InformationRetrieval():

    def __init__(self):
        self.doc_concepts = None
        self.doc_IDs_ordered = None
        self.analyser = SemanticAnalyser('./esa_wiki-0.0.1/matrix')

        # passage size
        self.N = 50

    def remake_doc(self, doc):
        """
        Remake the document/query from the preprocessed form into
        a set of passages.
        """
        remade_doc = []

        # for each sentence join each sentence in terms of passages
        for sentence in doc:
            for i in range(0, len(sentence), self.N):
                if i+self.N >= len(sentence):
                    remade_doc.append(' '.join(sentence[i:]))
                else:
                    remade_doc.append(' '.join(sentence[i:i+self.N]))


        return remade_doc

    def build_concept_vectors(self, docs, doc_ids):
        """
        Represent each document in terms of ESA Concept Vectors
        using the Semantic Analyser
        """
        self.doc_concepts = [[] for i in range(len(doc_ids))]

        # remake document and convert into ESA concept vectors
        # and store in self.doc_concepts
        for i, doc in enumerate(docs):
            doc = self.remake_doc(doc)
            for passage in doc:
                self.doc_concepts[i].append(self.analyser.interpretation_vector(passage))

    def rank(self, queries):
        """
        convert the query into ESA Concept vector and compare it with
        the document vectors to deteremine relevant documents and rank
        documents using the similarity score (cosine similarity)
        """
        self.doc_IDs_ordered = list(range(len(queries)))

        # main loop
        for i, query in enumerate(queries):
            cosine_scores = []

            # remake the query
            query_remade = self.remake_doc(query)

            # convert the query into an ESA concept vector
            query_concept = []
            for passage in query_remade:
                query_concept.append(self.analyser.interpretation_vector(passage))

            # compare the query vector with the document vector and
            # choose the best performing passage from the document
            # passages and take that as the similarity score of the
            # document.
            for doc_concept in self.doc_concepts:
                if len(doc_concept) == 0:
                    cosine_scores.append(0)
                    continue
                score = []
                for qc in query_concept:
                    for dc in doc_concept:
                        # cosine similarity score calculation
                        score.append(self.analyser.scalar(dc, qc))

                score = np.array(score)
                # add the score of the best performing passage
                cosine_scores.append(np.max(score))

            # order the documents in descending order of similarity scores and add to the
            # ordered docs for the query
            docs_ordered = list(range(len(self.doc_concepts)))
            docs_ordered = [x for _, x in sorted(zip(cosine_scores, docs_ordered), reverse=True)]

            self.doc_IDs_ordered[i] = np.array(docs_ordered)

        return self.doc_IDs_ordered
