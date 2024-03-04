import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

movie_dict=[]
url = "https://www.rottentomatoes.com/browse/movies_at_home/sort:popular"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.content, 'lxml')

movies_list = []

movies = soup.find_all('div', {'class': 'js-tile-link'})
num = 0
for movie_div in movies:
    anchor = movie_div.find('a')
    if anchor:
        urls = 'https://www.rottentomatoes.com' + anchor['href']
        movies_list.append(urls)
        num += 1
        movie_url = urls
        movie = requests.get(movie_url, headers=headers)
        movie_soup = BeautifulSoup(movie.content, 'lxml')
        movie_title_elem = movie_soup.find_all('span', {'class': 'p--small'})
        for titles in movie_title_elem :#and movie_info_elem:
          movie_title = titles.text.strip()
          print(movie_title,'\n',urls,"\n")
          movie_info = {
            "Title" : movie_title,
            "Link" : urls
          }
          movie_dict.append(movie_info)

all_movies = pd.DataFrame(movie_dict)
all_movies.to_csv("Movies.csv")
        
