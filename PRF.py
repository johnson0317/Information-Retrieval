import os
import numpy as np
from numpy import dot
from numpy.linalg import norm
import operator
import math
from collections import defaultdict
alpha = 0.8
beta = 0.4
gama = 0.4
q_dir = r'Query/'
doc_dir = r'Document/'
ret_num = 30
def cossim(q,d):
    innerproduct = 0
    q_norm = 0
    d_norm = 0
    for key in d:
        d_norm += d[key]**2
    for keys in q:
        q_norm += q[keys]**2
        if d.__contains__(keys):
            innerproduct += q[keys]*d[keys]
    return innerproduct/((q_norm * d_norm)**(1/2))
def get_tf(documents):
    count_dict = []
    for d_index, doc in enumerate(documents):
        temp = defaultdict(int)
        for key in doc:
            temp[key] += 1
        count_dict.append(temp)
    return count_dict
def tfidf(documents, idf):
    for doc_index, doc in enumerate(documents):
        for key in doc.keys():
            documents[doc_index][key] = documents[doc_index][key] * math.log((2265 / idf[key]) , 10)
def first_retrieval(query, docs):
    result = []
    doc_num = []
    temp = []
    rel_doc = defaultdict(int)
    unrel_doc = defaultdict(int)
    newq = defaultdict(int)
    for j, doc in enumerate(docs):
        result.append(cossim(query, docs[j]))
        doc_num.append(j)
    final = zip(result, doc_num)
    output = sorted(final, key=lambda x: x[0], reverse=True)
    for sim, doc_index in output[:ret_num]:
        for key in docs[doc_index]:
            rel_doc[key] += docs[doc_index][key]
    temp.append(rel_doc.keys())
    for sim, doc_index in output[ret_num:]:
        for key in docs[doc_index]:
            unrel_doc[key] += docs[doc_index][key]
    temp.append(unrel_doc.keys())
    all_keys = set(temp[0])
    for key in all_keys:
        newq[key] = alpha * query[key] + beta * (1 / ret_num) * rel_doc[key] - (gama / (2265 - ret_num)) * unrel_doc[key]

    return newq
wordlist = []
q_list = os.listdir(q_dir)
queries = []
query_title = []
idf = defaultdict(int)
for q_name in q_list:
    q_path = q_dir + q_name
    query_title.append(q_name)
    with open(q_path, mode='r') as file:
        temp = file.read()
        queries.append(temp.replace('-1', '').split())
        for keys in set(temp.replace('-1', '').split()):
            idf[keys] += 1

doc_list = os.listdir(doc_dir)
documents = []
doc_title = []
doc_length = []
for doc_name in doc_list:
    doc_title.append(doc_name)
    doc_path = doc_dir + doc_name
    with open(doc_path, mode='r') as file:
        temp = file.read()
        documents.append(temp[71:].replace('-1', '').split())
        doc_length.append(len(temp[71:].replace('-1', '').split()))
        for keys in set(temp[71:].replace('-1', '').split()):
            idf[keys] += 1

query_tf = get_tf(queries)
doc_tf = get_tf(documents)
tfidf(query_tf, idf)
tfidf(doc_tf, idf)
fp = open(r'C:\Users\johnson_chou\Desktop\Information Retrieval\Submission.txt', 'a')
fp.write('Query,RetrievedDocuments\n')
for q_index, query in enumerate(query_tf):
    new_query = first_retrieval(query, doc_tf)
    result = []
    fp.write(query_title[q_index] + ',')
    for j in range(len(doc_tf)):
        result.append(cossim(new_query, doc_tf[j]))
    final = list(zip(result, doc_title))
    output = sorted(final, key=lambda x: x[0], reverse=True)
    for z in range(50):
        fp.write(output[z][1] + ' ')
    fp.write('\n')
fp.close()
