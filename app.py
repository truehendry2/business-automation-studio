import streamlit as st
from modules import dashboard, excel_tools, email_tools, browser_tools, ai_tools

st.set_page_config(
    page_title="Business Automation Studio",
    page_icon="⚙️",
    layout="wide"
)

st.sidebar.title("⚙️ Automation Studio")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "📊 Excel Automation",
        "📧 Email Automation",
        "🌐 Browser Automation",
        "🤖 AI Assistant",
        "📈 Reports",
        "⚙ Settings"
    ]
)

if page == "🏠 Dashboard":
    dashboard.show()

elif page == "📊 Excel Automation":
    excel_tools.show()

elif page == "📧 Email Automation":
    email_tools.show()

elif page == "🌐 Browser Automation":
    browser_tools.show()

elif page == "🤖 AI Assistant":
    ai_tools.show()

elif page == "📈 Reports":
    st.title("Reports")
    st.info("Reports page coming soon.")

elif page == "⚙ Settings":
    st.title("Settings")
    st.info("Settings page coming soon.")