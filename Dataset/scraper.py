# from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.webdriver.common.by import By
import requests
from csv import writer


driver = webdriver.Chrome()

# print(len(elements))
# print(elements)
details = []

page_no = 1
for i in range(1,10):
    driver.get('https://www.meesho.com/search?q=chikankari+kurti&searchType=autosuggest&searchIdentifier=text_search&page='+str(page_no))
    # driver.get('https://www.meesho.com/search?q=iphone&searchType=autosuggest&searchIdentifier=text_search&page='+str(page_no))
    sleep(0.5)
    elements = driver.find_elements(By.XPATH , "/html/body/div/div[3]/div/div[3]/div[2]/div[2]/div/div")
    i=1
    try:
        for element in elements:
            img_url = element.find_element(By.XPATH , "//*[@id='__next']/div[3]/div/div[3]/div[2]/div[2]/div/div["+str(i)+"]/a/div/div[1]/picture/source[2]").get_attribute('srcset')
            # print(img_url)
            
            price = element.find_element(By.XPATH , "//*[@id='__next']/div[3]/div/div[3]/div[2]/div[2]/div/div["+str(i)+"]/a/div/div[2]/div[1]/span/div/h5").text.replace(" onwards" , "")
            # print(price)
            # overall_ratings = element.find_element(By.XPATH , '//*[@id="__next"]/div[3]/div/div[3]/div[2]/div[2]/div/div['+str(i)+']/div/a/div/div[2]/div[3]/div/span[1]').get_attribute('label')
            # print(overall_ratings)
            # sleep(50000)
                                                            # //*[@id="__next"]/div[3]/div/div[3]/div[2]/div[2]/div/div[1]/a
            product_url = element.find_element(By.XPATH , '//*[@id="__next"]/div[3]/div/div[3]/div[2]/div[2]/div/div['+str(i)+']/a').get_attribute('href')
            # print(product_url)

            details += [{'index' : str(page_no)+str(i) ,'img_url' : img_url , 'price' : price , 'product_url' : product_url , 'ratings' : {'5':0 , '4':0 , '3':0 , '2':0 , '1':0}}]
            

            i+=1
    except:
        continue
    page_no += 1

# print(details[0]['product_url'])

for product in details:
    driver.get(product['product_url'])
    driver.find_element(By.XPATH , '//*[@id="__next"]/div[3]/div/div[2]/div[4]/div/div[2]/div[1]/span[2]').click
    product['ratings']['1'] = driver.find_element(By.XPATH , '//*[@id="__next"]/div[3]/div/div[2]/div[5]/div[1]/div/div[1]/div[2]/div[1]/div[3]/span').text
    product['ratings']['2'] = driver.find_element(By.XPATH , '//*[@id="__next"]/div[3]/div/div[2]/div[5]/div[1]/div/div[1]/div[2]/div[2]/div[3]/span').text
    product['ratings']['3'] = driver.find_element(By.XPATH , '//*[@id="__next"]/div[3]/div/div[2]/div[5]/div[1]/div/div[1]/div[2]/div[3]/div[3]/span').text
    product['ratings']['4'] = driver.find_element(By.XPATH , '//*[@id="__next"]/div[3]/div/div[2]/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[3]/span').text
    product['ratings']['5'] = driver.find_element(By.XPATH , '//*[@id="__next"]/div[3]/div/div[2]/div[5]/div[1]/div/div[1]/div[2]/div[5]/div[3]/span').text

    # print(ratings)

print(details)

with open('dataset1.csv', 'w' , encoding = 'utf-8' , newline='') as f:
    write = writer(f)
    parameters = ['index' ,'img_url' , 'prod_url' , 'price' , '5' ,'4','3','2','1']
    write.writerow(parameters)
    for detail in details:
        arr = [detail['index'] , detail['img_url'] , detail['product_url'] , detail['price'] , detail['ratings']['5'] , detail['ratings']['4'] , detail['ratings']['3'], detail['ratings']['2'] , detail['ratings']['1']]
        write.writerow(arr)

