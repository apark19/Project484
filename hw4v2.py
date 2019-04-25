import pandas as pd
import time
from multiprocessing import Process, Lock, Pool, freeze_support
import re
from functools import partial


# Create dataframes for all of the .dat files
directorFrame = pd.read_csv('movie_directors.dat', encoding='ISO-8859-1', sep='\t', usecols=['movieID', 'directorID', 'directorName'])
actorFrame = pd.read_csv('movie_actors.dat', encoding='ISO-8859-1', sep='\t', usecols=['movieID', 'actorID', 'actorName', 'ranking'])
genreFrame = pd.read_csv('movie_genres.dat', sep='\t', usecols=['movieID', 'genre'])
movieTagFrame = pd.read_csv('movie_tags.dat', encoding='ISO-8859-1', sep='\t', usecols=['movieID', 'tagID', 'tagWeight'])
tagsFrame = pd.read_csv('tags.dat', sep='\t', encoding='ISO-8859-1', usecols=['id', 'value'])
trainFrame = pd.read_csv('train.dat', sep=' ', encoding='ISO-8859-1', usecols=['userID', 'movieID', 'rating'])

trainFrame = trainFrame.iterrows()
trainFrame = list(trainFrame)
testFrame = pd.read_csv('test.dat', sep=' ', encoding='ISO-8859-1', usecols=['userID', 'movieID'])

# Remove any redundant information
# del actorFrame['actorName']
# del directorFrame['directorName']
del movieTagFrame['tagWeight']


def insertTrainingTuples(dataframe, trainingdata):
    print("inside function")
    count = 0
    
    tmp = str(trainingdata[1])
    tmp = re.sub('[^0-9.]+', ' ', tmp)
    tmp = tmp.split(" ")
    userEntry = list()
    userEntry.append(int(float(tmp[1])))
    userEntry.append(int(float(tmp[2])))
    userEntry.append(float(tmp[3]))
    dataframe.loc[count, ['userID', 'movieID', 'rating']] = userEntry

    outputList = list()
    outputList.append(dataframe.loc[count, "userID"])
    outputList.append(dataframe.loc[count, "movieID"])
    outputList.append(dataframe.loc[count, "rating"])
    print(outputList)
    count += 1
    
    return dataframe


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


if __name__ == "__main__":
    # execution start
    start = time.time()

    directorList = directorFrame['directorName'].tolist()   # yields 10155 entries
    actorList = actorFrame['actorName'].tolist()    # yields 231742 entries
    genreList = genreFrame['genre'].tolist() # yields 20809 entries

    # total = actors + directors + genres = 4053 + 95242 + 20 = 99315 columns to represent this info
    directorSet = set(directorList) # yields 4053 entries
    actorSet = set(actorList) # yields 95242 entries
    genreSet = set(genreList) # yields 20 entries

    # Make a dataFrame with empty columns of the above sets
    movieColumns = set(['userID', 'movieID', 'rating'])
    movieColumns = movieColumns | directorSet | actorSet | genreSet
    dataFrame = pd.DataFrame(columns=movieColumns)

    p = Pool(4)
    new_x = list(p.map(partial(insertTrainingTuples, dataFrame), trainFrame)) # processes each plot
    p.close()
    p.join()
    #df2.loc[startrow:endrow, startcolumn:endcolumn]
    #    dataFrame.loc['userID', int(float(tmp[1]))]
    #    dataFrame.loc['movieID', ]
    #dataFrame = trainFrame.append(dataFrame, sort=False)
    #print(dataFrame)

    end = time.time()
    #print(new_x)
    print(end - start)
    """
    exit()

    count = 0
    for row in trainFrame.iterrows():
        tmp = str(row[1])
        tmp = re.sub('[^0-9.]+', ' ', tmp)
        tmp = tmp.split(" ")
        userEntry = list()
        userEntry.append(int(float(tmp[1])))
        userEntry.append(int(float(tmp[2])))
        userEntry.append(float(tmp[3]))
        dataFrame.loc[count, ['userID', 'movieID', 'rating']] = userEntry

        outputList = list()
        outputList.append(dataFrame.loc[count, "userID"])
        outputList.append(dataFrame.loc[count, "movieID"])
        outputList.append(dataFrame.loc[count, "rating"])
        print(outputList)
        print(count)
        count += 1
        if count == 1000:
            break

    end = time.time()
    print()
    print(end - start)
    """

