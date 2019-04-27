import nltk#the variable corpus is the training set
import re
import numpy as np
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse
from operator import itemgetter
from multiprocessing import Process,Lock,Pool,freeze_support
import time
from nltk import pos_tag
import pandas as pd
from nltk.corpus import stopwords

from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import csv
directorFrame = pd.read_csv('movie_directors.dat', encoding='ISO-8859-1', sep='\t', usecols=['movieID', 'directorID', 'directorName'])
actorFrame = pd.read_csv('movie_actors.dat', encoding='ISO-8859-1', sep='\t', usecols=['movieID', 'actorID', 'actorName', 'ranking'])
genreFrame = pd.read_csv('movie_genres.dat', sep='\t', usecols=['movieID', 'genre'])
trainFrame = pd.read_csv('train.dat', sep=' ', encoding='ISO-8859-1', usecols=['movieID'])
mID = trainFrame['movieID'].tolist()
print(mID[0])
header = []
def key_pair(Frame, Frame1, Frame2):
    keyidg = Frame['movieID'].tolist()
    key_genre = Frame['genre'].tolist()
    keyidd = Frame1['movieID'].tolist()
    key_director = Frame1['directorName'].tolist()
    keyida = Frame2['movieID'].tolist()
    key_actor = Frame2['actorName'].tolist()

    frame_pair_genre = [[int(keyidg[i]), key_genre[i]] for i in range(len(keyidg))]
    frame_pair_director = [[int(keyidd[i]), key_director[i]] for i in range(len(keyidd))]
    frame_pair_actor = [[int(keyida[i]), key_actor[i]] for i in range(len(keyida))]
    return [frame_pair_actor, frame_pair_director, frame_pair_genre]


def search_pair(id,frame):
    attributes = []
    for i in frame[2]:
        if(i[0] == id):
            attributes.append(i[1])
    for i in frame[1]:
        if(i[0] == id):
            attributes.append(i[1])
    for i in frame[0]:
        if(i[0] == id):
            attributes.append(i[1])
    return attributes

with open("utility.csv","rb") as ut,open("test.csv","wb") as out:
    frame  = key_pair(genreFrame,directorFrame,actorFrame)
    movie_vectors = csv.reader(ut,delimiter = ',')
    outer = csv.writer(out)
    i = 0
    for row in movie_vectors:
        if(i!=0):
            print(row)
        else:
            header = list(row)
            print()
            break
    counter_row = -1
    #print(header)
    count_bool = 0
    for row in movie_vectors:
        row_list = []
        
        counter_row +=1
        print(counter_row)
        movieID = mID[counter_row]
        print(movieID)
        attributes = search_pair(movieID,frame)
        print("attributes",attributes)
        for col in row:
            counter_col = 0
            print(header[0])
            if(count_bool == 0):
                count_bool+=1
           
            else:
                bool = True
                print("header length",len(header))
                tmp = header[counter_col]
                print(tmp)
                if( tmp in attributes):
                    row_list.append('1')
                else:
                    row_list.append('0')
            counter_col += 1
        #print(row_list)
        outer.writerow(row_list)
        break
    