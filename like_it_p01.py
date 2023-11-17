# imports
import requests
from bs4 import BeautifulSoup
import threading  # Import the threading module
from unidecode import unidecode

# Define the scrape_comments function outside search
def scrape_comments(link_produto, comments):
    response = requests.get(link_produto)
    soup_produto = BeautifulSoup(response.text, 'html.parser')

    # Enters the html class responsible for the list of comments
    avaliacoes = soup_produto.find_all('article', class_='ui-review-capability-comments__comment')

    # Enters the html class responsible for each of the comments, storing them in the comments list
    for avaliacao in avaliacoes:
        comment_text = avaliacao.find('p', {'class': 'ui-review-capability-comments__comment__content'}).text.strip()
        comments.append(comment_text)

def search(product):
    # Makes a request in the free market search tool and generates the html of the page with what was typed by the user
    url = f'https://lista.mercadolivre.com.br/{product}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # elects the items suggested by the free market, based on the search
    produtos = soup.select('.ui-search-layout__item')
    comments = []

    # Create a list to hold threads
    threads = []
    
    # Iterate over the products and create a thread for each
    for produto in produtos:
        link_produto = produto.select_one('.ui-search-link')['href']
        thread = threading.Thread(target=scrape_comments, args=(link_produto, comments))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()
    
    def remove_accents(list):
        return [unidecode(i) for i in list]
    
    comments = remove_accents(comments)


    nova_lista = [palavra.replace('\n', '') for palavra in comments]

    comments = [x for x in nova_lista if x != '']


    comments = comments[:20] # used to limit
    return comments

