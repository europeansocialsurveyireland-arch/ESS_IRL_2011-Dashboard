import streamlit as st


def insight(text: str, *, source: str = "Irish Social Attitudes: 2023 report") -> None:
    """A consistent 'what this means' callout under a chart."""
    st.info(f"**Insight.** {text}\n\n*Source: {source}*")


def data_insight(text: str, *, data: str) -> None:
    """Insight derived from the data directly (topic not covered in the source report).

    `data` names the rounds the chart actually draws on, e.g. "ESS Round 10 (2021/22)".
    It is required on purpose: these topics come from different rounds, so there is no
    safe default.
    """
    st.info(f"**Insight.** {text}\n\n*Derived from {data} Ireland data (not covered in the published report).*")


def page_header(title: str, subtitle: str = "") -> None:
    st.title(title)
    if subtitle:
        st.caption(subtitle)
    st.divider()
