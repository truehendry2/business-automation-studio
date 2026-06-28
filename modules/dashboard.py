import streamlit as st
import pandas as pd

def show():
    st.title("⚙️ Business Automation Studio")
    st.write("Version 1.0 — Automate repetitive business workflows from one dashboard.")

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Today's Tasks", "12", "+3")
    col2.metric("Completed", "11", "+2")
    col3.metric("Failed", "1", "-1")
    col4.metric("Automations", "4", "+1")

    st.divider()

    st.subheader("📌 System Status")

    status_col1, status_col2, status_col3 = st.columns(3)

    status_col1.success("Excel Module: Active")
    status_col2.warning("Email Module: Coming Soon")
    status_col3.warning("AI Module: Coming Soon")

    st.divider()

    st.subheader("🕒 Recent Activity")

    data = {
        "Time": ["09:00", "10:15", "11:30", "12:05"],
        "Tool": ["Excel Cleaner", "Dashboard", "Report Export", "Excel Cleaner"],
        "Action": ["Removed duplicates", "Opened app", "Generated report", "Cleaned file"],
        "Status": ["Success", "Success", "Success", "Success"]
    }

    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)

    st.divider()

    st.subheader("📊 Automation Overview")

    chart_data = pd.DataFrame({
        "Module": ["Excel", "Email", "Browser", "AI"],
        "Tasks": [8, 2, 1, 1]
    })

    st.bar_chart(chart_data.set_index("Module"))