#!/usr/bin/env python
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

# Path to chromedriver
#!which chromedriver

# Windows users
#executable_path = {'executable_path': 'chromedriver.exe'}
#browser = Browser('chrome', **executable_path, headless=False)

def scrape_all():
   # Initiate headless driver for deployment
   browser = Browser("chrome", executable_path="chromedriver", headless=True)
   
   news_title, news_paragraph = mars_news(browser)
   
   # Run all scraping functions and store results in a dictionary
   data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": image_urls(browser)
   }

   # Stop webdriver and return data
   browser.quit()
   return data
   

# Visit the Quotes to Scrape site
#url = 'http://quotes.toscrape.com/'
#browser.visit(url)

# Parse the HTML
#html = browser.html
#html_soup = soup(html, 'html.parser')

# Scrape the Title
#title = html_soup.find('h2').text
#title

# Scrape the top ten tags
#tag_box = html_soup.find('div', class_='tags-box')
# tag_box
#tags = tag_box.find_all('a', class_='tag')

#for tag in tags:
#    word = tag.text
#    print(word)

#tags

#url = 'http://quotes.toscrape.com/'
#browser.visit(url)

#for x in range(1, 6):
#   html = browser.html
#   quote_soup = soup (html, 'html.parser')
#   quotes = quote_soup.find_all('span', class_='text')
#   for quote in quotes:
#      print('page:', x, '----------')
#      print(quote.text)
#   next = browser.links.find_by_partial_text('Next')
#   next.click()

# for x in range(1, 6):
#    html = browser.html
#    quote_soup = soup (html, 'html.parser')
#    quotes = quote_soup.find_all('div', class_='quote')
#    for quote in quotes:
#       print('page:', x, '----------')
#       print(quote.text)
#    browser.links.find_by_partial_text('Next')

# url = 'http://books.toscrape.com//'
# browser.visit(url)

# html = browser.html
# html_soup = soup(html, 'html.parser')

# # Scrape the book urls
# tag_box = html_soup.find('ol', class_='row')
# # tag_box
# tags = tag_box.find_all('a')

# for tag in tags:
#     word = tag.text
#     print(word)

# type(tags)

# type(tag_box)

# for link in html_soup.find_all('ol'):
#     #print(type(link))
#     for link1 in link.find_all('a'):
#         #print(type(link1))
#         tmp = link1.get('title')
#         if type(tmp) != None.__class__:
#             print(tmp)
#         #print(type(tmp))

def mars_news(browser):
    
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
    
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        #slide_elem.find("div", class_='content_title')
        
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
        #news_title
        
        # news_p = slide_elem.find_all('div', class_="article_teaser_body")
        # news_p[0].get_text()
        # for new in news_p:
        #     print(new.get_text())
        
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
        #news_p
    
    except AttributeError:
        return None, None
    
    return news_title, news_p

def featured_image(browser):
    # ### Featured Images
    # 
    
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    
    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()
    
    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()
    
    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
        #img_url_rel
        
    except AttributeError:
        return None
    
    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    #img_url
    return img_url

def mars_facts():
    try:
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None
    
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)
    
    return df.to_html()

def image_urls(browser):
    # Variable to hold list of dictionary items
    hemisphere_image_urls = []
    
    # base url for visiting liks and coming back
    base_url = 'https://astrogeology.usgs.gov'
    
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    
    html = browser.html
    thumb_soup = soup(html, 'html.parser')
    
    # Find all divs with class item
    # then find all div with class description 
    #   this gives hyperlink to the page and name of image
    # use the link as url and get to that new page
    # find the div with class downloads
    # then get the a and its href attribute for the full link of the image
    # build a dictionary and append the item to the list
    for href in thumb_soup.find_all('div', class_='item'):
        for item in href.find_all('div', class_='description'):
            tmpUrl = item.find('a').get('href')
            tmpName = item.find('h3').get_text()
            #print(tmpName)
            new_url = base_url + tmpUrl
            #print(new_url)
            browser.visit(new_url)
            htmln = browser.html
            full_soup = soup(htmln, 'html.parser')
            downlds = full_soup.find('div', class_='downloads')
            hyperLink = downlds.find('a').get('href')
            #print(hyperLink)
            dictI = {'img_url': hyperLink,
                     'title': tmpName}
            hemisphere_image_urls.append(dictI)
            browser.back()
    return hemisphere_image_urls
    
#browser.quit()
if __name__ == "__main__":
    
    # If running as script, print scraped data
    print(scrape_all())
