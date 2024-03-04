# import requests
# from bs4 import BeautifulSoup
# import time
# import pandas as pd

# movie_dict=[]
# url = "https://www.imdb.com/what-to-watch/fan-favorites/?ref_=hm_fanfav_sm"
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
# }
# r = requests.get(url, headers=headers)
# soup = BeautifulSoup(r.content, 'lxml')

# movies_list = []

# movies = soup.find_all('div', {'class': 'ipc-poster-card ipc-poster-card--baseAlt ipc-poster-card--dynamic-width ipc-sub-grid-item ipc-sub-grid-item--span-2'})

# for movie_div in movies:
#     anchor = movie_div.find('a',{'class':'ipc-lockup-overlay ipc-focusable'})
#     if anchor:
#         urls = 'https://www.imdb.com/' + anchor['href']
#         movies_list.append(urls)
#         num += 1
#         movie_url = urls
#         movie = requests.get(movie_url, headers=headers)
#         movie_soup = BeautifulSoup(movie.content, 'lxml')
#         movie_title_elem = movie_soup.find_all('span', {'class': 'hero__primary-text'})
#         for titles in movie_title_elem :#and movie_info_elem:
#           movie_title = titles.text.strip()
#           print(movie_title,'\n',urls,"\n")
#           movie_info = {
#             "Title" : movie_title,
#             "Link" : urls
#           }
#           movie_dict.append(movie_info)

# all_movies = pd.DataFrame(movie_dict)
# all_movies.to_csv("MoviesIMDB.csv")
        

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import pandas as pd

headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 '}
service = Service(executable_path="chromedriver.exe")
options = Options()
options.add_argument(f'user-agent={headers["User-Agent"]}')

options.add_argument('--headless=new')


options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(service=service,options=options)
action = ActionChains(driver)
driver.get("https://www.imdb.com/what-to-watch/fan-favorites/?ref_=hm_fanfav_sm")
driver.implicitly_wait(10)

movies_dict = []
movies_list=[]
try:
    # element = WebDriverWait(driver, 5).until(
    #     EC.presence_of_element_located((By.CLASS_NAME, 'ipc-poster-card.ipc-poster-card--baseAlt.ipc-poster-card--dynamic-width.ipc-sub-grid-item.ipc-sub-grid-item--span-2'))
    # )
    
    elements = driver.find_elements(By.CSS_SELECTOR,'.ipc-poster-card.ipc-poster-card--baseAlt.ipc-poster-card--dynamic-width.ipc-sub-grid-item.ipc-sub-grid-item--span-2')
    
    time.sleep(5)
    for movies_div in elements:
        
        anchor = movies_div.find_element(By.CLASS_NAME,'ipc-lockup-overlay.ipc-focusable')
        print(anchor.get_attribute("href"))
        if anchor:
            url = anchor.get_attribute("href")
            movies_list.append(url)
            
            driver.get(url)
            
            title = driver.find_element(By.CLASS_NAME,'hero__primary-text').text
            print(title)
            #description = driver.find_element(By.CLASS_NAME,'sc-466bb6c-0.hlbAws').text
            #print(description)
            movie_info = {
            "Title" : title,
            "Link" : url#,
            # "Description": description
          }
            movies_dict.append(movie_info)
        else:
            print("Unable to fetch")
except Exception as e:
    print(e)
print(movies_list)
all_movies = pd.DataFrame(movies_dict)
all_movies.to_csv("MoviesIMDB.csv")





    

