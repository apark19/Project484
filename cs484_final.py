import nltk#the variable corpus is the training set
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

from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

stpwrd = set(stopwords.words('english'))
stpwrd_update = ["br","eof","i","im","i'm",",","it","as","the","this","but","its","it's","you" "also","for","us","was","to","on","there","of","in","his","hers","-"]
stpwrd.update(stpwrd_update)
lemmatizer = nltk.stem.WordNetLemmatizer
def Pre(par):
    #par = list(par)
    
    paragraph = par[0].lower()#the plots are in the third element of the array. lower is used so that words will still be considered the same instance when vectorized
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
    new_paragraph = [word[0] for word in paragraph if((word[0] not in stpwrd) and (word[1] in pos_keep))]#the firs condition is uneccesary if the second works properly
	
	
    
    new_paragraph= " ".join(new_paragraph)
    
	#once the issue is fixed, I would like to see if lemmatization could be implemented while maintainig reasonable runtime https://www.geeksforgeeks.org/python-lemmatization-with-nltk/ 	
	
    return new_paragraph
if __name__ == "__main__":
    p = Pool(4)
    seconds = time.time()
    x_tittles = pd.read_csv("movie_plots.csv",header=None,usecols=[1],index_col=0)#tittles
    x_train = pd.read_csv("movie_plots.csv",header=None,usecols=[7],index_col=0)#plots           
    y_train = pd.read_csv("movie_plots.csv",header =None,index_col=0,usecols=[5])#genres
    x_train = list(x_train.itertuples())
    y_train = list(y_train.itertuples())
    x_tittles =  list(x_tittles.itertuples())
    y_train = [list(row) for row in y_train]#converts pandas dataframe into list
    x_train = [list(x_train[i]) for i in range(len(x_train)) if(y_train[i][0]!="unknown")]#does the same as the list comprehension for y_train for x_train but removing the unknown movies

    x_tittles = [list(x_tittles[i]) for i in range(len(x_tittles)) if(y_train[i][0]!="unknown")]#does the same as the list comprehension for y_train for x_tittles but removing the unknown movies
    y_train = [y_train[i] for i in range(len(y_train)) if(y_train[i][0]!="unknown")]#removes unknown genre instances
    #more movies will eventually have to be removed from the training set (movies that share genres or genres that are to niche) for now, this enough to carry through
    del y_train[0]#removes header statements
    del x_train[0]
    del x_tittles[0]
    movie_set = [copy.deepcopy(x_tittles),copy.deepcopy(x_train),copy.deepcopy(y_train)]#for ease in accessing evenly columned tittle, plot, and genre
    movie_set[1] = list(p.map(Pre, movie_set[1]))#processes each plot (can be inputed directly in tfidfVectorize().fit_transform as it is a list of strings)
    """ 
    print(x_train[0]) 
    print(movie_set[1][0])
    print(x_train[3])
    print(movie_set[1][3])
    print(x_train[67])
    print(movie_set[1][67])
    #x_train is not modified. the difference in the processing can be seen in the execution of the above print statements
    """
    p.close()
    p.join()
	
    print("finished:")
    print("time taken %f" % (time.time() - seconds))
    
