# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    # Set variables
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data

# Create a function to scrape mars_news.
# The variable "browser" will be defined outside of this function 
def mars_news(browser):

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

    # Add try/except for error handling
    try:

        slide_elem = news_soup.select_one('div.list_text')
        slide_elem.find('div', class_='content_title')

        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()


        # Use the parent element to find the summary for the first article
        news_paragraph = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None

    # Return the data
    return news_title, news_paragraph



# # Image Scraping

def featured_image(browser):

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
    
    # Add try/except for error handling
    try: 
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    # Return the image url
    return img_url


# # Mars Facts

def mars_facts():
    
    # Add try/except for error handling
    try: 
        # Create a dataframe from the first table found on this webpage
        df = pd.read_html('https://galaxyfacts-mars.com/')[0]
    
    # BaseException is a catchall, that is raised when any error is encountered.
    # Does not allow any user-defined exceptions
    except BaseException:
        return None

    # Add column names to df
    df.columns = ['description', 'Mars', 'Earth']
    # Set the index for the df
    df.set_index('description', inplace=True)

    # Convert df to html
    return df.to_html(classes="table table-striped")


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())
