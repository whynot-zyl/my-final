from snownlp import SnowNLP
import codecs
import os
import matplotlib.pyplot as plt
import numpy as np

def anlyse():
    source = open("comments.txt","r", encoding='utf-8')
    line = source.readlines()
    sentimentslist = []
    for i in line:
        s = SnowNLP(i)
        #print(s.sentiments)
        sentimentslist.append(s.sentiments)
    plt.hist(sentimentslist, bins = np.arange(0, 1, 0.01), facecolor = 'g')
    plt.xlabel('Sentiments Probability')
    plt.ylabel('Quantity')
    plt.title('Analysis of Sentiments')
    plt.show()
