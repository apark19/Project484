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

def Pre(par):
    par = list(par)
    tmp=copy.deepcopy(par)
    paragraph = tmp[2].lower()#the plots are in the third element of the array. lower is used so that words will still be considered the same instance when vectorized
    paragraph = re.sub('[^+A-Za-z0-9]+',' ',paragraph)#substittes non alphabetic or numerical charectars with a space
    #print(paragraph)
    paragraph = re.split(' ',paragraph)#issue here, paragraph does not split properly into words
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
    tmp[2] = new_paragraph
	#once the issue is fixed, I would like to see if lemmatization could be implemented while maintainig reasonable runtime https://www.geeksforgeeks.org/python-lemmatization-with-nltk/ 	
	
    return tmp
if __name__ == "__main__":
    p = Pool(4)
    seconds = time.time()
    x_train = pd.read_csv("movie_plots.csv",header=None,usecols=[1,7])#index,movie names, and plots from movie plot csv
    y_train = pd.read_csv("movie_plots.csv",header =None,usecols=[5])#genres
    #x = [[row[0],row[2]] for row in x_train.itertuples()]
    #print( re.sub('[^+A-Za-z0-9\\n]+',' ',x_train))
    #print(x_train)
    x = list(x_train.itertuples())
    x = [list(row) for row in x]#converts the pandas dataframe into normal list for compatability with map and overall ease of use
    del x[0]
    print(len(x))
    new_x = list(p.map(Pre, x))#processes each plot  
    print(new_x[0])
    print(new_x[1])#should run through once to see what the elements look like
    print(new_x[2])
    print(new_x[5])
    print(len(new_x))
    p.close()
    p.join()
	
    print("finished:")
    print("time taken %f" % (time.time() - seconds))