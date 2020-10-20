#!/usr/bin/env python
# coding: utf-8

# In[1]:


from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd


# In[2]:


# Path to chromedriver
get_ipython().system('which chromedriver')


# In[3]:


# Windows users
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# In[4]:


# Visit the Quotes to Scrape site
url = 'http://quotes.toscrape.com/'
browser.visit(url)


# In[5]:


# Parse the HTML
html = browser.html
html_soup = soup(html, 'html.parser')


# In[6]:


# Scrape the Title
title = html_soup.find('h2').text
title


# In[7]:


# Scrape the top ten tags
tag_box = html_soup.find('div', class_='tags-box')
# tag_box
tags = tag_box.find_all('a', class_='tag')

for tag in tags:
    word = tag.text
    print(word)


# In[8]:


tags


# In[9]:


url = 'http://quotes.toscrape.com/'
browser.visit(url)


# In[10]:


for x in range(1, 6):
   html = browser.html
   quote_soup = soup (html, 'html.parser')
   quotes = quote_soup.find_all('span', class_='text')
   for quote in quotes:
      print('page:', x, '----------')
      print(quote.text)
   next = browser.links.find_by_partial_text('Next')
   next.click()


# In[11]:


for x in range(1, 6):
   html = browser.html
   quote_soup = soup (html, 'html.parser')
   quotes = quote_soup.find_all('div', class_='quote')
   for quote in quotes:
      print('page:', x, '----------')
      print(quote.text)
   browser.links.find_by_partial_text('Next')


# In[12]:


url = 'http://books.toscrape.com//'
browser.visit(url)


# In[13]:


html = browser.html
html_soup = soup(html, 'html.parser')


# In[14]:


# Scrape the book urls
tag_box = html_soup.find('ol', class_='row')
# tag_box
tags = tag_box.find_all('a')

for tag in tags:
    word = tag.text
    print(word)


# In[15]:


type(tags)


# In[16]:


type(tag_box)


# In[17]:


for link in html_soup.find_all('ol'):
    #print(type(link))
    for link1 in link.find_all('a'):
        #print(type(link1))
        tmp = link1.get('title')
        if type(tmp) != None.__class__:
            print(tmp)
        #print(type(tmp))
            


# In[18]:


# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[19]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')


# In[20]:


slide_elem.find("div", class_='content_title')


# In[21]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# In[22]:


news_p = slide_elem.find_all('div', class_="article_teaser_body")
news_p[0].get_text()
for new in news_p:
    print(new.get_text())


# In[23]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# ### Featured Images
# 

# In[24]:


# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# In[25]:


# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()


# In[26]:


# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()


# In[27]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[28]:


# Find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel


# In[29]:


# Use the base URL to create an absolute URL
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url


# In[30]:


df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns=['description', 'value']
df.set_index('description', inplace=True)
df


# In[31]:


df.to_html()


# In[32]:


browser.quit()


# # Module 10 Challenge Starts

# In[2]:


# Import Splinter, BeautifulSoup, and Pandas
#from splinter import Browser
#from bs4 import BeautifulSoup as soup
#import pandas as pd

# Already imported above so commented this code


# In[27]:


# Path to chromedriver
get_ipython().system('which chromedriver')


# In[28]:


# Windows users
executable_path = {'executable_path': 'c:\\chromedriver_win32\\chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# In[4]:


# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[5]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('ul.item_list li.slide')


# In[6]:


slide_elem.find("div", class_='content_title')


# In[7]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# In[8]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# ### JPL Space Images Featured Image

# In[9]:


# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# In[10]:


# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()


# In[11]:


# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()


# In[12]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[13]:


# find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel


# In[14]:


# Use the base url to create an absolute url
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url


# ### Mars Facts

# In[15]:


df = pd.read_html('http://space-facts.com/mars/')[0]

df.head()


# In[16]:


df.columns=['Description', 'Mars']
df.set_index('Description', inplace=True)
df


# In[17]:


df.to_html()


# ### Mars Weather

# In[18]:


# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)


# In[19]:


# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')


# In[20]:


# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
# ### Hemispheres

# In[21]:


# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[22]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []
base_url = 'https://astrogeology.usgs.gov'

# 3. Write code to retrieve the image urls and titles for each hemisphere.
html = browser.html
thumb_soup = soup(html, 'html.parser')
#thumbs = thumb_soup.find_all('a', class_='itemLink')
#print(thumbs)

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


# In[23]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[24]:


# 5. Quit the browser
browser.quit()


# In[ ]:




