# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Set up the browser
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# # Article Scrapping
# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# Set up html parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')
slide_elem.find('div', class_='content_title')

# Use the parent element to find the first 'a' tag and save it as 'news_title'
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the summary for the first article
news_summary = slide_elem.find('div', class_='article_teaser_body').get_text()
news_summary


# # Image Scraping
# Visit the mars nasa news site
url = 'https://spaceimages-mars.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# # Mars Facts
# Create a dataframe from the first table found on this webpage
df = pd.read_html('https://galaxyfacts-mars.com/')[0]
# Add column names to df
df.columns = ['description', 'Mars', 'Earth']
# Set the index for the df
df.set_index('description', inplace=True)
df

# Convert df to html
df.to_html()

# Quit the automated browser
browser.quit()
