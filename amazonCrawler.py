import unittest
import sys
import time
import math
import array
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from operator import attrgetter
import pandas as pd
import csv

# Function to calculate average 
def average(ratings):
	try:
		return sum(ratings) / len(ratings)
	except ZeroDivisionError:
		return 0

# Credibility Function to check if a reviewer is a credible source in general
def profile_credibility(helpful_votes, num_reviews):
	profile_score = 0
	benchmark = 1
	profile_score = int(helpful_votes) / int(num_reviews)
	
	if(profile_score >= benchmark):
		# the reviewer is credible 
		return 1
	else:
		# the reviewer isn't credible
		return 0

# Main
profArr = [] # array of profile links
tempRatingArr = [] # temp array of ratings
helpfulVotes_arr = [] # array of helpful votes of profile
numReviews_arr = [] # array of number of reviews of profile
newAvgScore_arr = array.array("f") # array of reviews to be counted
ratingArr = [] # array of each rating
info_list = [] 
currPage = 1

# Open up firefox browser
driver = webdriver.Chrome(executable_path="/Users/vivekbharadwaj/Desktop/ComputerNetworking/Project2/networkingprojects/chromedriver")


# Get item link from user input
webpageLink = input("Enter link to amazon product: ")

# Navigate to webpage
driver.get(webpageLink)

# Find link to all reviews page
allReviewsPage = driver.find_element_by_css_selector('a.a-link-emphasis.a-text-bold').get_attribute('href')

# Get all reviews webpage
driver.get(allReviewsPage)
totalReviews = driver.find_element_by_xpath("//div[@data-hook='cr-filter-info-review-rating-count']/span").get_attribute('innerHTML')

# Get total pages
mylist = totalReviews.split(" ")
totalReviews = mylist[27]
temp = int(totalReviews) 
pages = math.ceil(temp / 10)

# Don't run unless necessary for testing, lots of get requests to the server. 

# Loop total number of pages 
for i in range(pages):

	profileExists = True
	tmp = 0

	# Loop through profiles on each page
	while(profileExists):

		# Get profile links
		profile = driver.find_elements_by_xpath("//div[contains(@id,'customer_review')]//div/a[@class='a-profile']")
		if len(profile) > 0:
			profArr.append(profile[tmp].get_attribute('href'))
		else:
			profileExists = False
			break

		# Get and store all reviews in array 
		review = driver.find_elements_by_xpath("//div[@id='cm_cr-review_list']//i[contains(@class,'review-rating')]/span")
		tempRatingArr.append(review[tmp].get_attribute('innerHTML'))

		tmp += 1
		if(tmp == (len(profile))):
			profileExists = False

	if(pages != 1 and currPage != pages):

		nextPage = driver.find_element_by_xpath("//li[@class= 'a-last']//*[contains(@href, 'pageNumber')]").get_attribute('href')
		driver.get(nextPage)
		currPage += 1

	time.sleep(1)

# Get first value x in rating string: "x out of 5.0"
for i in range(len(tempRatingArr)):
	
	templist = tempRatingArr[i].split(" ")
	ratingArr.append(templist[0])

# Iterate through each profile to gather data for credibility function 
for i in range(len(profArr)):

	driver.get(profArr[i])
	time.sleep(2) # sleep to give time to load page and find element 

	try: 
		helpfulVotes = driver.find_element_by_xpath("//div[contains(@id,'profile_')]//div[@class='dashboard-desktop-stats-section']/div[1]//div[@class='dashboard-desktop-stat-value']/span").get_attribute('innerHTML')
		helpfulVotes_arr.append(helpfulVotes.replace(',', ''))
	except NoSuchElementException:
		helpfulVotes_arr.append(0)

	numReviews = driver.find_element_by_xpath("//div[contains(@id,'profile_')]//div[@class='dashboard-desktop-stats-section']/div[2]//div[@class='dashboard-desktop-stat-value']/span").get_attribute('innerHTML')
	numReviews_arr.append(numReviews.replace(',', ''))
	
	# Organizes data stored
	info_item = {
		"Rating": tempRatingArr[i],
		"Helpful Votes": helpfulVotes_arr[i],
		"Total Reviews": numReviews_arr[i]
	}
	info_list.append(info_item)

	if (profile_credibility(helpfulVotes_arr[i], numReviews_arr[i])) == 1: 
		newAvgScore_arr.append(float(ratingArr[i]))



df = pd.DataFrame(info_list)
#Saves data to a csv file
df.to_csv('productreviewers_2.csv') 

print("New average score is: ")
print(average(newAvgScore_arr))

driver.close()
# End of main 
