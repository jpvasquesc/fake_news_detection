import scrapy
from pathlib import Path

class G1LinksSpider(scrapy.Spider):
    """
    Web scrapping 'spider', based on scrapy's 'Spider' class. 
    Built to scrap links to news articles listed in the 'https://g1.globo.com/' webpage.   
    """

    name = 'g1_links'
    allowed_domains = ['g1.globo.com']
    
    # List of pages to scrape
    start_urls = ['https://g1.globo.com/']
    MAX_PAGES = 10
    scrapped_pages = 1
    
    def parse(self, response):
        """
        Parse the links to news artcles out of the HTML returned by the given web request response.
        Save all links in a '.txt' file.
        Make a web request for the next page.
        """
        # HTML elements selectors
        LINK_SELECTOR =  "a.feed-post-link::attr(href)"
        
        # Path to .txt file
        links_file_path = Path("../../../links/g1.txt")
        links_file_path.touch(exist_ok=True)

        # Parse and save
        with open(links_file_path, "a") as links_file:
            for link in response.css(LINK_SELECTOR).getall():                
                if link and "especiais" not in link and "video" not in link:
                    links_file.write("{0}\n".format(link))

        # Scrape the link to the next page that lists articles
        NEXT_PAGE_SELECTOR = '.load-more a ::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        
        # Make a web request to 'next_page'
        if next_page and self.scrapped_pages < self.MAX_PAGES:
            self.scrapped_pages += 1
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )