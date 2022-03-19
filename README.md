# web-scraping-challenge
Repository for HW 12 - Web Scraping and Document Databases!

<!-- Thank you to Dr. Arrington for the walkthrough on this whole project! -->

## Step 1 - Scraping
* We start with a Jupyter Notebook file, 'mission_to_mars.ipynb'

    ## Inside the Jupyter Notebook
* We set up a connection to chromewebdriver so that Splinter can access our Chrome browser

* The first section is scraping the NASA Mars news site
    * We establish the url and implement a wait time and browser visit
    * We convert the browser html to a soup object with BeautifulSoup
    * We create a 'slide_elem' to use to '.find' the classes we want 
        - the news title ('content_title') text
        - and the paragraph ('article_teaser_body') text
        - these classes are found by investigating the web pages underlying HTML

* The second section is scraping the featured image and its url
    * We again establish the url and browser visit
    * We specify the 'button' tag as our target and ask Splinter to '.click()' it
    * We turn the HTML found into a soup object
    * We specify the 'fancybox-image' class as our next target, specifically it's 'src' (the link)
    * We save off that link as a variable and use it to return the webpage location of the image 

* The third section is scraping the facts page
    * Instead of establishing the url as a variable, we use the url to create a Pandas DataFrame using '.read_html()'
    * This allows us to have a table of the page data
    * We rename the columns and set the index
    * Then we re-convert the data in the DataFrame back to HTML

* The fourth and final section of the JN is scraping the hemispheres 
    * We again establish the url and browser visit
    * We create a for loop to look for the links of the hemispheres iamges and urls
        - We create an empty dictionary for the hemisphere info
        - We specify the img for '.click()'ing 
        - We grab the Sample img anchor tag to extract the href and add it to the dictionary
        - We extract the title by 'h2.title' text and add it to the dictionary


## Step 2 - MongoDB and Flask Application
* We use MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped from the URLs above
* We start by creating a a scrape Python file 'scrape_mars.py'

    ## In the 'scrape_mars.py' Python file

## scrape_all()
* First we create a 'scrape_all()' function that will hold all the scraping elements
    - These will be replications of the scraping we did in the JN file
    - In reality, this section was built out as the following functions were implemented,
    - but here it will be explained as it laid out in the code

    * First we set up Splinter to access Chrome
    * Next we define our "scrape_news(browser)" which pulls the information from the pages
        - This is the "news_title" and "news_paragraph"
    * Next we build a dictionary ('marsData') using the information we scrape out
        - newsTitle, newsParagraph, featuredImage, facts, hemispheres, lastUpdated
    * Then we tell the browser to stop and display our output

## scrape_news(browser)
* As previously stated, this is a replication of the news site scrape we did in the JN file

* We set up Splinter and BeautifulSoup to grab the news title and paragraph.

## scrape_feature_img(browser)
* We set up Splinter and BeautifulSoup to grab the featured image url

## scrape_facts_page(browser)
* This one is a little bit different since in the JN file we used a Pandas df
* Here, we set up Splinter and BeautifulSoup but we set it took for the 'diagram mt-4' class
    - This pulls the table that the data is set into
    - Then we append the text to an empty string

## scrape_hemispheres(browser)
* Here we return to the previous methodologies
* We set up Splinter and BeautifulSoup to grab the hemispehere image data


    ## In the 'app.py' Flask app file

* In this file we create a Flask app to run our scrapes and display the data a in visual format
* As well as to save the data to a MongoDB database

* First step is to create the app (app = Flask(__name__))
* Then we establish a connection to Mongo

* Next we create our app routes

## ("/") - index()
* We connect to Mongo and return the render_template for index.html and display our data

## ("/scrape")
* We create a table for our data in Mongo called 'marsTable'
* We drop the table if it exists
* We call the 'scrape_all()' script and insert the data into our table
* Then we redirect to our index page to see the results


And that's it! Thanks for reading :)