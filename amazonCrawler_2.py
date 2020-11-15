from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from operator import attrgetter
import pandas as pd
import time
import math

#CSC360 Project 2: Amazon Product Review Scraping
#	This program goes to the specified webpage of a certain Amazon product.
#	It then scrapes the pages of product reviews to obtain data that will be
#	used to estimate the credibility of each reviewer. The program will then use
#	these results to create a new adjusted average score (star rating) for the given product.

profArr = []  #List of profile urls
ratingArr = []  #List of reviewer star ratings
info_list = []  #List of all desired information, including the number of helpful votes and reviews of each reviewer
currPage = 1  #For navigating through multiple pages of reviews

# Open up firefox browser -- when running set path to wherever geckodriver is on your computer
driver = webdriver.Firefox(executable_path="C:\Program Files (x86)\geckodriver")

# Get item link from user input
#webpageLink = input("Enter webpage:")
#print (webpageLink)

# Navigate to webpage
driver.get("https://www.amazon.com/DualSense-Wireless-Controller-PlayStation-5/dp/B08FC6C75Y/ref=cm_cr_arp_d_product_top?ie=UTF8")
#Test for Product with more than one page of reviews: https://www.amazon.com/DualSense-Wireless-Controller-PlayStation-5/dp/B08FC6C75Y/ref=cm_cr_arp_d_product_top?ie=UTF8
#Test for Product with only one page of reviews: https://www.amazon.com/MEROKEETY-Sleeve-Pullover-Blouses-Apricot/dp/B08KG4MMTV/ref=zg_bsnr_fashion_26?_encoding=UTF8&refRID=WE48MJ31KTKRHPT0RZX0&th=1&psc=1

# Find link to all reviews page
allReviewsPage = driver.find_element_by_css_selector('a.a-link-emphasis.a-text-bold').get_attribute('href')

# Get all reviews webpage
driver.get(allReviewsPage)
time.sleep(3)

#Get the number of pages of reviews for the product
temp = driver.find_element_by_xpath("//div[@data-hook='cr-filter-info-review-rating-count']/span").get_attribute('innerHTML')
mylist = temp.split(" ")
temp = mylist[27]
temp2 = int(temp.replace(",",""))
pages = math.ceil(temp2 / 10)

# Don't run unless necessary for testing, lots of get requests to the server. 
for i in range(pages):
	profileExists = True
	tmp = 0
	#Gets the profile url and product rating of each reviewer on a certain page
	while profileExists:
		profile = driver.find_elements_by_xpath("//div[contains(@id,'customer_review')]//div/a[@class='a-profile']")
		review = driver.find_elements_by_xpath("//div[@id='cm_cr-review_list']//i[contains(@class,'review-rating')]/span")
		profArr.append(profile[tmp].get_attribute('href'))
		ratingArr.append(review[tmp].get_attribute('innerHTML'))
		tmp += 1
		if(tmp == (len(profile))):
			profileExists = False
	#Checks if a next page of reviews exists and if so, accesses it
	if(pages != 1 and currPage != pages):
		nextPage = driver.find_element_by_xpath("//li[@class= 'a-last']//*[contains(@href, 'pageNumber')]").get_attribute('href')
		driver.get(nextPage)
		currPage += 1
	time.sleep(3)

#Goes through each reviewer's profile to get number of helpful votes and number of reviews
for i in range(len(profArr)):
	driver.get(profArr[i])
	time.sleep(3)
	helpful_Votes = driver.find_element_by_xpath("//div[contains(@id,'profile_')]//div[@class='dashboard-desktop-stats-section']/div[1]//div[@class='dashboard-desktop-stat-value']/span").get_attribute('innerHTML')
	numReviews = driver.find_element_by_xpath("//div[contains(@id,'profile_')]//div[@class='dashboard-desktop-stats-section']/div[2]//div[@class='dashboard-desktop-stat-value']/span").get_attribute('innerHTML')
	#Dictionary to organize data for each reviewer
	info_item = {
		"Rating": ratingArr[i],
		"Helpful Votes": helpful_Votes,
		"Number of Reviews": numReviews
	}
	info_list.append(info_item)

df = pd.DataFrame(info_list)

#Saves data to a csv file
df.to_csv('product_reviewers.csv')

#To look at the csv file, either find it in your computer's file management application (Ex. File Explorer for Windows)
# or in your terminal/command prompt type "product_reviewers.csv", making sure you are in the right directory

driver.quit()
