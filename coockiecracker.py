from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

service = Service(executable_path="chromedriver.exe")

driver = webdriver.Chrome(service=service)

driver.get("https://orteil.dashnet.org/cookieclicker/")


cookie_id = "bigCookie"
cookies_id = "cookies"
product_price_prefix = "productPrice"
product_prefix = "product"

language= WebDriverWait(driver,5).until(
    EC.presence_of_element_located((By.ID, "langSelect-EN"))
)
# time.sleep(1)
# language = driver.find_element(By.ID, "langSelect-EN")
language.click()
time.sleep(0.5)


cookie = driver.find_element(By.ID, cookie_id)
time.sleep(0.5)
cookie.click()

while True:

    #time.sleep(0.5)
    cookie.click()
    cookies_count = driver.find_element(By.ID, cookies_id).text.split(" ")
    cookie_str = "".join(cookies_count[1:])
    cookies_count = int(cookies_count[0].replace(",",""))
    print(cookies_count," ",str(cookie_str))

    for i in range(4):
        product_price = driver.find_element(By.ID, product_price_prefix + str(i)).text.replace(",","")
        
        if not product_price.isdigit():
            continue
        
        product_price = int(product_price)

        if cookies_count >= product_price:

            product = driver.find_element(By.ID, product_prefix + str(i))
            product.click()
            break

time.sleep(200)


