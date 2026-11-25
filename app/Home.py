import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent))

st.set_page_config(
    page_title="Irish Social Attitudes 2023 — ESS Round 11",
    page_icon="\U0001F1EE\U0001F1EA",
    layout="wide",
)

st.title("Irish Social Attitudes: 2023")
st.caption("Interactive exploration of Round 11 of the European Social Survey (ESS) in Ireland")

st.markdown(
    """
This dashboard turns the University College Dublin *Irish Social Attitudes: 2023* report and its
underlying data into interactive insights. Every page tracks how Irish public opinion has moved
across ESS rounds 1–11 (2002–2023), and breaks the latest wave down by education, age, gender,
employment, income and urban/rural residence where the data allows it.

Use the sidebar to move between topics.
"""
)

st.divider()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Sample issued", "3,930")
col2.metric("Completed interviews", "≈2,075")
col3.metric("Response rate", "52.8%")
col4.metric("Fieldwork", "Jun 2023 – Jan 2024")

st.divider()

st.subheader("What's covered")

# Colour palette matches the European Social Survey's own brand
# (verified from europeansocialsurvey.org / ess.sikt.no CSS custom properties):
# red #AD1400, hover/dark red #670000, black #141414.
topics = [
    ("Trust", "Trust"),
    ("Trust in Institutions", "Trust_in_Institutions"),
    ("Health & Health Services", "Health_and_Health_Services"),
    ("Europe", "Europe"),
    ("Life Satisfaction & Happiness", "Life_Satisfaction_and_Happiness"),
    ("Economic Satisfaction", "Economic_Satisfaction"),
    ("Immigration", "Immigration"),
    ("Religion", "Religion"),
    ("Climate Change", "Climate_Change"),
    ("Gender", "Gender"),
    ("COVID-19", "COVID-19"),
    ("Precarity", "Precarity"),
]
tiles_html = "".join(
    f'<a class="ess-tile" href="/{slug}" target="_self">{name}</a>' for name, slug in topics
)
st.markdown(
    f"""
    <style>
    .ess-tile-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
        gap: 12px;
        margin: 8px 0 24px 0;
    }}
    .ess-tile {{
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        min-height: 64px;
        padding: 18px 14px;
        border-radius: 8px;
        background-color: #AD1400;
        color: #ffffff !important;
        font-weight: 600;
        font-size: 1rem;
        text-decoration: none !important;
        transition: background-color 0.15s ease;
    }}
    .ess-tile:hover {{
        background-color: #670000;
    }}
    </style>
    <div class="ess-tile-grid">{tiles_html}</div>
    """,
    unsafe_allow_html=True,
)

st.divider()

with st.expander("About the survey"):
    st.markdown(
        """
The European Social Survey (ESS) is a cross-national survey run every two years across Europe.
Round 11 fieldwork in Ireland ran from **27 June 2023 to 3 January 2024**, carried out face-to-face
(CAPI/CAMI) by 88 trained interviewers. A three-stage probability sample was drawn from the
Geodirectory address database: 655 electoral-division clusters were selected across 17 urban/rural
strata, 6 addresses per cluster, and one individual per address via the last-birthday method.
Of 3,930 issued sample units, 52.8% responded, yielding roughly 2,075 completed interviews.

Report authors: Micheál L. Collins, Mathew J. Creighton, Ebru Işıklı, Ausra Cizauskaite, Sarah Carol
and Dorren McMahon — UCD Geary Institute for Public Policy.

Source data: [ESS Round 11 datafile](https://ess.sikt.no/en/datafile/242aaa39-3bbb-40f5-98bf-bfb1ce53d8ef)
"""
    )

st.caption("Built with Streamlit · Data: European Social Survey Round 11, Ireland")
