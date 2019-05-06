import nltk#creates csv file with parsed genres
import re
import numpy as np
import sklearn
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse
from operator import itemgetter
from multiprocessing import Process,Lock,Pool,freeze_support
import time
from nltk import pos_tag
import pandas as pd
import copy
from nltk.corpus import stopwords
from functools import partial
from nltk.stem import WordNetLemmatizer

from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from sklearn.ensemble import BaggingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from scipy import sparse
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import f1_score
import codecs
import csv
lem = WordNetLemmatizer()
stpwrd = set(stopwords.words('english'))
stpwrd_update = ["br","eof","i","im","i'm",",","it","as","the","this","but","its","it's","you" "also","for","us","was","to","on","there","of","in","his","hers","-"]
stpwrd.update(stpwrd_update)
#DT = DecisionTreeClassifier()
vec = TfidfVectorizer()
def Pre(par):
    #par = list(par)
    
    paragraph = par.lower()#the plots are in the third element of the array. lower is used so that words will still be considered the same instance when vectorized
    #print(paragraph)
    paragraph = re.sub('[^+A-Za-z0-9]+',' ',paragraph)#substittes non alphabetic or numerical charectars with a space
    #print(paragraph)
    paragraph = re.split(' ',paragraph)#issue mostly fixed (not planning getting it perfect as most noise is reduced), sentence difference can be seen in the print statements in main
    #print(paragraph)
    new_paragraph = []
    pos_keep = ['JJ','JJR','JJR','JJS','RB','RBR','RBS','VB','VBD','VBG','VBN','VBP','VBZ']# all desired parts of speech  (all forms of verbs, adhectives etc. no subject)
	
	
    if('' in paragraph):#removes any empty charectar within a passed paragrph that may be left over
        while('' in paragraph):
	        paragraph.remove('')
	
    	
    paragraph = nltk.pos_tag(paragraph)#returns tuples with each word paired with parts of speech keyword https://medium.com/@gianpaul.r/tokenization-and-parts-of-speech-pos-tagging-in-pythons-nltk-library-2d30f70af13b
    #print(paragraph)#the above link shows the keys for the nltk parts of speech
    #print(paragraph)
    new_paragraph = [word[0] for word in paragraph if((word[0] not in stpwrd) and (word[1] in pos_keep))]#the firs condition is uneccesary if the second works properly
	
	
    
    new_paragraph= " ".join(new_paragraph)
    
	#once the issue is fixed, I would like to see if lemmatization could be implemented while maintainig reasonable runtime https://www.geeksforgeeks.org/python-lemmatization-with-nltk/ 	
	
    return new_paragraph
def boost(x_data,y_label,p,g_truth):
    ada = AdaBoostClassifier(n_estimators = 1000)
    ada.fit(x_data,y_label)
    pred  = ada.predict(p)
    score = f1_score(g_truth,pred, average='weighted')  
    print(pred)
    print(score)
def vectorize(data):
    vec = TfidfVectorizer()
    vector_data  = vec.fit_transform(data)
    return vector_data
if __name__ == "__main__":
    seconds = time.time()
    p = Pool(4)
    """
     with codecs.open('training_data(movies).csv','r','utf-8') as x_data:
        with codecs.open('movies_2020.csv','r','utf-8') as test:
            with codecs.open('prediction_dtree.dat','w','utf-8') as predictions:
                pd.read_csv()
    """
    train = pd.read_csv('training_data(movies).csv',index_col = 0)
    test = pd.read_csv('movies_2020.csv',index_col = 0)
    train_x = [row for row in train['plot']]
    train_y = np.array([row for row in train['genre']])
    train_x = np.array(train_x)
    test_x = [ row  for row in test['description']]
    g_truth = [ row.lower()  for row in test['genre']]
   
    test_x = np.array(list(p.map(Pre,test_x)))
    training = vec.fit_transform(train_x)
    testing = vec.transform(test_x)
    print(training.shape)
    print(testing.shape)
    boost(training,train_y,testing,g_truth)
    
    #print(test_x)
    #exit()
    print("finished:")
    print("time taken %f" % (time.time() - seconds))
    
    