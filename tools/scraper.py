import requests
from bs4 import BeautifulSoup


def scout_jobs():
    url = "https://www.linkedin.com/jobs/search/?keywords=Marketing%20Design"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    job_cards = soup.find_all('div', class_='base-card')
    results = []

    for card in job_cards:
        try:
            title = card.find('h3', class_='base-search-card__title').text.strip()
            link = card.find('a', class_='base-card__full-link')['href']
            results.append({"title": title, "link": link})
        except:
            continue
    return results
