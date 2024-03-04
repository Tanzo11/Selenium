from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time

headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 '}
service = Service(executable_path="chromedriver.exe")
options = Options()
options.add_argument(f'user-agent={headers["User-Agent"]}')

options.add_argument('--headless=new')


options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(service=service,options=options)
action = ActionChains(driver)
driver.get("https://www.imdb.com/title/tt0371746/?ref_=fn_al_tt_1")
driver.implicitly_wait(10)


try:
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'ipc-slate.ipc-slate--baseAlt.ipc-slate--dynamic-width.sc-f7ef1f83-2.iaOMF.no-description.ipc-sub-grid-item.ipc-sub-grid-item--span-4'))
    ) 
    
    target_tab = element.find_element(By.CSS_SELECTOR, ".ipc-lockup-overlay.ipc-focusable")
    print(target_tab.get_attribute("href"))
   
    time.sleep(18)
    # target_tab.click()
    action.click(target_tab).perform()
except Exception as e:
    print(f"An error occurred: {e}")

time.sleep(5)
hotstar_url = driver.current_url
print("Hotstar URL:", hotstar_url)

# Optionally, you can further scrape information from the Hotstar page
hotstar_soup = BeautifulSoup(driver.page_source, "html.parser")
# Example: Extract title
title = hotstar_soup.find("h1").text
print("Title:", title)

time.sleep(10)
driver.quit()

