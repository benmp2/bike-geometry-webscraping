import urllib
from bs4 import BeautifulSoup

class base_scraper():

    def __init__(self, site_url):
        
        self.site_url=site_url
        self.soup = None
        self.set_soup()
        
        
    def set_soup(self):
    
        # query the website and return the html to the variable ‘page’
        try:
            page = urllib.request.urlopen(self.site_url)
        except:
            print('unable to load url')
        
        # parse the html using beautiful soup and store in variable 'soup'
        try:
            self.soup = BeautifulSoup(page, 'html.parser')
        except:
            print("BeautifulSoup unable to parse the website's html")