import streamlit as st
from tools.scraper import scout_jobs

CSS = """
<style>
.job-card {
    background-color: #1e1e2e;
    border: 1px solid #313244;
    border-radius: 10px;
    padding: 16px;
    margin-bottom: 8px;
    transition: border-color 0.2s;
}
.job-card:hover {
    border-color: #89b4fa;
}
.job-card a {
    font-size: 1rem;
    font-weight: 600;
    color: #89b4fa;
    text-decoration: none;
}
.job-card a:hover {
    text-decoration: underline;
}
.job-number {
    font-size: 0.75rem;
    color: #6c7086;
    margin-bottom: 4px;
}
.job-company {
    font-size: 0.85rem;
    color: #a6adc8;
    margin-top: 6px;
}
.job-location {
    font-size: 0.8rem;
    color: #6c7086;
    margin-top: 3px;
}
.job-posted {
    font-size: 0.75rem;
    color: #585b70;
    margin-top: 3px;
}
</style>
"""


def run():
    st.set_page_config(page_title="Marketing Job Scout", layout="wide")

    st.markdown(CSS, unsafe_allow_html=True)

    # --- Sidebar ---
    with st.sidebar:
        st.header("Search Settings")
        keywords = st.text_input("Keywords", value="Marketing Design")
        num_results = st.slider("Results to show", min_value=1, max_value=25, value=10)
        search = st.button("Scout for Jobs", use_container_width=True)

    st.title("🎯 Live Marketing & Design Scout")
    st.caption("Powered by LinkedIn job search")

    if search:
        with st.spinner(f'Scouting LinkedIn for "{keywords}"...'):
            job_list = scout_jobs(keywords)

        if not job_list:
            st.error("LinkedIn is blocking the request. Try again later.")
        else:
            jobs = job_list[:num_results]
            st.success(f"Found {len(jobs)} results for **{keywords}**")

            # 2-column grid
            col1, col2 = st.columns(2)
            for i, job in enumerate(jobs):
                card_html = f"""
                <div class="job-card">
                    <div class="job-number">#{i + 1}</div>
                    <a href="{job['link']}" target="_blank">{job['title']}</a>
                    <div class="job-company">{job['company']}</div>
                    <div class="job-location">📍 {job['location']}</div>
                    <div class="job-posted">🗓 {job['posted']}</div>
                </div>
                """
                if i % 2 == 0:
                    col1.markdown(card_html, unsafe_allow_html=True)
                else:
                    col2.markdown(card_html, unsafe_allow_html=True)
