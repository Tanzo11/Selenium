from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import psycopg2

def initialize_driver():
    options = Options()
    # options.add_argument('--headless=new')
    return webdriver.Chrome(options=options)

def get_products(driver, url,n):
    driver.get(url)
    driver.maximize_window()
    time.sleep(5)
    
    products_dict = []
    scrollHeight = 0
    i = 1
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
            
            #Store the data as a dictionary
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
    return products_dict

def connect_to_db():
    return psycopg2.connect(
        dbname="fastdb",
        user="postgres",
        password="Tanzo",
        host="localhost",
        port="5432"
    )

def create_products_table(cur):
    cur.execute('''
        DROP TABLE IF EXISTS products    
    ''')

    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id VARCHAR(255) PRIMARY KEY,
            name VARCHAR(255),
            description TEXT,
            price VARCHAR(50),
            link TEXT
        )
    """)

def insert_data_into_db(cur, products_dict):
    for row in products_dict:
        row_values = tuple(row.values())
        cur.execute("INSERT INTO products (product_id, name, description, price, link) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (product_id) DO NOTHING", row_values)


n = int(input("Enter the no. of pages : "))

driver = initialize_driver()
products_dict = get_products(driver, "https://www.nykaafashion.com/catalogsearch/result/?q=Jeans+for+Men&utm_source=nykaabeauty&utm_medium=search_redirection&utm_campaign=frombeautyweb&search_redirection=True&p=1", n)

conn = connect_to_db()
cur = conn.cursor()

create_products_table(cur)
insert_data_into_db(cur, products_dict)


conn.commit()
conn.close()

driver.quit()

