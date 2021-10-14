import scrapy
from pathlib import Path

class JovenPanLinksSpider(scrapy.Spider):
    """
    Web scrapping 'spider', based on scrapy's 'Spider' class. 
    Built to scrap links to news articles, listed in the "http://jovempan.com.br/ultimas/' webpage.   
    """
    name = "jovem_pan_links"
    allowed_domains = ["jovempan.com.br"]
    
    # List of pages to scrape
    start_urls = ["http://jovempan.com.br/ultimas/"]
    MAX_PAGES = 4
    scrapped_pages = 0
    
    def parse(self, response):
        """
        Parse the links to news articles out of the HTML returned by the given web request response.
        Save all links in a '.txt' file.
        Make a web request for the next page.
        """
        # HTML elements selectors
        LINK_SELECTOR = "h2.post-title > a::attr(href)"
        
        # Path to .txt file
        links_file_path = Path("../../../links/jovem_pan.txt")
        links_file_path.touch(exist_ok=True)

        # Parse and save
        with open(links_file_path, "a") as links_file:
            for link in response.css(LINK_SELECTOR).getall():  
                links_file.write("{0}\n".format(link))

        # Scrape the link to the next page that lists articles
        NEXT_PAGE_SELECTOR = "ul.pagination > li > a[aria-label*='Próxima']::attr(href)"
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        
        # Make a web request to 'next_page'
        if next_page and (self.scrapped_pages <= self.MAX_PAGES):
            self.scrapped_pages += 1
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )
