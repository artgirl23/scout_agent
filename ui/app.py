import streamlit as st
from tools.scraper import scout_jobs

CSS = """
<style>
.job-card {
    background-color: #1e1e2e;
    border: 1px solid #313244;
    border-radius: 10px;
    padding: 16px 18px;
    margin-bottom: 10px;
    transition: border-color 0.2s;
}
.job-card:hover {
    border-color: #89b4fa;
}
.job-title a {
    font-size: 0.95rem;
    font-weight: 700;
    color: #89b4fa;
    text-decoration: none;
    line-height: 1.4;
}
.job-title a:hover {
    text-decoration: underline;
}
.job-meta {
    font-size: 0.8rem;
    color: #7f849c;
    margin-top: 5px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.job-badges {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
    margin-top: 10px;
}
.badge {
    font-size: 0.72rem;
    font-weight: 500;
    color: #a6e3a1;
    background-color: #1e3a2e;
    border-radius: 4px;
    padding: 2px 8px;
}
.job-posted {
    font-size: 0.7rem;
    color: #45475a;
    margin-top: 8px;
}
</style>
"""


def _badges_html(job_type: str) -> str:
    """Return badge HTML only for fields that have real values."""
    badges = []
    for value in job_type.split(" · "):
        value = value.strip()
        if value and value.lower() != "not specified":
            badges.append(f'<span class="badge">{value}</span>')
    if not badges:
        return ""
    return f'<div class="job-badges">{"".join(badges)}</div>'


def _card_html(job: dict) -> str:
    meta_parts = [job["company"]]
    if job["location"].lower() != "location not listed":
        meta_parts.append(job["location"])
    meta = " · ".join(meta_parts)

    posted = ""
    if job["posted"].lower() != "date not listed":
        posted = f'<div class="job-posted">🕐 {job["posted"]}</div>'

    return f"""
    <div class="job-card">
        <div class="job-title"><a href="{job['link']}" target="_blank">{job['title']}</a></div>
        <div class="job-meta">{meta}</div>
        {_badges_html(job['job_type'])}
        {posted}
    </div>
    """


def run():
    st.set_page_config(page_title="Marketing Job Scout", layout="wide")
    st.markdown(CSS, unsafe_allow_html=True)

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

            col1, col2 = st.columns(2)
            for i, job in enumerate(jobs):
                if i % 2 == 0:
                    col1.markdown(_card_html(job), unsafe_allow_html=True)
                else:
                    col2.markdown(_card_html(job), unsafe_allow_html=True)
