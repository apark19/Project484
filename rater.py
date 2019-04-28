#import nltk#the variable corpus is the training set
import re
import io
import numpy as np
import sklearn
import math
from scipy import sparse
from operator import itemgetter
from multiprocessing import Process,Lock,Pool,freeze_support
import time
import pandas as pd
import copy
from sklearn.neighbors import NearestNeighbors
import csv
seconds = time.time()
predictors = []
item_profiles = []
count = 0
def find_his(user,index,movie_vectors):#extracts user history vectors
    tmp_count = copy.deepcopy(index)
    user_his = []
    for i in range(len(movie_vectors)):
        #print("user",user)
        #print("movie",movie_vectors[tmp_count])
        if(user == movie_vectors[tmp_count][0]):
           
            user_his.append(movie_vectors[tmp_count])
            tmp_count+=1
        else:
            #tmp_count+=1
            break
    return [user_his,tmp_count]#tmp count is a "boolmark" for where to start the search within the movie_vectors again
def find_movie(movie,item_profiles):
    ret = []
    for i in item_profiles:
        print(movie)
        if(movie == i[0]):
            ret = copy.deepcopy(i)
            break
    print(ret)
    del ret[0]
    return ret
def predict_rate(user_his,curr_user):
    print("begin rating")
    K = int(math.sqrt(len(user_his)))
    movie_cpy = copy.deepcopy(user_his)
    for i in movie_cpy:
        for i in range(3):
            del movie_cpy[i]
    
    pred = find_movie(curr_user[1],item_profiles)
    print(pred)
    for i in range(3):
            del pred[i]
    knn = NearestNeighbors(k_neighbors = K)
    knn.fit(movie_cpy)
    neighbors = knn.kneighbors([pred],return_distance=False).tolist()
    rating = 0
    for i in neighbors:
        rating += int(movie_cpy[i[0]][2])
    rating = rating/len(neighbors)
    print(rating)

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
with open('utilityMatrixFinal.csv',encoding = 'utf-8') as util:#parses for utility matrix vectors
    util_read = csv.reader(util)
    bool = 0
    
    #print(len(util_read))
    
    for row in util_read:
        #print(row)
        if(bool !=0):
            movie_vectors.append(row)
            
            
        else:
            bool+=1
del predictors[0]
b = 0
item_profiles = (row for row in csv.reader(open('itemProfile1.csv',encoding = 'utf-8')))
item_profiles = list(item_profiles)
del item_profiles[0]

"""
with open('itemProfile1.csv',encoding = 'utf-8') as items:#parses for item profile vectors
    items_read = csv.reader(items)
    bool = 0
    #print(len(util_read))
    item_profiles = (row for row in csv.reader(open('itemProfile1.csv',encoding = 'utf-8')))
    for row in items_read:
        if(bool !=0):
            item_profiles.append(row)
           
            
        else:
            bool+=1
"""
#del predictors[0]
curr_user = copy.deepcopy(predictors[0][0])
curr_user_vec = copy.deepcopy(predictors[0])
tmp_user_his = []
index = 0
tmp = []

tmp = find_his(curr_user,index,movie_vectors)
tmp_user_his = tmp[0]
index = tmp[1]#user history is gathered for predictor function
#print(movie_vectors)
for i in predictors:
    
    if(i[0] != curr_user):#if
        tmp = find_his(curr_user,index,movie_vectors)#user histor vectors still have the first three elements as the userID, movieID, and rating keethis in mind when finishing the predictor function
        tmp_user_his = tmp[0]
        index = tmp[1]
        curr_user = copy.deepcopy(i[0])
        curr_user_vec = copy.deepcopy(i)
        predict_rate(tmp_user_his,curr_user_vec)
        #predictor function goes here
    else:
       predict_rate(tmp_user_his,curr_user_vec) 
    #here aswell with an else statemennt
   
    break   
#print(movie_vectors[index][0])
#print(len(tmp_user_his))
print("finished:")
print("time taken %f" % (time.time() - seconds))
