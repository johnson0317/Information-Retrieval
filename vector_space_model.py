import os
import numpy as np
from numpy import dot
from numpy.linalg import norm
import operator
import math
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
def tf(dic, wordlist):           #type dictionay list
    for i in range(len(wordlist)):
        for key in dic[i]:
            counter = 0
            counter = wordlist[i].count(key)
            dic[i][key] = counter
def tfidf(list, idfvec):
    for i in range(len(list)):
        for key in list[i]:
            list[i][key] *= math.log(2265 / idfvec[key], 10)
def deletion(vec):
    temp = vec.replace('-1\n','')
    return temp
def cossim(q,d):
    innerproduct = 0
    for keys in q:
        if d.__contains__(keys):
            innerproduct += q[keys]*d[keys]
    return innerproduct/(len(q)*len(d))
totalstr = []
idf = {}
for dirPath, dirNames, fileNames in os.walk(r"C:\Users\承翰\Desktop\Assignment\NTUST\Information Retrieval and Applications\VSM_HW1\Data_1\Query"):
    strlistq = []
    querytitle = []
    query = []
    dict = {}
    for f in fileNames:         #incorporate all queries into a list
            fp = open(r'C:\Users\承翰\Desktop\Assignment\NTUST\Information Retrieval and Applications\VSM_HW1\Data_1\Query\{0}'.format(f),'r' )
            file = fp.read()
            temp = deletion(file)
            totalstr.append(temp)
            strlistq.append(temp.split())
            dict = {i:0 for i in temp.split()}
            for i in list(dict.fromkeys(temp.split())):
                if idf.__contains__(i):
                    idf[i] = idf[i] + 1
                else:
                    d = {i : 1}
                    idf.update(d)
            query.append(dict)
            querytitle.append(f)
            fp.close()
for dirPath, dirNames, fileNames in os.walk(r"C:\Users\承翰\Desktop\Assignment\NTUST\Information Retrieval and Applications\VSM_HW1\Data_1\Document"):
    strlistd = []
    doc = []
    dict = {}
    doctitle = []
    for f in fileNames:
        fp = open(r'C:\Users\承翰\Desktop\Assignment\NTUST\Information Retrieval and Applications\VSM_HW1\Data_1\Document\{0}'.format(f), 'r')
        file = fp.read()
        temp = deletion(file[71:])
        totalstr.append(temp)
        strlistd.append(temp.split())
        dict = {i : 0 for i in deletion(file[71:]).split()}
        for i in list(dict.fromkeys(temp.split())):
            if idf.__contains__(i):
                idf[i] = idf[i] + 1
            else:
                d = {i: 1}
                idf.update(d)
        doc.append(dict)
        doctitle.append(f)
        fp.close()

tf(query, strlistq)
tf(doc, strlistd)
tfidf(query, idf)
tfidf(doc, idf)
fp = open(r'C:\Users\承翰\Desktop\Assignment\NTUST\Information Retrieval and Applications\VSM_HW1\Submission.txt', 'a')
fp.write('Query,RetrievedDocuments\n')
for i in range(len(query)):
    result = []
    fp.write(querytitle[i] + ',')
    for j in range(len(doc)):
        result.append(cossim(query[i], doc[j]))
    final = list(zip(result, doctitle))
    output = sorted(final, key=lambda x:x[0], reverse=True)
    for z in range(len(output)):
        fp.write(output[z][1]+' ')
    fp.write('\n')
fp.close()
