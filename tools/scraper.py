import requests
from bs4 import BeautifulSoup


def scout_jobs(keywords="Marketing Design"):
    url = f"https://www.linkedin.com/jobs/search/?keywords={requests.utils.quote(keywords)}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    job_cards = soup.find_all('div', class_='base-card')
    results = []

    for card in job_cards:
        try:
            title = card.find('h3', class_='base-search-card__title').text.strip()
            link = card.find('a', class_='base-card__full-link')['href']
            company_tag = card.find('h4', class_='base-search-card__subtitle')
            company = company_tag.text.strip() if company_tag else "Unknown"
            location_tag = card.find('span', class_='job-search-card__location')
            location = location_tag.text.strip() if location_tag else "Location not listed"
            date_tag = card.find('time', class_='job-search-card__listdate')
            if not date_tag:
                date_tag = card.find('time', class_='job-search-card__listdate--new')
            posted = date_tag['datetime'] if date_tag and date_tag.get('datetime') else "Date not listed"
            results.append({"title": title, "link": link, "company": company, "location": location, "posted": posted})
        except:
            continue
    return results
