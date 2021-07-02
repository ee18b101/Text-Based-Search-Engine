# -*- coding: utf-8 -*-

"""Small module for computational linguistics applied to Twitter.
The main classes are a TweetHarvester, which gathers data from Twitters' API,
and a SemanticAnalyser, which relies on the previously constructed TFIDF
matrices."""

from scipy import sparse as sps
from collections import Counter
from numpy.linalg import norm
import re
from esa_wiki import shared
import os

# sys.stdout = codecs.getwriter('utf8')(sys.stdout)
# sys.stderr = codecs.getwriter('utf8')(sys.stderr)

# ==============================================================================
# Defines stuff to analyse text using an already constructed interpretation
# matrix.
# ==============================================================================

from .shared import row_chunk_size, extensions


class SemanticAnalyser(object):
    """Analyser class using Explicit Semantic Analysis (ESA) to process
    text fragments. It can compute semantic (pseudo) distance and similarity,
    as well"""


    def __init__(self, matrix_path: str):
        self.matrix_path = matrix_path

        # Hashes for word and concept indices
        with open(os.path.join(matrix_path, 'word2index.ind'), 'r') as f:
            self.word2index = shared.load(f)
        with open(os.path.join(matrix_path, 'concept2index.ind'), 'r') as f:
            self.concept2index = shared.load(f)
        self.index2concept = {i: c for c, i in self.concept2index.items()}

        # Count number of words and concepts
        self.n_words = len(self.word2index)
        self.n_concepts = len(self.concept2index)

        self.__cache = {}
        self.__max_cache_size = 200


    def clean(self, text):
        text = re.sub('[^\w\s\d\'\-]', '', text)
        text = text.lower()

        return text


    def interpretation_vector(self, text):
        """Converts a text fragment string into a row vector where the i'th
        entry corresponds to the total TF-IDF score of the text fragment
        for concept i"""

        # Remove mess (quotes, parentheses etc) from text
        text = self.clean(text)

        # Convert string to hash like {'word' : no. of occurrences}
        countmap = Counter(text.split()).items()

        # Interpretation vector to be returned
        result = sps.csr_matrix((1, self.n_concepts), dtype=float)

        # Add word count in the correct position of the vector
        for word, count in countmap:
            try:
                ind = self.word2index[word]
                # Which file to look in
                file_number = int(ind / row_chunk_size)
                filename = os.path.join(self.matrix_path, str(file_number) + extensions['matrix'])

                # And which row to extract
                row_number = ind % row_chunk_size

                if filename in self.__cache.keys():
                    temp, _ = self.__cache[filename]
                    # Least recently used cache strategy
                    self.__cache[filename] = (temp, 0)
                else:
                    with open(filename, 'r') as f:
                        temp = shared.mload(f)
                        self.__cache[filename] = (temp, 0)
                        if len(self.__cache) >= self.__max_cache_size:
                            # Get key [0] of value [1] with oldest age [1]
                            oldest = max(self.__cache.items(), key=lambda p: p[1][1])[0]
                            del self.__cache[oldest]

                result = result + count * temp.getrow(row_number)

            except KeyError:
                pass  # No data on this word -> discard

        # Done. Return row vector as a 1x#concepts CSR matrix
        return result


    def interpret_text(self, text, display_concepts=10):
        '''Attempts to guess the core concepts of the given text fragment'''
        # Compute the interpretation vector for the text fragment
        vec = self.interpretation_vector(text)

        # Magic, don't touch
        top_n = vec.data.argsort()[:len(vec.data) - 1 - display_concepts:-1]

        # List top scoring concepts and their TD-IDF
        concepts = [self.index2concept[vec.indices[i]] for i in top_n]
        return concepts


    def interpret_file(self, filename):
        with open(filename, 'r') as f:
            data = self.clean(f.read())
        return self.interpret_text(data)


    def interpret_input(self):
        text = input("Enter text fragment: ")
        topics = self.interpret_text(text)
        print("Based on your input, the most probable topics of your text are:")
        print(topics)


    def scalar(self, v1, v2):
        # Compute their inner product and make sure it's a scalar
        dot = v1.dot(v2.transpose())
        assert dot.shape == (1, 1)

        if dot.data:
            scal = dot.data[0]
        else:
            scal = 0  # Empty sparse matrix means zero

        eps = 1e-8

        # Normalize and return
        sim = scal / (norm(v1.data) * norm(v2.data) + eps)
        return sim


    def cosine_similarity(self, text1, text2):
        """Determines cosine similarity between input texts.
        Returns float in [0,1]"""

        # Determine intepretation vectors
        v1 = self.interpretation_vector(text1)
        v2 = self.interpretation_vector(text2)

        # Compute the normalized dot product and return
        return self.scalar(v1, v2)


    def cosine_distance(self, text1, text2):
        return 1 - self.cosine_similarity(text1, text2)
