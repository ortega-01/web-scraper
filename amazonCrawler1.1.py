import unittest
import sys
import time
import math
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from operator import attrgetter
#import pandas as pd

# Credibility Function
def credibilityfunc(helpful_votes, num_reviews)
	pass

# Main
profArr = []
revArr = []
helpfulVotes_arr = []
numReviews_arr = []

# Open up firefox browser
driver = webdriver.Firefox()

# Get item link from user input
#webpageLink = input("Enter webpage:")
#print (webpageLink)

# Navigate to webpage
driver.get("https://www.amazon.com/DualSense-Wireless-Controller-PlayStation-5/dp/B08FC6C75Y/ref=cm_cr_arp_d_product_top?ie=UTF8")

# Find link to all reviews page
allReviewsPage = driver.find_element_by_css_selector('a.a-link-emphasis.a-text-bold').get_attribute('href')

# Get all reviews webpage
driver.get(allReviewsPage)
#time.sleep(2)
totalReviews = driver.find_element_by_xpath("//div[@data-hook='cr-filter-info-review-rating-count']/span").get_attribute('innerHTML')

# Get total pages
mylist = totalReviews.split(" ")
#for i in range(len(mylist)):
#	print(mylist[i])
#	print(i)
totalReviews = mylist[27]
temp = int(totalReviews) 
pages = math.ceil(temp / 10)

# dont run unless necessary for testing, lots of get reqests to the server. 
"""
for i in range(pages):
	for x in range(10):
		profile = driver.find_elements_by_xpath("//div[contains(@id,'customer_review')]//div/a[@class='a-profile']")
		review = driver.find_elements_by_xpath("//div[@id='cm_cr-review_list']//i[contains(@class,'review-rating')]/span")
		profArr.append(profile[x].get_attribute('href'))
		ratingArr.append(review[x].get_attribute('innerHTML'))
	nextPage = driver.find_element_by_xpath("//li[@class= 'a-last']//*[contains(@href, 'pageNumber')]").get_attribute('href')
	driver.get(nextPage)
	time.sleep(1)

for i in range(len(profArr)):
	driver.get(profArr[i])
	time.sleep(2)
	helpfulVotes = driver.find_element_by_xpath("//div[contains(@id,'profile_')]/div/div/div[4]/div[2]/div[1]/div[2]/div/div[1]/a/div/div[1]/span").get_attribute('innerHTML')
	helpfulVotes_arr[i] = helpfulVotes
	numReviews = driver.find_element_by_xpath("//div[contains(@id,'profile_')]/div/div/div[4]/div[2]/div[1]/div[2]/div/div[2]/a/div/div[1]/span").get_attribute('innerHTML')
	numReviews_arr[i] = numReviews
	print(helpfulVotes)
	print(numReviews, "\n")
	print(ratingArr[i])
"""
driver.close()
# End of main 

""" 
Things to be done:
	Credibilty algo
	Make more efficent if possible 
	Implement dictionary/struct if needed for credibility algo 
	Create a main if necessary 
"""
