from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

service = Service(executable_path="chromedriver.exe")
headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 '}
chrome_options = Options().add_argument(f'user-agent={headers["User-Agent"]}')

driver = webdriver.Chrome(service=service, options=chrome_options)
time.sleep(0.5)
driver.get("https://google.com")
WebDriverWait(driver,5).until(
    EC.presence_of_element_located((By.CLASS_NAME, "gLFyf"))
)

input_element = driver.find_element(By.CLASS_NAME, "gLFyf")   #access the element
input_element.clear()
input_element.send_keys("tech with tim" + Keys.ENTER) 
#to type the text   and Keys to send a particular keyboard input
link = WebDriverWait(driver,5).until(
    EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Tech With Tim"))
)
urls = driver.find_elements(By.PARTIAL_LINK_TEXT, "Tech With Tim")
for url in urls:
    print('---->>>', url.get_attribute("href"))

# link = driver.find_element(By.PARTIAL_LINK_TEXT, "Tech with Tim")
print(link.get_attribute("href"))
#links = driver.find_elements(By.PARTIAL_LINK_TEXT, "INDIA VS ENGLAND HIGHLIGHTS")
#to get multiple links and LINK_TEXT to get the exact link
link.click()


time.sleep(8)

driver.quit()