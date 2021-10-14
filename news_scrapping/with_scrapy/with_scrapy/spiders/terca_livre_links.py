import scrapy
from pathlib import Path

class TercaLivreSpider(scrapy.Spider):
    """
    Web scrapping 'spider', based on scrapy's 'Spider' class. 
    Built to scrap links to news articles, listed in the 'https://tercalivre.com.br/mais-noticias' webpage.   
    """
    name = 'terca_livre_links'
    allowed_domains = ['tercalivre.com.br']
    
    # List of pages to scrape
    start_urls = ['https://tercalivre.com.br/mais-noticias/page/{0}/'.format(page) for page in range(1,7)]

    def parse(self, response):
        """
        Parse the links to news articles out of the HTML returned by the given web request response.
        Save all links in a '.txt' file.
        """
        # HTML elements selectors
        LINK_SELECTOR = "h2.entry-title > a::attr(href)"
        
        # Path to .txt file
        links_file_path = Path("../../../links/terca_livre.txt")
        links_file_path.touch(exist_ok=True)

        # Parse and save
        with open(links_file_path, "a") as links_file:
            for link in response.css(LINK_SELECTOR).getall():  
                links_file.write("{0}\n".format(link))
