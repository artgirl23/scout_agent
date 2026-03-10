import csv
import io
import streamlit as st
from tools.scraper import scout_jobs

CSS = """
<style>
.job-title-link a {
    font-size: 1rem;
    font-weight: 700;
    color: #89b4fa !important;
    text-decoration: none;
}
.job-title-link a:hover {
    text-decoration: underline;
}
.badge-row {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
    margin-top: 2px;
}
.badge {
    font-size: 0.72rem;
    font-weight: 500;
    color: #a6e3a1;
    background-color: #1e3a2e;
    border-radius: 4px;
    padding: 2px 8px;
}
</style>
"""

CSV_FIELDS = ["title", "company", "location", "posted", "job_type", "link"]


def _to_csv(jobs: list[dict]) -> str:
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=CSV_FIELDS, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(jobs)
    return buf.getvalue()


def _render_card(job: dict) -> None:
    with st.container(border=True):
        # Title — linked
        st.markdown(
            f'<div class="job-title-link"><a href="{job["link"]}" target="_blank">{job["title"]}</a></div>',
            unsafe_allow_html=True,
        )

        # Company · Location on one muted line
        meta_parts = [job["company"]]
        if job["location"].lower() != "location not listed":
            meta_parts.append(job["location"])
        st.caption(" · ".join(meta_parts))

        # Job type badges — only if real values exist
        badges = [
            v.strip() for v in job["job_type"].split(" · ")
            if v.strip() and v.strip().lower() != "not specified"
        ]
        if badges:
            badge_html = "".join(f'<span class="badge">{b}</span>' for b in badges)
            st.markdown(
                f'<div class="badge-row">{badge_html}</div>',
                unsafe_allow_html=True,
            )

        # Posted date — most subtle, only if present
        if job["posted"].lower() != "date not listed":
            st.markdown(
                f"<small style='color:#45475a;'>🕐 {job['posted']}</small>",
                unsafe_allow_html=True,
            )


def run():
    st.set_page_config(page_title="Marketing Job Scout", layout="wide")
    st.markdown(CSS, unsafe_allow_html=True)

    if "job_results" not in st.session_state:
        st.session_state.job_results = []

    with st.sidebar:
        st.header("Search Settings")

        if st.session_state.job_results:
            st.download_button(
                label="⬇️ Download Results as CSV",
                data=_to_csv(st.session_state.job_results),
                file_name="scout_results.csv",
                mime="text/csv",
                use_container_width=True,
            )
            st.divider()

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
            st.session_state.job_results = job_list[:num_results]

    jobs = st.session_state.job_results
    if jobs:
        st.success(f"Found {len(jobs)} results for **{keywords if search else ''}**")
        col1, col2 = st.columns(2)
        for i, job in enumerate(jobs):
            with col1 if i % 2 == 0 else col2:
                _render_card(job)
