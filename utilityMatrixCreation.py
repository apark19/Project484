import pandas as pd
import csv
import time
from multiprocessing import Pool
from functools import partial

# UTF-8 / ISO-8859-1
directorFrame = pd.read_csv('movie_directors.dat', encoding='unicode_escape', sep='\t',
                            usecols=['movieID', 'directorID', 'directorName'])
actorFrame = pd.read_csv('movie_actors.dat', encoding='unicode_escape', sep='\t',
                         usecols=['movieID', 'actorID', 'actorName', 'ranking'])
genreFrame = pd.read_csv('movie_genres.dat', sep='\t', encoding='unicode_escape', usecols=['movieID', 'genre'])
trainFrame = pd.read_csv('train.dat', sep=' ', encoding='unicode_escape', usecols=['userID', 'movieID', 'rating'])


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


def search_pair(id, frame):
    attributes = []
    for i in frame[2]:
        if (i[0] == id):
            attributes.append(i[1])
    for i in frame[1]:
        if (i[0] == id):
            attributes.append(i[1])
    for i in frame[0]:
        if (i[0] == id):
            attributes.append(i[1])
    return attributes


def search_col(attributeList,rowToInsert,col):

        if col in attributeList:
            rowToInsert.append('1')
            # attributeCount += 1
            # print("appending 1")
            # onesCount += 1
        else:
            rowToInsert.append('0')
        return attributeList


if __name__ == "__main__":
    start = time.time()

    userIDs = trainFrame['userID'].tolist()  # list of userID's in the training set
    movieIDs = trainFrame['movieID'].tolist() # list of movieID's in the training set
    ratings = trainFrame['rating'].tolist() # list of ratings in the training set

    #userSet = set(userIDs)
    #print(len(userSet))
    #exit()

    movieAttributePairs = key_pair(genreFrame, directorFrame, actorFrame)

    # Get unique column headers
    directorList = directorFrame['directorName'].tolist()  # yields 10155 entries
    actorList = actorFrame['actorName'].tolist()  # yields 231742 entries
    genreList = genreFrame['genre'].tolist()  # yields 20809 entries

    # total = actors + directors + genres = 4053 + 95242 + 20 = 99315 columns to represent this info
    directorSet = set(directorList)  # yields 4053 entries
    actorSet = set(actorList)  # yields 95242 entries
    genreSet = set(genreList)  # yields 20 entries

    totalSet = directorSet | actorSet | genreSet
    headers = list(totalSet)

    headers.insert(0, 'userID')
    headers.insert(1, 'movieID')
    headers.insert(2, 'rating')
    del headers[3]

    #print(headers[0])
    #print(headers[1])
    #print(headers[2])
    #print(headers[3])
    #print(headers[4])
    #print(len(headers))
    #exit()

    outFile = open("utilityMatrixFinal.csv", "w")
    outer = csv.writer(outFile)
    index = -1

    attributeCount = 0
    colCount = 0
    onesCount = 0
    # arr = search_pair(3, movieAttributePairs)
    # print(arr)
    # print(len(arr))
    # exit()
    p = Pool(4)
    print(userIDs[0])

    for user in range(len(userIDs)):
        userIndex = userIDs[user]

        #print(userIndex)
        #print(user)
        #exit()

        if index == -1:
            outer.writerow(headers)
        else:
            attributeList = search_pair(movieIDs[index], movieAttributePairs)
            rowToInsert = [user, movieIDs[index], ratings[index]]
            rowToInsert = list(p.map(partial(search_col,attributeList,rowToInsert),headers))
            '''
            for col in headers:
                if col in attributeList:
                    rowToInsert.append('1')
                    #attributeCount += 1
                    #print("appending 1")
                    #onesCount += 1
                else:
                    rowToInsert.append('0')
                #colCount += 1'''
            #print("movieID", movieIDs[index])
            #print("attributeCount: ", attributeCount)
            print("length of attribute list: ", len(attributeList))
            #print("ColCount: ", colCount)
            #colCount = 0
            outer.writerow(rowToInsert)
        if index == 1000:
            break
        #attributeCount = 0
        index += 1

    print("onesCount:", onesCount)
    print("total iterations: ", index)
    outFile.close()

    end = time.time()
    print(end - start)
