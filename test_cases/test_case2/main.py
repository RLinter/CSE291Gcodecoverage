# pip install requests beautifulsoup4 pytest requests-mock


import requests
from bs4 import BeautifulSoup

def fetch_page_title(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
        title_tag = soup.find('title')
        return title_tag.text if title_tag else 'No title found'
    except requests.RequestException as e:
        return f"Error: {str(e)}"
