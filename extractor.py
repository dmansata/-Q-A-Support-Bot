from bs4 import BeautifulSoup
import re

def clean_text(text):
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_content(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Remove unwanted elements
    for element in soup(['script', 'style', 'nav', 'footer', 'iframe', 'noscript']):
        element.decompose()

    # Try to find main content area (heuristic)
    main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content') or soup.body

    if main_content:
        text = main_content.get_text(separator=' ')
    else:
        text = soup.get_text(separator=' ')

    return clean_text(text)
