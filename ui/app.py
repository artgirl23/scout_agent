import streamlit as st
from tools.scraper import scout_jobs


def run():
    st.set_page_config(page_title="Marketing Job Scout")
    st.title("🎯 Live Marketing & Design Scout")

    if st.button("Scout for Jobs"):
        with st.spinner('Scouting LinkedIn...'):
            job_list = scout_jobs()
            if job_list:
                for i, job in enumerate(job_list[:10]):
                    st.markdown(f"**{i+1}.** [{job['title']}]({job['link']})")
            else:
                st.error("LinkedIn is blocking the request. Try again later.")
