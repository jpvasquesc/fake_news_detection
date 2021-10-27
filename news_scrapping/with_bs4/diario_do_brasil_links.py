"""
Get the links for new posts listed in the page "https://diariodobrasil.org/todas-materias/".
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
    parser = argparse.ArgumentParser(prog="'Diario do Brasil' posts scrapping",
                                     description="Scrape the webpage 'diariodobrasil.org/todas-materias/' for links of the most recent posts")
    
    parser.add_argument('security_token', type=str, help="Connection security token that updates daily.\
                                                          How to find this token:\n\
                                                          1 - While in the page 'https://diariodobrasil.org/todas-materias/', open your web browser's Dev Tools.\n\
                                                          2 - Go to the 'Network' tab.\n\
                                                          3 - Click the 'ver mais...' button at the bottom of the webpage.\n\
                                                          4 - A process named 'admin-ajax.php' should appear, click on it.\n\
                                                          5 - In the 'Headers' tab, find the 'Form Data' section.\n\
                                                          6 - Under 'Form Data', find 'nonce:', the value at it's side is the security token.\n\
                                                          Token example: '5b355af4ca'")

    parser.add_argument('-p','--pages', dest='p', type=int, default=5, help="Number of pages to scrape")
    return parser.parse_args()

def get_article_listing_page(page: int, security_token: str):
    """
    Get the HTML for the post listing webpage.
    """
    form_data = {'action': 'load_more',
                    "class": r"Essential_Addons_Elementor\Elements\Post_Grid",
                    "args": "orderby=date&order=desc&ignore_sticky_posts=1&post_status=publish&posts_per_page=32&offset=15&post_type=post",
                    "page": str(page),
                    "page_id": "245827",
                    "widget_id": "ebb0ef2", 
                    "nonce": security_token, # This value seems to updates daily
                    "template_info[dir]": "lite",
                    "template_info[file_name]": "default.php",
                    "template_info[name]": "Post-Grid"}
    page_request = requests.post("https://diariodobrasil.org/wp-admin/admin-ajax.php", data=form_data)
    response = page_request.json()

    if type(response) == str:
        html = BeautifulSoup(response, features="lxml")
        return html
    raise ValueError("Wrong security token. Please check if when you click the 'ver mais...' button, more posts are loaded or not.")
def get_links(html):
    """
    Parse post's links out of html and save in a '.txt' file.
    """
    # Create file
    txt_path = Path("../../news_scrapping/links/diario_do_brasil.txt")
    txt_path.touch(exist_ok=True)

    # Parse and save
    with open(txt_path, "a") as txt_file:
        links_list = [a_tag['href'] for a_tag in html.find_all('a', {"class": "eael-grid-post-link"}, href=True)]
        for link in links_list:
            txt_file.write("{0}\n".format(link))
    
    return len(links_list)

def main():
    """
    Get the links for posts listed in the first 'PAGES' pages from the webpage "https://diariodobrasil.org/todas-materias/".
    """
    
    args = parse_input_arguments()
    
    num_links = 0
    for page in range(1, args.p):
        html = get_article_listing_page(page, args.security_token)
        num_links += get_links(html)
        print("Parsed page {0}".format(page))
    
    print("Done! Saved {0} links from the page 'https://diariodobrasil.org/todas-materias/'.".format(num_links))

if __name__ == "__main__":
    main()