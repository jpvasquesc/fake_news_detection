import scrapy
from pathlib import Path
import re

class DiarioDoBrasilArticlesSpider(scrapy.Spider):
    """
    Web scrapping 'spider', based on scrapy's 'Spider' class. 
    Built to scrap the text of news articles under the 'diariodobrasil.org' domain.   
    """
    name = 'diario_do_brasil_articles'
    allowed_domains = ['diariodobrasil.org']

    # Get links to the news articles from which the text will be scrapped
    links_path = Path("../../../links/diario_do_brasil.txt")
    links_path.touch(exist_ok=True)
    with open(links_path, "r") as links_file:
        start_urls = list({link.strip() for link in links_file.readlines()})

    def parse(self, response):
        """
        Parse the text out of the HTML returned by a given web request response.
        Save page's text in a '.txt' file named after the article's title.
        """
        # HTML elements selectors
        PARAGRAPH_SELECTOR = ".post-content > *:not([id*='comments']) > *:not([class*='sharedaddy']):not([class*='535446a9c8b556bfa11394b020286a83'])"
        TEXT_SELECTOR = ".//text()"
        
        # parse
        text = []
        for element in response.css(PARAGRAPH_SELECTOR):
            paragraph = ' '.join( [line.strip() for line in element.xpath(TEXT_SELECTOR).extract()])
            if paragraph:
                text.append(paragraph)

        # Get text file name from article's title
        title = response.css("title::text").get().strip()
        underscore_separated = "_".join(title.split(" ")).lower()
        file_name = re.sub(r'\W+', '', underscore_separated)[0:50] # arbritary limit
        article_file = Path("../../../articles/diario_do_brasil/{0}.txt".format(file_name))

        # Save text in a file
        article_file.touch(exist_ok=True)
        with open(article_file, "w", encoding="UTF-8") as f:
            f.write("{0}\n".format(response.request.url))
            f.write("\n".join(text))