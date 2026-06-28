import streamlit as st
import sqlite3
import os
import platform

from config import *

def show():

    st.title("⚙ Settings")

    st.write("Manage application settings and system information.")

    st.divider()

    ##########################

    st.subheader("Appearance")

    theme = st.selectbox(
        "Theme",
        [
            "Dark",
            "Light"
        ],
        index=0
    )

    export = st.selectbox(
        "Default Export Format",
        [
            "Excel",
            "CSV"
        ]
    )

    auto_logs = st.toggle(
        "Auto Save Logs",
        value=AUTO_SAVE_LOGS
    )

    notifications = st.toggle(
        "Notifications",
        value=NOTIFICATIONS
    )

    st.divider()

    ##########################

    st.subheader("Database")

    if os.path.exists(DATABASE_PATH):

        size = os.path.getsize(DATABASE_PATH)/1024

        st.metric(
            "Database Size",
            f"{size:.2f} KB"
        )

    else:

        st.error("Database not found.")

    st.code(DATABASE_PATH)

    ##########################

    st.divider()

    st.subheader("Maintenance")

    col1,col2=st.columns(2)

    with col1:

        if st.button("Backup Database"):

            st.info("Feature coming soon.")

    with col2:

        if st.button("Clear Logs"):

            conn=sqlite3.connect(DATABASE_PATH)

            cursor=conn.cursor()

            cursor.execute("DELETE FROM automation_logs")

            conn.commit()

            conn.close()

            st.success("Logs cleared successfully.")

    ##########################

    st.divider()

    st.subheader("System Information")

    col1,col2=st.columns(2)

    with col1:

        st.metric("Version",VERSION)

        st.metric("Author",AUTHOR)

    with col2:

        st.metric("Python",platform.python_version())

        st.metric("Platform",platform.system())