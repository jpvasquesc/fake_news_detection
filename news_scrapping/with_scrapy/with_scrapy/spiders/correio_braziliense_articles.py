import scrapy
from pathlib import Path
import re

class CorreioBrazilienseArticlesSpider(scrapy.Spider):
    """
    Web scrapping 'spider', based on scrapy's 'Spider' class. 
    Built to scrap the text of news articles under the 'correiobraziliense.com.br' domain.   
    """
    
    name = 'correio_braziliense_articles'
    allowed_domains = ['correiobraziliense.com.br/']

    # Get links to the news articles from which the text will be scrapped
    links_path = Path("../../../links/correio_braziliense.txt")
    links_path.touch(exist_ok=True)
    with open(links_path, "r") as links_file:
        start_urls = list({link.strip() for link in links_file.readlines()})

    def parse(self, response):
        """
        Parse the text out of the HTML returned by a given web request response.
        Save page's text in a '.txt' file named after the article's title.
        """
        # HTML elements selectors
        PARAGRAPH_SELECTOR = "article.article p.texto"
        TEXT_SELECTOR = ".//text()"

        # Parse text
        text = []        
        for element in response.css(PARAGRAPH_SELECTOR):
            paragraph = ' '.join( [line.strip() for line in element.xpath(TEXT_SELECTOR).extract()])
            if paragraph:
                text.append(paragraph)

        # Get text file name from article's title
        title = response.css("div.materia-title > h1::text").get().lower().rstrip()
        underscore_separated = "_".join(title.split(" "))
        file_name = re.sub(r'\W+', '', underscore_separated)[0:50] # arbritary limit
        article_file = Path("../../../articles/correio_braziliense/{0}.txt".format(file_name))

        # Save text in a file
        article_file.touch(exist_ok=True)
        with open(article_file, "w", encoding="UTF-8") as f:
            f.write("{0}\n".format(response.request.url))
            f.write("\n".join(text))
