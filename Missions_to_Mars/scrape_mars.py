# import splinter, beautiful soup, and chrome driver
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt

# scrape all function
def scrape_all():
    # Set up Splinter
    executable_path = {'executable_path': 'C:/Users/Joshua/Downloads/chromedriver_win32/chromedriver.exe'}
    browser = Browser('chrome', **executable_path)

    # the goal is to return a json that has all of the necessary data, so that it can be loaded into MongoDB

    # get the information from the news page
    news_title, news_paragraph = scrape_news(browser)

    # build a dictionary using the information from the scrapes
    marsData = {
        "newsTitle": news_title,
        "newsParagraph": news_paragraph,
        "featuredImage": scrape_feature_img(browser),
        "facts": scrape_facts_page(browser),
        "hemispheres": scrape_hemispheres(browser),
        "lastUpdated": dt.datetime.now()
    }

    # stop the webdriver
    browser.quit()

    # display output
    return marsData

# scrape the mars news page (previously created code from mission_to_mars.ipynb file)
def scrape_news(browser):
    # Visit the Mars news sit
    mars_news_url = 'https://redplanetscience.com'
    browser.visit(mars_news_url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time = 1)

    # Conver the browser html to a soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')

    slide_elem = news_soup.select_one('div.list_text')

    # grab the current title content
    slide_elem.find('div', class_='content_title')

    # Use the parent element to find the first tag and save it as 'news_title'
    news_title = slide_elem.find('div', class_='content_title').get_text()

    # Use the parent element to find the paragraph text
    news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    # return the title and the paragraph
    return news_title, news_p

# scrape through the featured image page
def scrape_feature_img(browser):
    # Visit featured image url
    featured_image_url = 'https://spaceimages-mars.com'
    browser.visit(featured_image_url)

    # Find and click the full image button
    full_image_link = browser.find_by_tag('button')[1]
    full_image_link.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Find the relative image url
    img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    # return the image url
    return img_url

# scrape through the facts page
def scrape_facts_page(browser):
    # Visit facts page url
    mars_facts_url = 'https://galaxyfacts-mars.com'
    browser.visit(mars_facts_url)

    # Convert the browser html to a soup object
    html = browser.html
    facts_soup = soup(html, 'html.parser')

    # find the facts location
    factsLocation = facts_soup.find('div', class_="diagram mt-4")

    # grab the html code for the fact table
    factTable = factsLocation.find('table')

    # create an empty string
    facts = ""

    # add the text to the empty string
    facts += str(factTable)

    # return
    return facts


# scrape through the hemispheres pages
def scrape_hemispheres(browser):
    # Visit hemispheres page url
    hemispheres_url = 'https://marshemispheres.com'
    browser.visit(hemispheres_url)

    # Create a list to hold the images and titles
    hemisphere_image_urls = []

    # set up the loop
    for i in range(4):

        # loop through each of the pages
        # hemisphere info dictionary
        hemisphereInfo = {}
        
        # We have to find the elements on each loop to avoid a stale element exception
        browser.find_by_css('a.product-item img')[i].click()
        
        # Next, we find the Sample image anchor tag and extract the href
        sample = browser.links.find_by_text('Sample').first
        hemisphereInfo['img_url'] = sample['href']
        
        # Get Hemisphere title
        hemisphereInfo['title'] = browser.find_by_css('h2.title').text
        
        # Append hemisphere object to list
        hemisphere_image_urls.append(hemisphereInfo)
        
        # Finally, we navigate backwards
        browser.back()
    
    # return hemisphere urls with titles
    return hemisphere_image_urls

    # # Convert the browser html to a soup object
    # html = browser.html
    # facts_soup = soup(html, 'html.parser')

if __name__ == "__main__":
    print(scrape_all())
