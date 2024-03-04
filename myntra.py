from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

n = int(input("Enter the no. of pages : "))
service = Service(executable_path="chromedriver.exe")
options = Options()
options.add_argument('--headless=new')
driver = webdriver.Chrome(service=service,options=options)

driver.get("https://www.nykaafashion.com/catalogsearch/result/?q=Jeans+for+Men&utm_source=nykaabeauty&utm_medium=search_redirection&utm_campaign=frombeautyweb&search_redirection=True&p=1")
driver.maximize_window()
time.sleep(5)
# WebDriverWait(driver,5).until(
#     EC.presence_of_element_located((By.CLASS_NAME, "css-384pms"))
# )
# print(driver.find_element(By.TAG_NAME, 'body').text)
scrollHeight = 0
i=1
#products_dict = {}
products_dict = []
while i<=(10*n):


    new_scrollHeight = driver.execute_script(f"window.scrollTo({scrollHeight}, ({scrollHeight}+(485)));return document.body.scrollHeight")
    time.sleep(1)
    
    
    i+=1
    products_list = driver.find_elements(By.CLASS_NAME,"css-1t10dtm")
    
    print(len(products_list))    
    
    
    for product in products_list:
        product_id = product.get_attribute("href").split("/")[-1]
        product_title = product.find_element(By.CLASS_NAME,"css-ham81y").text
        product_description = product.find_element(By.CLASS_NAME,"css-8ncoj4").text
        product_link = product.get_attribute("href")
        product_price = product.find_element(By.CLASS_NAME,"css-1ijk06y").text
        
        product_info = {
            "Product Id" : product_id,
            "Name" : product_title,
            "Description" : product_description,
            "Price" : product_price ,
            "Link" :  product_link
        }

        #products_dict[product_id] = product_info
        products_dict.append(product_info)

    time.sleep(1)
    if new_scrollHeight == scrollHeight:
        break
    scrollHeight +=485
    time.sleep(1)
print('done')
products = pd.DataFrame(products_dict)
products.set_index("Product Id",inplace=True)
products.to_csv("Products.csv")
#print(products_dict)
#print
time.sleep(100)

driver.quit()