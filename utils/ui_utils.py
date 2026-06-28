import streamlit as st


def app_header(title, subtitle):
    st.markdown(
        f"""
        <div style="
            padding: 24px;
            border-radius: 16px;
            background: linear-gradient(135deg, #1E293B, #0F172A);
            margin-bottom: 24px;
        ">
            <h1 style="margin:0; color:#F8FAFC;">{title}</h1>
            <p style="margin:8px 0 0 0; color:#CBD5E1; font-size:16px;">
                {subtitle}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


def metric_card(title, value, subtitle=""):
    st.markdown(
        f"""
        <div style="
            padding: 20px;
            border-radius: 14px;
            background-color: #1E293B;
            border: 1px solid #334155;
            min-height: 120px;
        ">
            <p style="color:#CBD5E1; margin:0;">{title}</p>
            <h2 style="color:#F8FAFC; margin:10px 0;">{value}</h2>
            <p style="color:#94A3B8; margin:0;">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def section_title(title, subtitle=""):
    st.markdown(f"### {title}")
    if subtitle:
        st.caption(subtitle)