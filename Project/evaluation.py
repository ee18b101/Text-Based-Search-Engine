from util import *

# Add your import statements here
import math

class Evaluation():
                                                        
    def queryPrecision(self, query_doc_IDs_ordered, query_id, true_doc_IDs, k):
        """
        Computation of precision of the Information Retrieval System
        at a given value of k for a single query
        
        Parameters
        ----------
        arg1 : list
            A list of integers denoting the IDs of documents in
            their predicted order of relevance to a query
        arg2 : int
            The ID of the query in question
        arg3 : list
            The list of IDs of documents relevant to the query (ground truth)
        arg4 : int
            The k value

        Returns
        -------
        float
            The precision value as a number between 0 and 1
        """
        precision =-1
        #Fill in code here
        retrieved = 0
        rel = 0
        for docID in query_doc_IDs_ordered:
            retrieved+= 1
            if docID in true_doc_IDs:
                rel += 1
            
            if retrieved == k:
                break
        
        precision = (rel/retrieved)
        # print(query_id, precision)
        return precision


    def meanPrecision(self, doc_IDs_ordered, query_ids, qrels, k):
        """
        Computation of precision of the Information Retrieval System
        at a given value of k, averaged over all the queries

        Parameters
        ----------
        arg1 : list
            A list of lists of integers where the ith sub-list is a list of IDs
            of documents in their predicted order of relevance to the ith query
        arg2 : list
            A list of IDs of the queries for which the documents are ordered
        arg3 : list
            A list of dictionaries containing document-relevance
            judgements - Refer cran_qrels.json for the structure of each
            dictionary
        arg4 : int
            The k value

        Returns
        -------
        float
            The mean precision value as a number between 0 and 1
        """
        meanPrecision = -1
        #Fill in code here
        
        prec_sum  = 0
        count = 0
        for i,query_doc_IDs_ordered in enumerate(doc_IDs_ordered):
            
            true_doc_IDs = []
            
            while int(qrels[count]["query_num"]) == query_ids[i]:
                true_doc_IDs.append(int(qrels[count]["id"]))
                count += 1
                if count == len(qrels):
                    break
                
            prec = self.queryPrecision(query_doc_IDs_ordered, query_ids[i], true_doc_IDs, k)
            prec_sum += prec
        
        meanPrecision = prec_sum/len(query_ids)
        
        return meanPrecision

    
    def queryRecall(self, query_doc_IDs_ordered, query_id, true_doc_IDs, k):
        """
        Computation of recall of the Information Retrieval System
        at a given value of k for a single query

        Parameters
        ----------
        arg1 : list
            A list of integers denoting the IDs of documents in
            their predicted order of relevance to a query
        arg2 : int
            The ID of the query in question
        arg3 : list
            The list of IDs of documents relevant to the query (ground truth)
        arg4 : int
            The k value

        Returns
        -------
        float
            The recall value as a number between 0 and 1
        """

        recall = -1
        
        #Fill in code here
        retr_relevant = 0
        retr = 0
        relevant = len(true_doc_IDs)
        
        for docID in query_doc_IDs_ordered:
            retr +=1
            if docID in true_doc_IDs:
                retr_relevant +=1
            if retr == k:
                break    
        
        recall = (retr_relevant/relevant)
        
        
        
        return recall


    def meanRecall(self, doc_IDs_ordered, query_ids, qrels, k):
        """
        Computation of recall of the Information Retrieval System
        at a given value of k, averaged over all the queries

        Parameters
        ----------
        arg1 : list
            A list of lists of integers where the ith sub-list is a list of IDs
            of documents in their predicted order of relevance to the ith query
        arg2 : list
            A list of IDs of the queries for which the documents are ordered
        arg3 : list
            A list of dictionaries containing document-relevance
            judgements - Refer cran_qrels.json for the structure of each
            dictionary
        arg4 : int
            The k value

        Returns
        -------
        float
            The mean recall value as a number between 0 and 1
        """

        meanRecall = -1
        #Fill in code here
        
        recall_sum  = 0
        count = 0
        for i,query_doc_IDs_ordered in enumerate(doc_IDs_ordered):
            
            true_doc_IDs = []
            while int(qrels[count]["query_num"]) == query_ids[i]:
                true_doc_IDs.append(int(qrels[count]["id"]))
                count += 1
                
                if count == len(qrels):
                    break
                
            rec = self.queryRecall(query_doc_IDs_ordered, query_ids[i], true_doc_IDs, k)
            recall_sum += rec
        
        meanRecall = recall_sum/len(query_ids)
        
        return meanRecall

    def queryFscore(self, query_doc_IDs_ordered, query_id, true_doc_IDs, k):
        """
        Computation of fscore of the Information Retrieval System
        at a given value of k for a single query

        Parameters
        ----------
        arg1 : list
            A list of integers denoting the IDs of documents in
            their predicted order of relevance to a query
        arg2 : int
            The ID of the query in question
        arg3 : list
            The list of IDs of documents relevant to the query (ground truth)
        arg4 : int
            The k value

        Returns
        -------
        float
            The fscore value as a number between 0 and 1
        """

        fscore = -1

        #Fill in code here
        alpha = 0.5
        
        pr = self.queryPrecision(query_doc_IDs_ordered, query_id, true_doc_IDs, k)
        re = self.queryRecall(query_doc_IDs_ordered, query_id, true_doc_IDs, k)
        
        if re == 0 or pr == 0:
            fscore = 0
        else:    
            fscore = 1/(alpha*(1/pr)+(1-alpha)*(1/re))
        
        return fscore


    def meanFscore(self, doc_IDs_ordered, query_ids, qrels, k):
        """
        Computation of fscore of the Information Retrieval System
        at a given value of k, averaged over all the queries

        Parameters
        ----------
        arg1 : list
            A list of lists of integers where the ith sub-list is a list of IDs
            of documents in their predicted order of relevance to the ith query
        arg2 : list
            A list of IDs of the queries for which the documents are ordered
        arg3 : list
            A list of dictionaries containing document-relevance
            judgements - Refer cran_qrels.json for the structure of each
            dictionary
        arg4 : int
            The k value
        
        Returns
        -------
        float
            The mean fscore value as a number between 0 and 1
        """
       
        meanFscore = -1

        #Fill in code here
     
        
        fscore_sum  = 0
        count = 0
        for i,query_doc_IDs_ordered in enumerate(doc_IDs_ordered):
            
            true_doc_IDs = []
            while int(qrels[count]["query_num"]) == query_ids[i]:
                true_doc_IDs.append(int(qrels[count]["id"]))
                count += 1
                
                if count == len(qrels):
                    break
                
            fsc = self.queryFscore(query_doc_IDs_ordered, query_ids[i], true_doc_IDs, k)
            fscore_sum += fsc
        
        meanFscore = fscore_sum/len(query_ids)
        
        return meanFscore
        
        
    

    def queryNDCG(self, query_doc_IDs_ordered, query_id, true_doc_IDs, k):
        """
        Computation of nDCG of the Information Retrieval System
        at given value of k for a single query

        Parameters
        ----------
        arg1 : list
            A list of integers denoting the IDs of documents in
            their predicted order of relevance to a query
        arg2 : int
            The ID of the query in question
        arg3 : list
            The list of IDs of documents relevant to the query (ground truth)
        arg4 : int
            The k value

        Returns
        -------
        float
            The nDCG value as a number between 0 and 1
        """

        nDCG = -1

        #Fill in code here
        relevance = list(range(k))
        true_doc_IDs_proxy = [x for x,_ in true_doc_IDs]
        true_relevance_proxy = [y for _,y in true_doc_IDs]

        for i,docID in enumerate(query_doc_IDs_ordered):
            try:
                index = true_doc_IDs_proxy.index(docID)
                relevance[i] = true_relevance_proxy[index]
            except:
                relevance[i] = 0
            # if docID in true_doc_IDs_proxy:
            #     relevance[i] = 1
            # else:
            #     relevance[i] = 0
            
            if i == k-1:
                break
                
        DCG  = 0
        
        for i,rel in enumerate(relevance):
            DCG += rel/math.log((i+1+1),2)   
        
        IDCG = 0  # Ideal DCG which is calculated with relevance array sorted 
        relevance_sort = list(sorted(relevance, reverse=True))
        
        for i,rel in enumerate(relevance_sort):
            if rel == 0:
                break
            IDCG += rel/math.log((i+1+1),2) 
        
        if DCG == 0:
            nDCG = 0
        else: nDCG = DCG/IDCG
        ''''''
        
        return nDCG


    def meanNDCG(self, doc_IDs_ordered, query_ids, qrels, k):
        """
        Computation of nDCG of the Information Retrieval System
        at a given value of k, averaged over all the queries

        Parameters
        ----------
        arg1 : list
            A list of lists of integers where the ith sub-list is a list of IDs
            of documents in their predicted order of relevance to the ith query
        arg2 : list
            A list of IDs of the queries for which the documents are ordered
        arg3 : list
            A list of dictionaries containing document-relevance
            judgements - Refer cran_qrels.json for the structure of each
            dictionary
        arg4 : int
            The k value

        Returns
        -------
        float
            The mean nDCG value as a number between 0 and 1
        """

        meanNDCG = -1

        #Fill in code here
        NDCG_sum  = 0
        count = 0
        for i,query_doc_IDs_ordered in enumerate(doc_IDs_ordered):
            
            true_doc_IDs = []
            
            while int(qrels[count]["query_num"]) == query_ids[i]:
                true_doc_IDs.append((int(qrels[count]["id"]), 5-int(qrels[count]["position"])))
                count += 1
                if count == len(qrels):
                    break
                
            nDCG = self.queryNDCG(query_doc_IDs_ordered, query_ids[i], true_doc_IDs, k)
            NDCG_sum += nDCG
        
        meanNDCG = NDCG_sum/len(query_ids)
        return meanNDCG


    def queryAveragePrecision(self, query_doc_IDs_ordered, query_id, true_doc_IDs, k):
        """
        Computation of average precision of the Information Retrieval System
        at a given value of k for a single query (the average of precision@i
        values for i such that the ith document is truly relevant)

        Parameters
        ----------
        arg1 : list
            A list of integers denoting the IDs of documents in
            their predicted order of relevance to a query
        arg2 : int
            The ID of the query in question
        arg3 : list
            The list of documents relevant to the query (ground truth)
        arg4 : int
            The k value

        Returns
        -------
        float
            The average precision value as a number between 0 and 1
        """
        
        avgPrecision = -1

        #Fill in code here
        retrieved = 0
        rel = 0
        pr = []
        
        for docID in query_doc_IDs_ordered:
            retrieved+= 1
            
            if docID in true_doc_IDs:
                rel += 1
                pr.append(rel/retrieved)
            
            if retrieved == k:                                       
                break
            
        if rel == 0:
            avgPrecision = 0
        else:    
            avgPrecision = sum(pr)/rel     
        
        return avgPrecision
        

    def meanAveragePrecision(self, doc_IDs_ordered, query_ids, qrels, k):
        """
        Computation of MAP of the Information Retrieval System
        at given value of k, averaged over all the queries

        Parameters
        ----------
        arg1 : list
            A list of lists of integers where the ith sub-list is a list of IDs
            of documents in their predicted order of relevance to the ith query
        arg2 : list
            A list of IDs of the queries
        arg3 : list
            A list of dictionaries containing document-relevance
            judgements - Refer cran_qrels.json for the structure of each
            dictionary
        arg4 : int
            The k value

        Returns
        -------
        float
            The MAP value as a number between 0 and 1
        """

        meanAveragePrecision = -1

        #Fill in code here
        AP_sum  = 0
        count = 0
        for i,query_doc_IDs_ordered in enumerate(doc_IDs_ordered):
            
            true_doc_IDs = []
            
            while int(qrels[count]["query_num"]) == query_ids[i]:
                true_doc_IDs.append(int(qrels[count]["id"]))
                count += 1
                if count == len(qrels):
                    break
                
            avg_prec = self.queryAveragePrecision(query_doc_IDs_ordered, query_ids[i], true_doc_IDs, k)
            AP_sum += avg_prec
        
        meanAveragePrecision = AP_sum/len(query_ids)
        
        return meanAveragePrecision

