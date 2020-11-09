from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from operator import attrgetter
import pandas as pd
import time

PATH = "C:\Program Files (x86)\chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
driver = webdriver.Chrome(PATH,chrome_options=options)

driver.get("https://www.amazon.com/DualSense-Wireless-Controller-PlayStation-5/product-reviews/B08FC6C75Y/ref=cm_cr_getr_d_paging_btm_prev_1?ie=UTF8&reviewerType=all_reviews&pageNumber=1")
#https://www.amazon.com/HP-Chromebook-11-inch-Laptop-11a-na0021nr/product-reviews/B08H6YZY3Y/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews
#print(driver.title)

numReviewers = 0
ratings = []
urls = []
helpful_Votes = []
num_Reviews = []
info_list = []
pageNum = 0

#Ex. To wait for something on webpage to be loaded
#Waits max 10 sec for presence of specified element
try:
    wait1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "cm_cr-review_list")))
    reviews = driver.find_elements_by_xpath("//div[@id='cm_cr-review_list']//i[contains(@class,'review-rating')]/span")
    allReviewsPage = driver.find_elements_by_xpath("//div[contains(@id,'customer_review')]//div/a[@class='a-profile']")
    #nextPage = driver.find_element_by_xpath("//*[@id='cm_cr-pagination_bar']/ul/li[2]/a")
    #prevPage = driver.find_element_by_xpath("//*[@id='cm_cr-pagination_bar']/ul/li[1]/a")

    for i in range(len(allReviewsPage)):
        ratings.append(reviews[i].get_attribute('innerHTML'))
        prof = (allReviewsPage[i].get_attribute('href'))
        urls.append(prof)
        numReviewers += 1
        #info_item = {
            #"Rating": ratings[i]
        #}
        #info_list.append(info_item)

    #print(ratings)
    #print(urls)
    #print(len(allReviewsPage))
    #print(len(reviews))
    #print(prevPage.get_attribute('href'))

    #try:
        #nextPage = driver.find_element_by_xpath("//*[@id='cm_cr-pagination_bar']/ul/li[2]/a[contains(@text,'Next Page')]")
        #prevPage = driver.find_element_by_xpath("//a[contains(@text,'Previous Page')]")
        #//*[@id="cm_cr-pagination_bar"]/ul/li[2]/a/text()[1]
        
        #pageNum += 1
        #if(nextPage.size != 0):
            #next_Page = nextPage.get_attribute('href')
            #driver.get(next_Page)
        #print(pageNum)
        #print(nextPage.size)
        #print(prevPage.size)
    #except:
        #print("No next page")


    #Gets individual profile info -- helpful votes and number of reviews
    for j in range(numReviewers):
        driver.get(urls[j])
        wait2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "dashboard-desktop-stat-value")))
        helpful_Votes = driver.find_element_by_xpath("//div[contains(@id,'profile_')]/div/div/div[4]/div[2]/div[1]/div[2]/div/div[1]/a/div/div[1]/span").get_attribute('innerHTML')
        numReviews = driver.find_element_by_xpath("//div[contains(@id,'profile_')]/div/div/div[4]/div[2]/div[1]/div[2]/div/div[2]/a/div/div[1]/span").get_attribute('innerHTML')
        info_item = {
            "Rating": ratings[j],
            "Helpful Votes": helpful_Votes,
            "Number of Reviews": numReviews
        }
        info_list.append(info_item)
        time.sleep(3)

    df = pd.DataFrame(info_list)
    print(df)

    #time.sleep(3)

    #print(helpful_Votes)
    #print(num_Reviews)
    #print(ratings)
    #print(numReviewers)
    #print(urls)

finally:
    #pass
    driver.quit()