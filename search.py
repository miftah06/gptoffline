import requests
from bs4 import BeautifulSoup
import logging

def google_search(query):
    try:
        search_url = f"https://www.google.com/search?q={query}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        logging.debug(f"Response HTML: {soup.prettify()}")

        results = []
        for g in soup.find_all('div', class_='tF2Cxc'):
            link = g.find('a')['href']
            title = g.find('h3').text if g.find('h3') else 'No title'
            results.append({'title': title, 'link': link})

        if not results:
            logging.debug(f"No results found for query: {query}")
            raise ValueError("No results found")

        return results
    except requests.RequestException as e:
        logging.error(f"Request error occurred: {str(e)}")
        raise RuntimeError(f"Request error occurred: {str(e)}")
