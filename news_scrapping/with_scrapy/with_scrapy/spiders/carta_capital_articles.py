import scrapy
from pathlib import Path
import re


class CartaCapitalArticlesSpider(scrapy.Spider):
    """
    Web scrapping 'spider', based on scrapy's 'Spider' class. 
    Built to scrap the text of news articles under the 'www.cartacapital.com.br' domain.   
    """
    name = 'carta_capital_articles'
    allowed_domains = ['www.cartacapital.com.br']

    # Get links to the news articles from which the text will be scrapped
    links_path = Path("../../../links/carta_capital.txt")
    links_path.touch(exist_ok=True)
    with open(links_path, "r") as links_file:
        start_urls = list({link.strip() for link in links_file.readlines()})

    def parse(self, response):
        """
        Parse the text out of the HTML returned by a given web request response.
        Save page's text in a '.txt' file named after the article's title.
        """
        # HTML elements selectors
        PARAGRAPH_SELECTOR = ".eltdf-post-text-inner > :not(div):not([class*='telegram-notice']):not([class*=leia-tbm])"
        TEXT_SELECTOR = ".//text()"

        # Parse text
        text = []
        for element in response.css(PARAGRAPH_SELECTOR):
            paragraph = ' '.join( [line.strip() for line in element.xpath(TEXT_SELECTOR).extract()])
            if paragraph:
                text.append(paragraph)

        # Get text file name from article's title
        title = response.css("title::text").get().lower().rstrip()
        underscore_separated = "_".join(title.split(" "))
        file_name = re.sub(r'\W+', '', underscore_separated)[0:50] # arbritary limit
        article_file = Path("../../../articles/carta_capital/{0}.txt".format(file_name))

        # Save text in .txt file
        article_file.touch(exist_ok=True)
        with open(article_file, "w", encoding="UTF-8") as f:
            f.write("{0}\n".format(response.request.url))
            f.write("\n".join(text))
