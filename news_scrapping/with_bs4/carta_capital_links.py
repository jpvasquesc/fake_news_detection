"""
Get the links for news articles listed in the page "https://www.cartacapital.com.br/mais-recentes/".
This page uses a AJAX requests for infinte scrolling.
"""

import argparse
import requests
from bs4 import BeautifulSoup
from pathlib import Path

def parse_input_arguments():
    """
    Create a command-line menu for this script using 'argparse'.
    """
    parser = argparse.ArgumentParser(prog="'Carta Capital' articles scrapping",
                                     description="Scrape the webpage 'diariodobrasil.org/todas-materias/' for links of the most recent posts")
    parser.add_argument('-p','--pages', dest='p', type=int, default=5, help="Number of pages to scrape")
    return parser.parse_args()

def get_article_listing_page(page: int):
    """
    Get the HTML for the article listing page
    """
    form_data={"next_page": str(page),
            "max_pages": "4152",
            "paged": str(page),
            "pagination_type": "load-more",
            "display_pagination": "yes",
            "display_excerpt": "no",
            "display_comments": "no",
            "display_author": "yes",
            "display_category": "yes",
            "display_date": "yes",
            "thumb_image_size": "full-mobile",
            "number_of_posts": "10",
            "parallax_effect": "no",
            "base": "eltdf_post_layout_three",
            "action": "readanddigest_list_ajax",}
    page_request = requests.post("https://www.cartacapital.com.br/wp-admin/admin-ajax.php", data=form_data)
    html = BeautifulSoup(page_request.json()["html"], features="lxml")
    return html

def get_links(html):
    """
    Parse links out of html and save in a '.txt' file.
    """
    # Create file
    txt_path = Path("../../news_scrapping/links/carta_capital.txt")
    txt_path.touch(exist_ok=True)

    # Parse and save
    with open(txt_path, "a") as txt_file:
        links_list = [a_tag['href'] for a_tag in html.find_all('a', {"class": "eltdf-pt-link"}, href=True)]
        for link in links_list:
            txt_file.write("{0}\n".format(link))
    
    return len(links_list)

def main():
    """
    Get the links for articles listed in the first 'args.p' pages from the webpage "https://www.cartacapital.com.br/mais-recentes/".
    """
    args = parse_input_arguments()
    
    num_links = 0
    for page in range(1, args.p+1):
        html = get_article_listing_page(page)
        num_links += get_links(html)
        print("Parsed page {0}".format(page))
    
    print("Done! Saved {0} links from the page 'https://www.cartacapital.com.br/mais-recentes/'.".format(num_links))

if __name__ == "__main__":
    main()