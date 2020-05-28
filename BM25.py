import os
import numpy as np
from numpy import dot
from numpy.linalg import norm
import operator
import math
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
averdoclen = 0
k1 = 3.5
k3 = 3.75
b = 0.75
def tf(dic, wordlist):           #type dictionay list
    for i in range(len(wordlist)):
        for key in dic[i]:
            counter = 0
            counter = wordlist[i].count(key)
            dic[i][key] = counter
def qtfidf(list, idfvec):
    for i in range(len(list)):
        for key in list[i]:
            list[i][key] = (((k3 + 1)*list[i][key])/(k3 + list[i][key])) * (math.log((2281 - idfvec[key] + 0.5) / (idfvec[key] + 0.5), 10))
def doctfnorm(list):
    for i in range(len(list)):
        for key in list[i]:
            list[i][key] = ((k1 + 1)*list[i][key])/(k1*((1-b) + (b*len(list[i]))/averdoclen) + list[i][key])
def deletion(vec):
    temp = vec.replace('-1\n','')
    return temp
def sim(q,d):
    res = 0
    for keys in q:
        if d.__contains__(keys):
            res += q[keys]*d[keys]
    return res
totalstr = []
idf = {}
for dirPath, dirNames, fileNames in os.walk(r"C:\Users\承翰\Desktop\Assignment\NTUST\Information Retrieval and Applications\HW2\Query"):
    strlistq = []
    querytitle = []
    query = []
    dict = {}
    for f in fileNames:         #incorporate all queries into a list
            fp = open(r'C:\Users\承翰\Desktop\Assignment\NTUST\Information Retrieval and Applications\HW2\Query\{0}'.format(f),'r' )
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
for dirPath, dirNames, fileNames in os.walk(r"C:\Users\承翰\Desktop\Assignment\NTUST\Information Retrieval and Applications\HW2\Document"):
    strlistd = []
    doc = []
    dict = {}
    doctitle = []
    for f in fileNames:
        fp = open(r'C:\Users\承翰\Desktop\Assignment\NTUST\Information Retrieval and Applications\HW2\Document\{0}'.format(f), 'r')
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
doclen = 0
for i in strlistd:
    doclen += len(i)
averdoclen = doclen/2281
tf(query, strlistq)
tf(doc, strlistd)
qtfidf(query, idf)
doctfnorm(doc)
fp = open(r'C:\Users\承翰\Desktop\Assignment\NTUST\Information Retrieval and Applications\HW2\Submission.txt', 'a')
fp.write('Query,RetrievedDocuments\n')
for i in range(len(query)):
    result = []
    fp.write(querytitle[i] + ',')
    for j in range(len(doc)):
        result.append(sim(query[i], doc[j]))
    final = list(zip(result, doctitle))
    output = sorted(final, key=lambda x:x[0], reverse=True)
    for z in range(len(output)):
        fp.write(output[z][1]+' ')
    fp.write('\n')
fp.close()


import os
import numpy as np
from numba import jit

