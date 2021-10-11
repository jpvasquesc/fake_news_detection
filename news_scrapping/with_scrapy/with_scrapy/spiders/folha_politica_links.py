import scrapy
from pathlib import Path

class FolhaPoliticaLinksSpider(scrapy.Spider):
    """
    Web scrapping 'spider', based on scrapy's 'Spider' class. 
    Built to scrap links to news articles listed in the 'https://www.folhapolitica.org' webpage utilizing date indexing 'yyyy-mm' .   
    """
    name = 'folha_politica_links'
    allowed_domains = ['www.folhapolitica.org']
    
    # List of pages to scrape
    start_urls = ['https://www.folhapolitica.org/2021/10', 'https://www.folhapolitica.org/2021/09']

    def parse(self, response):
        """ 
        Parse the links to news artcles out of the HTML returned by the given web request response.
        Save all links in a '.txt' file.
        """
        # HTML elements selectors
        LINK_SELECTOR =  ".post.hentry > .jump-link > a::attr(href)"

        # Path to .txt file
        links_file_path = Path("../../../links/folha_politica.txt")
        links_file_path.touch(exist_ok=True)

        # Parse and save
        with open(links_file_path, "a") as links_file:
                for link in response.css(LINK_SELECTOR).getall():
                    links_file.write("{0}\n".format(link))