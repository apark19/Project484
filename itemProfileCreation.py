import pandas as pd
import csv
import time

#UTF-8 / ISO-8859-1
directorFrame = pd.read_csv('movie_directors.dat', encoding='unicode_escape', sep='\t',
                            usecols=['movieID', 'directorID', 'directorName'])
actorFrame = pd.read_csv('movie_actors.dat', encoding='unicode_escape', sep='\t',
                         usecols=['movieID', 'actorID', 'actorName', 'ranking'])
genreFrame = pd.read_csv('movie_genres.dat', sep='\t', encoding='unicode_escape', usecols=['movieID', 'genre'])
trainFrame = pd.read_csv('train.dat', sep=' ', encoding='unicode_escape', usecols=['movieID'])



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


if __name__ == "__main__":
    start = time.time()

    mID = genreFrame['movieID'].tolist()  # list of movieID's in the genre set
    movieAttributePairs = key_pair(genreFrame, directorFrame, actorFrame)
    uniqueMovies = set(mID)
    #print(uniqueMovies)
    #print(len(uniqueMovies))
    #exit()

    # Get the column headers from utility.csv
    with open("utility.csv", "r", encoding='unicode_escape') as ut:
        movie_vectors = csv.reader(ut, delimiter=',')

        i = 0
        for row in movie_vectors:
            if i == 0:
                header = list(row)
                break
    ut.close()
    header.remove('movieID')
    header.insert(0, 'movieID')
    del header[1]

    # Get attributes for each movie in the genre frame
    outFile = open("itemProfile1.csv", "w")
    outer = csv.writer(outFile)
    count = -1

    attributeCount = 0
    colCount = 0
    onesCount = 0
    #arr = search_pair(3, movieAttributePairs)
    #print(arr)
    #print(len(arr))
    #exit()


    for movie in uniqueMovies:
        if count == -1:
            outer.writerow(header)
        else:
            attributeList = search_pair(movie, movieAttributePairs)
            rowToInsert = [movie]
            for col in header:
                if col in attributeList:
                    rowToInsert.append('1')
                    attributeCount += 1
                    print("appending 1")
                    onesCount += 1
                else:
                    rowToInsert.append('0')
                colCount += 1
            print("movieID", movie)
            print("attributeCount: ", attributeCount)
            print("length of attribute list: ", len(attributeList))
            print("ColCount: ", colCount)
            colCount = 0
            outer.writerow(rowToInsert)
        if count == 50:
            break
        attributeCount = 0
        count += 1

    print("onesCount:", onesCount)
    print("total iterations: ", count)
    outFile.close()

    end = time.time()
    print(end - start)

