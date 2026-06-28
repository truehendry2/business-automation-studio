import streamlit as st
import pandas as pd
from database.database import get_logs
from utils.ui_utils import app_header, metric_card, section_title


def show():
    app_header(
        "Business Automation Studio",
        "A modular platform for Excel, email, browser, reporting, and AI workflow automation."
    )

    logs = get_logs()

    if len(logs) == 0:
        st.info("No automation logs yet. Run an Excel automation first.")
        return

    df = pd.DataFrame(
        logs,
        columns=[
            "Timestamp",
            "File Name",
            "Tool",
            "Original Rows",
            "New Rows",
            "Status",
            "Message"
        ]
    )

    total_tasks = len(df)
    completed = len(df[df["Status"] == "Success"])
    failed = len(df[df["Status"] == "Failed"])
    success_rate = round((completed / total_tasks) * 100, 1)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card("Total Tasks", total_tasks, "All recorded automations")

    with col2:
        metric_card("Completed", completed, "Successful runs")

    with col3:
        metric_card("Failed", failed, "Failed runs")

    with col4:
        metric_card("Success Rate", f"{success_rate}%", "Automation reliability")

    st.divider()

    section_title("🕒 Recent Activity", "Latest automation runs from SQLite logs")
    st.dataframe(df.head(10), width="stretch")

    st.divider()

    section_title("📊 Automation Usage", "Most used tools and modules")
    usage = df["Tool"].value_counts()
    st.bar_chart(usage)

    st.divider()

    section_title("📁 Recent Files", "Recently processed files")
    recent_files = df[["Timestamp", "File Name", "Tool", "Message"]].head(5)
    st.dataframe(recent_files, width="stretch")