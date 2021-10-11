import scrapy
from pathlib import Path

class CorreioBrazilienseLinksSpider(scrapy.Spider):
    """
    Web scrapping 'spider', based on scrapy's 'Spider' class. 
    Built to scrap links to news articles, listed in the 'https://www.correiobraziliense.com.br/ultimas-noticias' webpage.   
    """
    name = 'correio_braziliense_links'
    allowed_domains = ['correiobraziliense.com.br/']
    
    # List of pages to scrape
    MAX_PAGES = 5 
    start_urls = ['https://www.correiobraziliense.com.br/webparts/98/7/{0}/'.format(page) for page in range(1, MAX_PAGES)]

    def parse(self, response):
        """
        Parse the links to news artcles out of the HTML returned by the given web request response.
        Save all links in a '.txt' file.
        """
        # HTML elements selectors
        LINK_SELECTOR =  "li > a::attr(href)"

        # Path to .txt file
        links_file_path = Path("../../../links/correio_braziliense.txt")
        links_file_path.touch(exist_ok=True)

        # Parse and save
        with open(links_file_path, "a") as links_file:
            for link in response.css(LINK_SELECTOR).getall():
                links_file.write("https://www.correiobraziliense.com.br/{0}\n".format(link))