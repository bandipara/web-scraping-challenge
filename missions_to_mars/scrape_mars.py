from bs4 import BeautifulSoup as bs
from splinter.browser import Browser
import pandas as pd
import requests as req
import time
#!which chromedriver

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    scrape_dict = {}

##Mars.Nasa.Gov
url = 'https://mars.nasa.gov/news/'
Browser.visit(url)

html = Browser.html
soup = bs(html, 'html.parser')

article = soup.find("div", class_='list_text')
article

#title of first news

news_title = article.find('div', class_="content_title").text

#paragraph of first news

news_para = article.find('div', class_="article_teaser_body").text

scrape_dict["news_title"]=news_title

scrape_dict["news_para"]=news_para
#JPL Mars Space Images

url_jpl = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(url_jpl)

#click Full Image button
browser.click_link_by_id('full_image')

#click more info
browser.click_link_by_partial_text('more info')

#soup_2 for JPL
html_2 = browser.html
soup_2 = bs(html_2, 'html.parser')

#image URL

feat_img_url = soup_2.find('figure', class_='lede').a['href']
feat_img_url

#complete image URL
featured_image_url = f'https://www.jpl.nasa.gov{feat_img_url}'
print(featured_image_url)

#Twitter Mars Weather

url_twtr = "https://twitter.com/marswxreport?lang=en"
browser.visit(url_twtr)

#soup_3 for twitter
html_3=browser.html
soup_3= bs(html_3,'html.parser')

tweet_url = "https://twitter.com/marswxreport?lang=en"
browser.visit(tweet_url)
html = browser.html

# Parse HTML with Beautiful Soup
soup = bs(html, 'html.parser')

# Extract latest tweet
tweet_container = soup.find_all('div', class_="js-tweet-text-container")

# Loop through latest tweets and find the tweet that has weather information
for tweet in tweet_container: 
    mars_weather = tweet.find('p').text
    if 'sol' and 'pressure' in mars_weather:
        print(mars_weather)
        break
    else: 
        pass

#Mars Facts
facts_url = "https://space-facts.com/mars/"
browser.visit(facts_url)
html = browser.html
table = pd.read_html(facts_url)
mars_facts = table[1]

# Rename columns
mars_facts.columns = ['Description','Value_mars','Value_earth']

# Reset Index to be description
mars_facts.set_index('Description', inplace=True)
fact_html = mars_facts.to_html('table.html')

# Mars Hemispheres

hemi_url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(hemi_url)
html=browser.html
soup = bs(html, "html.parser")



# Create dictionary to store titles & links to images
hemisphere_image_urls = []

# Retrieve all elements that contain image information
results = soup.find("div", class_ = "result-list" )
hemispheres = results.find_all("div", class_="item")

# Iterate through each image
for hemisphere in hemispheres:
    title = hemisphere.find("h3").text
    title = title.replace("Enhanced", "")
    end_link = hemisphere.find("a")["href"]
    image_link = "https://astrogeology.usgs.gov/" + end_link    
    browser.visit(image_link)
    html = browser.html
    soup = bs(html, "html.parser")
    downloads = soup.find("div", class_="downloads")
    image_url = downloads.find("a")["href"]
    hemisphere_image_urls.append({"title": title, "img_url": image_url})

# Print image title and url

#
    ### Store Data
    #

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts": mars_facts,
        "hemisphere_image_urls": hemisphere_image_urls
        }

    # Close the browser after scraping
    browser.quit()

    # Return results
    #return mars_data
    return scrape_dict
#if __name__ == '__main__':
    #scrape()