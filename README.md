# Project484

WOutAnimationScrapperCSVs directory - stores all the scrapper data without Animation genres
WAnimationScrapperCSVs direcory - stores all the scrapper data with Animation genres

cs484_final.py pre proccesses plot summary text data into new csv with Animation directory contains movie data with animated film plot summaries
scrapperV2.py - python script that scraps HTML pages from movieweb.com by year
titleformatter.py - python script that removes any extraneous characters from scrapper titles and makes lowercase genres for matching with training set
trainingSetFiller.py - python script that creates a training set and test set by combining the scrapper data with original Kaggle data set.
484final_predictorBOOST.py - python script that utilizes AdaBOOST from sklearn to classify genres
484final_predictorDT.py - python script that utilizes Decision Tree from sklearn to classify genres
484final_predictorGB.py - python script that utilizes Naive Bayes from sklearn to classify genres
484final_predictorKNN.py - python script that utlizes KNN from sklearn to classify genres
484final_predictorMLP.py - python script that utilizes Neural Network from sklearn to classify genres

amino_apark_FinalReport.pdf - Final Report on findings
final_movies_training.csv - training set without Animation genre used for results
final_movies_trainingAnimation.csv - training set with Animation genre used  for results
testFinal.csv - test set without Animation genre used for results
testFinalAnimation.csv - test set without Animation genre used for results
