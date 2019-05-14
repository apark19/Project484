from bs4 import BeautifulSoup
import time
import pandas as pd
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import re

url = 'https://movieweb.com/movies/' # 2005 / 'https://movieweb.com/movies/2000/?page=2
genreLabels = {'Thriller', 'Action', 'Adventure', 'Fantasy', 'Drama', 'Comedy', 'Romance', 'Love', 'SciFi', 'Horror', 'Animation', 'Family'}
headers = {'User-Agent': 'Mozilla/5.0'}

# This function will take a URL as a parameter.
# This URL parameter must be accessible, else a HTMLError will occur
# This function will open a URL link and get the HTML contents of the page
# which will then be returned for parsing
def getHtmlPage(url):
    request = Request(url, headers=headers)    # Send GET request to server
    page = urlopen(request).read()      # Open page and read contents
    soup = BeautifulSoup(page, 'html.parser')   # initialize parser using BeautifulSoup
    return soup


if __name__ == "__main__":
    start = time.time()

    # Extract from each page until there is a 404 Error (HTTP ERROR 404: Not Found)
    # Iterate through the year that you want to search
    # Will extract from ALL pages from results
    #movieYear = 2016
    for year in range(2016, 2020):
        pageNumber = 1
        scrapperFrame = pd.DataFrame(columns=['title', 'plot', 'genre'])
        endFlag = False     # used to exit out of the loop
        while not endFlag:
            try:
                if pageNumber == 1:     # if first iteration, set URL AND lastPage (this is easiest on first iteration)
                    pageToExtract = url + str(year)
                    bSoup = getHtmlPage(pageToExtract)  # Get parser for given URL

                    navigationLinks = bSoup.find_all('a', {'class': 'pagination-link'})  # Get all pagination links
                    if len(navigationLinks) > 0:
                        lastPage = navigationLinks[len(navigationLinks)-1].get('href')  # if there are numerous links, get the lastPage
                    else:
                        lastPage = None     # else, there is only one page, so exit after 1 iteration
                    pageNumber += 1
                else:
                    pageToExtract = url + str(year) + '/?page=' + str(pageNumber)  # On iteration > 1, URL is different
                    bSoup = getHtmlPage(pageToExtract)
                    pageNumber += 1

                if lastPage == pageToExtract or lastPage is None:   # If at lastPage, exit after this iteration
                    endFlag = True

                for movie in bSoup.find_all('section', {'class': 'movie'}):     # For each movie on page
                    try:
                        title = movie.find('h2', {'class': 'movie-title'}).text     # Get title
                        genre = re.sub('[^A-Za-z]+', '', movie.find('li', {'class': 'movie-genre'}).text)   # Get genre
                        summary = movie.find('div', {'class': 'movie-synopsis'}).text   # Get summary

                    #print(title)
                    #print(genre)
                    #print(genre == 'SciFi')
                    #print(len(summary))

                        if genre is not None and genre in genreLabels and len(summary) > 127:   # If genre is found && is popular genre label && summary length is long enough
                            scrapperFrame.loc[len(scrapperFrame)] = [title, summary, genre]  # Add to dataFrame
                    except AttributeError:
                        print("This movie does not have genre: ", title)    # If genre is not present || genre is not popular, skip
                        print("PageNumber: ", pageNumber)
                        continue
            except HTTPError:
                print("Page cannot be found")
                print("Writing to csv...")
                endFlag = True  # End loop because end of results has been reached

        print(len(scrapperFrame))

        # Write to file
        fileName = 'movies_' + str(year) + '.csv'
        scrapperFrame.to_csv(fileName, sep=',', index=False)

    print("\nfinished:")
    end = time.time()
    print(end-start)
