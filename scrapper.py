from bs4 import BeautifulSoup
import time
import pandas as pd
import requests
from urllib.parse import urljoin
import json
from urllib.request import urlopen

if __name__ == "__main__":
    seconds = time.time()
    x_train = pd.read_csv("movie_plots.csv", usecols=['Release Year', 'Title', 'Origin/Ethnicity', 'Director', 'Cast', 'Genre', 'Wiki Page', 'Plot'])

    movieTitles = x_train['Title']
    movieYears = x_train['Release Year']

    #print(movieTitles)
    #print(len(movieTitles))

    #print(movieYears)
    #print(len(movieYears))

    #url = "http://www.imdb.com/find?ref_=nv_sr_fn&q=" + '+'.join(search_terms) + '&s=all'
    headers = {'User-Agent': 'Mozilla/5.0'}

    for index in range(len(movieTitles)):   # total= 34886
        searchTerm = movieTitles[index].replace(" ", "+")
        searchTerm = '+' + searchTerm + '+' + str(movieYears[index])
        #print(searchTerm)

        # Create url
        url = "http://www.imdb.com/find?ref_=nv_sr_fn&q=" + searchTerm + '&s=all'
        response = requests.get(url, headers=headers)
        bSoup = BeautifulSoup(response.text, "html.parser")
        searchResultUrl = bSoup.find('td', 'result_text').find('a').get('href')

        newUrl = urljoin(url, searchResultUrl)
        response = requests.get(newUrl, headers=headers)

        bSoup = BeautifulSoup(response.text, "xml")
        xmlToParse = bSoup.find('script', type='application/ld+json')
        print(xmlToParse)   # ->> this is in some json format or some shit


















        #data = json.loads(newUrl.read().decode())
        #print(data)

        exit()
        #year = bSoup.find('span', {'id': 'titleYear'}).find('a').get_text()
        #genre = bSoup.find('span', {'id': 'genre'}).find('a').get_text()
        #movie = bSoup.find('span', {'id': 'title'}).find('a').get_text()

        #print(movie)
        #exit()

        #print(response)
        #data = response.json()
        #print(data)

    print("finished:")
    print("time taken %f" % (time.time() - seconds))
