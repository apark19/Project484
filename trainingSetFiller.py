import pandas as pd
import time

#/Users/johndoe/PycharmProjects/untitled484/formattedScrapperFiles

def lowercaseTitle(title):
    return title.lower()


def sciFiNormalize(title):
    if title == 'sci-fi':
        return 'scifi'
    else:
        return title


if __name__ == "__main__":
    start = time.time()
    trainingFrame = pd.read_csv('training_data(movies).csv')
    trainingFrame['title'] = trainingFrame['title'].apply(lowercaseTitle)
    trainingFrame['genre'] = trainingFrame['genre'].apply(sciFiNormalize)

    '''
    #genres = trainingFrame['genre']
    #df.drop(df[df.score < 50].index, inplace=True)
    #subsetDataFrame = dfObj[dfObj['Product'] == 'Apples']
    romanceFrame = trainingFrame[trainingFrame['genre'] == 'romance']
    loveFrame = trainingFrame[trainingFrame['genre'] == 'love']
    comedyFrame = trainingFrame[trainingFrame['genre'] == 'comedy']
    fantasyFrame = trainingFrame[trainingFrame['genre'] == 'fantasy']
    thrillerFrame = trainingFrame[trainingFrame['genre'] == 'thriller']
    horrorFrame = trainingFrame[trainingFrame['genre'] == 'horror']
    scienceFrame = trainingFrame[trainingFrame['genre'] == 'sci-fi']
    actionFrame = trainingFrame[trainingFrame['genre'] == 'action']
    dramaFrame = trainingFrame[trainingFrame['genre'] == 'drama']
    familyFrame = trainingFrame[trainingFrame['genre'] == 'family']
    adventureFrame = trainingFrame[trainingFrame['genre'] == 'adventure']
    '''

    # Drop documentary entries
    trainingFrame.drop(trainingFrame[trainingFrame.genre == 'documentary'].index, inplace=True)

    # Comedy and Drama genres already have too many entries
    # Split these to 3,000
    # Remaining entries should be used for test
    #comedyFrameTrain = comedyFrame.iloc[0:3000, :]
    #comedyFrameTest = comedyFrame.iloc[3000:5641, :]
    #dramaFrameTrain = dramaFrame.iloc[0:3000, :]
    #dramaFrameTest = dramaFrame.iloc[3000:3890, :]

    # Process scrapper data by group (EX: Year 1970 - 1979)
    scrapperFrame = pd.DataFrame()
    for year in range(1910, 2020):
        fileName = 'formatted_' + str(year) + '.csv'
        tempFrame = pd.read_csv(fileName, names=None)
        scrapperFrame = pd.concat([scrapperFrame, tempFrame], ignore_index=True, sort=False)

    # Drop documentary entries from scrapper frame
    scrapperFrame.drop(scrapperFrame[scrapperFrame.genre == 'Documentary'].index, inplace=True)

    # TestFrame
    # TrainingFrame
    for index in range(len(trainingFrame)):
        if any(scrapperFrame.title == trainingFrame.iloc[index, 0]):
            scrapperFrame.drop(scrapperFrame[scrapperFrame.title == trainingFrame.iloc[index, 0]].index, inplace=True)

    #print(scrapperFrame)
    trainingFrame = pd.concat([scrapperFrame, trainingFrame], ignore_index=True)
    '''
    print(trainingFrame[trainingFrame.genre == 'romance'])
    print(trainingFrame[trainingFrame.genre == 'comedy'])
    print(trainingFrame[trainingFrame.genre == 'fantasy'])
    print(trainingFrame[trainingFrame.genre == 'thriller'])
    print(trainingFrame[trainingFrame.genre == 'horror'])
    print(trainingFrame[trainingFrame.genre == 'sci-fi'])
    print(trainingFrame[trainingFrame.genre == 'scifi'])
    print(trainingFrame[trainingFrame.genre == 'action'])
    print(trainingFrame[trainingFrame.genre == 'drama'])
    print(trainingFrame[trainingFrame.genre == 'family'])
    print(trainingFrame[trainingFrame.genre == 'adventure'])
    '''
    #print(trainingFrame)
    # comedyFrameTrain = comedyFrame.iloc[0:3000, :]
    # comedyFrameTest = comedyFrame.iloc[3000:5641, :]
    # dramaFrameTrain = dramaFrame.iloc[0:3000, :]
    # dramaFrameTest = dramaFrame.iloc[3000:3890, :]

    romanceFrame = trainingFrame[trainingFrame['genre'] == 'romance']
    #loveFrame = trainingFrame[trainingFrame['genre'] == 'love']
    comedyFrame = trainingFrame[trainingFrame['genre'] == 'comedy']
    fantasyFrame = trainingFrame[trainingFrame['genre'] == 'fantasy']
    thrillerFrame = trainingFrame[trainingFrame['genre'] == 'thriller']
    horrorFrame = trainingFrame[trainingFrame['genre'] == 'horror']
    scienceFrame = trainingFrame[trainingFrame['genre'] == 'scifi']
    actionFrame = trainingFrame[trainingFrame['genre'] == 'action']
    dramaFrame = trainingFrame[trainingFrame['genre'] == 'drama']
    familyFrame = trainingFrame[trainingFrame['genre'] == 'family']
    adventureFrame = trainingFrame[trainingFrame['genre'] == 'adventure']
    animationFrame = trainingFrame[trainingFrame['genre'] == 'animation']

    romanceFrameTrain = romanceFrame.iloc[0:1000, :]
    romanceFrameTest = romanceFrame.iloc[1000:1031, :]

    comedyFrameTrain = comedyFrame.iloc[0:1000, :]
    comedyFrameTest = comedyFrame.iloc[1000:2500, :]

    fantasyFrameTrain = fantasyFrame.iloc[0:600, :]
    fantasyFrameTest = fantasyFrame.iloc[600:27, :]

    thrillerFrameTrain = thrillerFrame.iloc[0:1000, :]
    thrillerFrameTest = thrillerFrame.iloc[1000:2003, :]

    horrorFrameTrain = horrorFrame.iloc[0:1000, :]
    horrorFrameTest = horrorFrame.iloc[1000:2000, :]

    scienceFrameTrain = scienceFrame.iloc[0:700, :]
    scienceFrameTest = scienceFrame.iloc[700:736, :]

    actionFrameTrain = actionFrame.iloc[0:1000, :]
    actionFrameTest = actionFrame.iloc[1000:2000, :]

    dramaFrameTrain = dramaFrame.iloc[0:1000, :]
    dramaFrameTest = dramaFrame.iloc[1000:2000, :]

    familyFrameTrain = familyFrame.iloc[0:700, :]
    familyFrameTest = familyFrame.iloc[700:745, :]

    adventureFrameTrain = adventureFrame.iloc[0:1000, :]
    adventureFrameTest = adventureFrame.iloc[1000:667, :]

    animationFrameTrain = animationFrame.iloc[0:1000, :]
    animationFrameTest = animationFrame.iloc[1000:1378, :]

    trainingSet = [romanceFrameTrain, fantasyFrameTrain, comedyFrameTrain, thrillerFrameTrain, horrorFrameTrain, scienceFrameTrain, actionFrameTrain, dramaFrameTrain, familyFrameTrain, adventureFrameTrain, animationFrameTrain]
    testSet = [romanceFrameTest, fantasyFrameTest, comedyFrameTest, thrillerFrameTest, horrorFrameTest, scienceFrameTest, actionFrameTest, dramaFrameTest, familyFrameTest, adventureFrameTest, animationFrameTest]

    trainingFrameFinal = pd.concat(trainingSet, ignore_index=True)
    print(trainingFrameFinal)

    testFrameFinal = pd.concat(testSet, ignore_index=True)
    print(testFrameFinal)

    trainingFrameFinal.to_csv('trainingFinalv2.csv', sep=',', index=False)
    testFrameFinal.to_csv('testFinalv2.csv', sep=',', index=False)

    print()

    end = time.time()
    print("Run time: ", end-start)
