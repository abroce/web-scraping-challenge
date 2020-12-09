from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    
    executable_path = {'executable_path': "C:/chromedriver.exe"}
    browser = Browser('chrome', **executable_path)
    return browser

mars_info = {}

def scrape_mars_news():

    browser = init_browser()

    
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)

    response = requests.get(news_url)
    html = browser.html
    soup = BeautifulSoup(response.text, 'html.parser')

    news_title = soup.title.text
    news_p = soup.body.p.text
    mars_info["news_title"] = news_title
    mars_info["news_p"] = news_p
        
    return mars_info

def scrape_mars_image():

    browser = init_browser()

    
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    featured_image_url = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
    main_url = 'https://www.jpl.nasa.gov'
    
    featured_image_url = main_url + featured_image_url
    mars_info["featured_image_url"] = featured_image_url 
        
    return mars_info

def scrape_mars_facts():
    
    facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(facts_url)
    mars_df = tables[0]
    
    mars_df.columns = ['Parameter', 'Description']
    mars_df.set_index('Parameter', inplace = True)
    html_table = mars_df.to_html()
    mars_info["mars_facts"] = html_table

    return mars_info

def scrape_mars_hemispheres():
    browser = init_browser()
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    html = browser.html
    
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='item')
    hemisphere_img_urls = []
    for item in items:
        title = item.find('h3').text
        hemisphere_url = 'https://astrogeology.usgs.gov' + item.find('a', class_='itemLink product-item')['href']
        
        browser.visit(hemisphere_url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        hemisphere_img_url = 'https://astrogeology.usgs.gov' + soup.find('img', class_='wide-image')['src']
        hemisphere_img_urls.append({'title': title, 'img_url': hemisphere_img_url})
    mars_info["hemisphere_img_urls"] = hemisphere_img_urls
    
    return mars_info