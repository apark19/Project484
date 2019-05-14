import pandas as pd
import time

# This function takes a movie title as a parameter
# and removes any leading whitespaces as well as
# converts the string to lower-case, which
# will allow for easy comparisons between
# duplicates in the training set.
def formatTitle(movieTitle):
    titleList = movieTitle.split(' ')   # split the title by space
    if len(titleList[len(titleList)-1]) == 0:   # if there is an extra space at the end of title
        lastIndex = len(titleList)-1    # the last index should be length-1
    else:
        lastIndex = len(titleList)  # if there is NOT an extra space, the last index is standard

    if len(titleList[0]) == 0:  # if there is a space at the beginning of the title
        newTitle = titleList[1].lower()
        for index in range(2, lastIndex):   # iterate from index 2 -> lastIndex
            newTitle = newTitle + ' ' + titleList[index].lower()
        return newTitle
    else:
        newTitle = titleList[0].lower()  # if there is NOT a space at the beginning of title
        for index in range(1, lastIndex):   # iterate from index 1 -> lastIndex
            newTitle = newTitle + ' ' + titleList[index].lower()
    return newTitle


if __name__ == "__main__":
    start = time.time()

    #movieYear = 1974
    for year in range(1910, 2020):
        fileName = 'movies_' + str(year) + '.csv'
        dataFrame = pd.read_csv(fileName, names=None)
        for index in range(len(dataFrame)):     # iterate through each movie title in file and format
            dataFrame.iloc[index, 0] = formatTitle(dataFrame.iloc[index, 0])    # Re-write to dataFrame
            dataFrame.iloc[index, 2] = dataFrame.iloc[index, 2].lower()
            #print(dataFrame.iloc[index, 0])

        # Write to file
        outFile = 'formatted_' + str(year) + '.csv'
        dataFrame.to_csv(outFile, sep=',', index=False)
        #print(dataFrame)

    end = time.time()
    print("Time elapsed: ", end-start)
