import streamlit as st
import pandas as pd
from database.database import get_logs


def show():
    st.title("⚙️ Business Automation Studio")
    st.write("Version 1.1 — Real automation tracking with SQLite logs.")

    st.divider()

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

    col1.metric("Total Tasks", total_tasks)
    col2.metric("Completed", completed)
    col3.metric("Failed", failed)
    col4.metric("Success Rate", f"{success_rate}%")

    st.divider()

    st.subheader("🕒 Recent Activity")
    st.dataframe(df.head(10), use_container_width=True)

    st.divider()

    st.subheader("📊 Automation Usage")

    usage = df["Tool"].value_counts()
    st.bar_chart(usage)

    st.divider()

    st.subheader("📁 Recent Files")

    recent_files = df[["Timestamp", "File Name", "Tool", "Message"]].head(5)
    st.dataframe(recent_files, use_container_width=True)