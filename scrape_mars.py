# Dependencies
import os
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests 
import pymongo
import flask_pymongo
from splinter import Browser #Choose the executable path to the driver when we use the splinter


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)
    
def scrape_info():
    browser = init_browser()
    
    #Create a Dictionary
    mars_data_dict = {}


    ##### VISIT NASA URL FOR NEWS #####
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)

    # Use BS to convert to HTML
    # Create Beautiful Soup Object
    news_html = browser.html

    # Parse HTML with Beautiful Soup
    news_soup = bs(news_html, 'html.parser')

    # Retrieve the title and news_paragraph
    news_title = news_soup.find('div', class_='content_title').text
    news_p = news_soup.find('div', class_='article_teaser_body').text

    # Store data in mars_data_dict
    mars_data_dict['newsTitle'] = news_title
    mars_data_dict['newsTag'] = news_p

    
    ##### VISIT JPL URL FOR MARS SPACE IMAGE #####
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)

    # Use BS to convert to HTML
    # Create Beautiful Soup Object 
    image_html = browser.html

    # Parse HTML with Beautiful Soup
    image_soup = bs(image_html, 'html.parser')

    # Retrieve background-image url 
    wallpaper_image_url  = image_soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

    # Website url 
    base_url = 'https://www.jpl.nasa.gov'

    # Concatenated url
    featured_image_url = base_url + wallpaper_image_url

    # Store data in mars_data_dict
    mars_data_dict['jplSpaceImage'] = featured_image_url

    
    ##### VISIT FOR TWITTER FOR WEATHER #####
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)

    # Use BS to convert to HTML
    # Create Beautiful Soup Object 
    weather_html = browser.html

    # Parse HTML with Beautiful Soup
    weather_soup = bs(weather_html, "html.parser")

    # Retrieve Mars Weather
    weather = weather_soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    # Store data in mars_data_dict
    mars_data_dict['weatherReport'] = weather
    
    
    ##### VISIT MARS FACTS URL FOR PROFILE #####
    # The assignment suggested we scrape the table from:
    profile_url = 'https://space-facts.com/mars/'
    # however, the site was intermittently down therefore utilized a profile table from another site.
    # profile_url = 'https://theplanets.org/mars/'

    # Get the table from the url
    profileTable = pd.read_html(profile_url)

    # Select the table from the url
    profile_df = profileTable[0]

    # Column Names
    profile_df.columns = ['Feature','Value']

    # Convert the data to a HTML table string
    htmlProfileTable = profile_df.to_html(classes = 'table table-striped')

    # Clean Up Unwanted New Lines
    htmlProfileTable.replace('\n', '')

    # Store data in mars_data_dict
    mars_data_dict['marsProfile'] = htmlProfileTable    


    ##### VISIT ASTROGEOLOGY URL FOR THE HEMISPHERES ##### 
    # Visit Astrogeology website for the hemispheres 
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)

    # Use BS to convert to HTML
    # Create Beautiful Soup Object
    hemispheres_html = browser.html

    # Parse HTML with Beautiful Soup
    hemispheres_soup = bs(hemispheres_html, 'html.parser')

    # Create empty list for hemisphere urls 
    hemispheres_image_urls = []

    # Create Variable for the hemisphere links
    hemispheres_links = browser.find_by_css('h3')

    # Create For Loop
    # i iterates through the length of hemispheres, 4
    for i in range(len(hemispheres_links)):
        # Create empty Dictionary
        hemispheres_dict = {}
        # Find the image on the hemispheres_url with class h3 and select it
        browser.find_by_css('h3')[i].click()
        
        # For the sample, select the title and image url
        sample_link = browser.find_link_by_text('Sample').first
        # Find the title on the specific hemisphere selected url with class h2 and select it 
        hemispheres_dict['title'] = browser.find_by_css('h2').text
        hemispheres_dict['img_url'] = sample_link['href']
        
        # Append the Value to the hemispheres_image_urls list
        hemispheres_image_urls.append(hemispheres_dict)
        
        # Go back so we can select the next sample hemisphere
        browser.back()
    
    # Store data in mars_data_dict
    mars_data_dict['hemispheres'] = hemispheres_image_urls

    # Close Browser
    browser.quit()

    # Return results
    return mars_data_dict

    # Print dictionary to confirm data is returning
    #print(mars_data_dict)

#Call on Function
#scrape_info()

# *Use Day 3 10_STU_SCRAPE_AND_RENDER + mission_to_mars.ipynb as template for this scrape_mars.py code.