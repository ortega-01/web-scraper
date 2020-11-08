import unittest
import sys
from selenium import webdriver

# Open up firefox browser
driver = webdriver.Firefox()

# Get item link from user input
#webpageLink = input("Enter webpage:")
#print (webpageLink)

# Navigate to webpage
driver.get("https://www.amazon.com/Sony-WH-CH510-Wireless-Headphones-WHCH510/dp/B07WSKKYPR/ref=sr_1_4?_encoding=UTF8&c=ts&dchild=1&keywords=On-Ear%2BHeadphones&qid=1604802580&s=aht&sr=1-4&ts_id=12097480011&th=1")

# Crawlin'
#div = driver.find_element_by_id('customer-reviews_feature_div')
allReviewsPage = driver.find_element_by_css_selector('a.a-link-emphasis.a-text-bold').get_attribute('href')

# Get all reviews webpage
driver.get(allReviewsPage)

rating1 = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div[1]/div/div[1]/div[5]/div[3]/div/div[1]/div/div/div[2]/a[1]')
#div = driver.find_element_by_id('customer_review-R2UWI4FAIK3OAO').text
#div = driver.find_element_by_id('a-row').text
#rating1 = div.find_element_by_class_name('a-icon-alt').text


print(rating1.text)

driver.close()

