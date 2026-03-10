import html
import requests
import streamlit as st
from bs4 import BeautifulSoup


def _text(tag) -> str:
    """Return clean plain text from a BeautifulSoup tag, stripping all HTML."""
    return html.escape(tag.get_text(separator=" ", strip=True)) if tag else ""


@st.cache_data(ttl=3600)
def scout_jobs(keywords="Marketing Design"):
    url = f"https://www.linkedin.com/jobs/search/?keywords={requests.utils.quote(keywords)}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    job_cards = soup.find_all('div', class_='base-card')
    results = []

    for card in job_cards:
        try:
            title = _text(card.find('h3', class_='base-search-card__title'))
            link = card.find('a', class_='base-card__full-link')['href']
            company = _text(card.find('h4', class_='base-search-card__subtitle')) or "Unknown"
            location = _text(card.find('span', class_='job-search-card__location')) or "Location not listed"
            date_tag = card.find('time', class_='job-search-card__listdate') or \
                       card.find('time', class_='job-search-card__listdate--new')
            posted = date_tag.get('datetime', '').strip() if date_tag else ""
            posted = posted if posted else "Date not listed"
            job_type_tags = card.find_all('span', class_='job-search-card__benefits-item')
            job_type = " · ".join(_text(t) for t in job_type_tags) if job_type_tags else "Not specified"
            results.append({"title": title, "link": link, "company": company, "location": location, "posted": posted, "job_type": job_type})
        except:
            continue
    return results
