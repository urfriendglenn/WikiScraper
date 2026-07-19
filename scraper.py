import requests
from bs4 import BeautifulSoup
import random
from urllib.parse import urljoin
import sys

site = sys.argv[1]

def scrapeWikiArticle(url):
    response = requests.get(
        url=url,
        headers={
            "User-Agent": "wiki-scraper/1.0",
        },
        timeout=30,
    )
    if response.status_code == 404:
        return False
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.find(id="firstHeading")
    print(title.text)

    allLinks = soup.find(id="bodyContent").find_all("a")
    random.shuffle(allLinks)
    for link in allLinks:
        href = link.get("href")
        if (
            not href
            or "/wiki/" not in href
            or "new" in link.get("class", [])
            or "redlink=1" in href
        ):
            continue

        next_url = urljoin("https://en.wikipedia.org", href)
        if scrapeWikiArticle(next_url):
            return True

    return True

scrapeWikiArticle(site)
