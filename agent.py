import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Marketing Job Scout")
st.title("🎯 Live Marketing & Design Scout")

def scout_jobs():
    url = "https://www.linkedin.com/jobs/search/?keywords=Marketing%20Design"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Targeting the job card containers
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

if st.button("Scout for Jobs"):
    with st.spinner('Scouting LinkedIn...'):
        job_list = scout_jobs()
        if job_list:
            for i, job in enumerate(job_list[:10]):
                st.markdown(f"**{i+1}.** [{job['title']}]({job['link']})")
        else:
            st.error("LinkedIn is blocking the request. Try again later.")