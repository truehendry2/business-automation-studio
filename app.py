import streamlit as st
from database.database import create_database
from modules.dashboard import dashboard
from modules.excel import excel_tools
from modules.email import email_tools
from modules.browser import browser_tools
from modules.ai import ai_tools
from modules.reports import reports
from modules.settings import settings


st.set_page_config(
    page_title="Business Automation Studio",
    page_icon="⚙️",
    layout="wide"
)

create_database()

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
    reports.show()

elif page == "⚙ Settings":
    settings.show()