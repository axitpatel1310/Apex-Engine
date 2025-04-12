import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

def result(s):
    links = []
    text = []
    texts = []
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
    headers = {"user-agent": USER_AGENT}
    try:
        r = requests.get("https://www.google.com/search?q=" + s, headers=headers, timeout=5)
        r.raise_for_status()  # Raise exception for 4xx/5xx status codes
        soup = BeautifulSoup(r.content, "html.parser")
        for g in soup.find_all('div', class_='N54PNb BToiNc cvP2Ce'):
            a = g.find('a')
            t = g.find('h3')
            p = g.find('div', class_='VwiC3b yXK7lf lVm3ye r025kc hJNv6b Hdw6tb')
            if a and a.get('href'):
                links.append(a.get('href'))
            else:
                links.append('')
            if t:
                text.append(t.text)
            else:
                text.append('')
            if p:
                texts.append(p.text)
            else:
                texts.append('')
        return links, text, texts
    except RequestException as e:
        print(f"Error fetching results: {e}")
        return [], [], []  # Return empty lists to avoid crashing