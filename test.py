from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
import pprint


def get_deeplink(imdb_id: str):
    IMDB_MOVIE_BASE_URL = "https://www.imdb.com/title/"
    # IMDB Movie page will be IMDB_MOVIE_BASE_URL + IMDB_ID

    options = Options()
    #options.headless = True
    options.add_argument('--headless=new')

    s = Service(ChromeDriverManager().install())

    # Install Driver
    driver = webdriver.Chrome(service=s, options=options)
    #driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    response_data = {}

    url = IMDB_MOVIE_BASE_URL + imdb_id + "/"

    driver.get(url)
    # time.sleep(3)
    time.sleep(5)
    html = driver.page_source
    print(html)
    a = driver.find_elements(By.CLASS_NAME, "WatchBox__MoreOptionsButton-sc-1kx3ihk-4")
    if a:
        anchors = []
        platform_text = []
        for i in a:
            if i.text == "More watch options":
                driver.find_elements(
                    By.CLASS_NAME, "WatchBox__MoreOptionsButton-sc-1kx3ihk-4"
                )[0].click()
                time.sleep(2)
                soup = BeautifulSoup(driver.page_source, "html.parser")
                # print(soup)

                div = soup.find(
                    "div",
                    {"class": "WatchOptions__CategoryContainer-sc-1ltcoc7-1 edEMgi"},
                )

                for i in div.find_all(
                    "a",
                    {
                        "class": "ipc-list__item WatchOptions__WatchOptionItem-sc-1ltcoc7-3 hZBQsI"
                    },
                ):
                    anchors.append(i["href"].split("?")[0])

                for i in div.find_all(
                    "div",
                    {"class": "WatchOptions__WatchOptionProvider-sc-1ltcoc7-4 ZwaXf"},
                ):
                    platform_text.append(i.text)

                for platform, deeplink in zip(platform_text, anchors):
                    response_data[platform] = deeplink

                driver.close()
    else:
        ott_platform = []
        href = []
        soup = BeautifulSoup(html, "html.parser")
        time.sleep(5)
        div = soup.find("div", {"class": "WatchBox__WatchParent-sc-1kx3ihk-5 bwsOYb"})

        # The name of the platform in the div
        if div.find("div", {"class": "WatchBox__PWO_Title-sc-1kx3ihk-1 jlBaNd"}):
            try:
                ott_platform = (
                    div.find("div", {"class": "WatchBox__PWO_Title-sc-1kx3ihk-1 jlBaNd"})
                    .get_text()
                    .split("Watch on ")[1]
                )
            except Exception as err:
                print(err)
                

        href = div.find_all("a", href=True)

        for i in href:
            deeplink = i["href"].split("?")[0]
        if len(ott_platform) == len(href) and (len(ott_platform) and len(href)) != 0:
            response_data["OTT"] = ott_platform
            response_data["Deeplink"] = deeplink
        driver.close()
    # driver.close()
    return response_data


# Movie on Amazon Prime
get_deeplink("tt8946378")

# Movie on Netflix
# get_deeplink("tt5071412")

# One movie on multiple platform
#a = get_deeplink("tt1375666")

# Movie on HBOMax
# get_deeplink("tt12361974")

# Watch on Hotstar
# get_deeplink("tt3896198")

#
# for id in ["tt10962368", "tt3846674", "tt4729430"]:
#     get_deeplink(id)

#print(a)

#get_deeplink("tt0371746")