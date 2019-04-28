import nltk#the variable corpus is the training set
import re
import io
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
import copy
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import unicodecsv as csv
import codecs
seconds = time.time()
predictors = []
item_profiles = []
count = 0
def find_his(user,index,movie_vectors):#extracts user history vectors
    tmp_count = copy.deepcopy(index)
    user_his = []
    for i in range(len(movie_vectors)):
       
        if(user == movie_vectors[tmp_count][0]):
           
            user_his.append(movie_vectors[tmp_count])
            tmp_count+=1
        else:
            #tmp_count+=1
            break
    return [user_his,tmp_count]#tmp count is a "boolmark" for where to start the search within the movie_vectors again 
#def predict_rate(item_profiles,user_his):
    #https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html read about kneighbors, the goal is to get k (sqrt(len(user_his))) neighbors and average their rating to make the predictions 

with open('test.dat') as test:#parses testig data into a list of lists with userID at index 0 and movieID at index 1 
    test_read = csv.reader(test,delimiter = ' ')
    for row in test:
        id = re.sub('[^A-Za-z0-9.]+',' ',str(row)).split(" ")
        del id[2] 
        predictors.append(id)#the numbers are strings
        count+=1
        if(count == 102):
            break
#parse utility matrix
movie_vectors = []
with open('utilityMatrixFinal.csv') as util:#parses for utility matrix vectors
    util_read = csv.reader(util)
    bool = 0
    #print(len(util_read))
    
    for row in util_read:
        if(bool !=0):
            movie_vectors.append(row)
            
            
        else:
            bool+=1
del predictors[0]
with open('itemProfile.csv') as items:#parses for item profile vectors
    items_read = csv.reader(items)
    bool = 0
    #print(len(util_read))
    
    for row in items_read:
        if(bool !=0):
            item_profiles.append(row)
            
            
        else:
            bool+=1

#del predictors[0]
curr_user = copy.deepcopy(predictors[0][0])
tmp_user_his = []
index = 0
tmp = []

tmp = find_his(curr_user,index,movie_vectors)
tmp_user_his = tmp[0]
index = tmp[1]#user history is gathered for predictor function
for i in predictors:
    
    if(i[0] != curr_user):#if
        tmp = find_his(curr_user,index,movie_vectors)#user histor vectors still have the first three elements as the userID, movieID, and rating keethis in mind when finishing the predictor function
        tmp_user_his = tmp[0]
        index = tmp[1]
        curr_user = copy.deepcopy(i[0])
        #predictor function goes here
    #here aswell with an else statemennt
   
    break   
#print(movie_vectors[index][0])
#print(len(tmp_user_his))
print("finished:")
print("time taken %f" % (time.time() - seconds))