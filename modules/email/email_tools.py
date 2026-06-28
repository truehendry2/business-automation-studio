import streamlit as st
import pandas as pd
from database.database import add_log


def show():
    st.title("📧 Email Automation")
    st.write("Version 1.0 — Sample inbox workflow for email categorization and task extraction.")

    st.divider()

    df = pd.read_csv("data/sample_emails.csv")

    unread_count = len(df[df["status"] == "Unread"])
    invoice_count = len(df[df["category"] == "Invoice"])
    support_count = len(df[df["category"] == "Support"])
    task_count = len(df[df["category"] == "Task"])

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Unread Emails", unread_count)
    col2.metric("Invoices", invoice_count)
    col3.metric("Support", support_count)
    col4.metric("Tasks", task_count)

    st.divider()

    st.subheader("📥 Inbox Preview")
    st.dataframe(df, width="stretch")

    st.divider()

    st.subheader("⚙️ Email Automation Actions")

    action = st.selectbox(
        "Choose action",
        [
            "Summarize Inbox",
            "Extract Tasks",
            "Show Invoices",
            "Show Support Emails",
            "Export Summary"
        ]
    )

    if st.button("🚀 Run Email Automation"):
        if action == "Summarize Inbox":
            result = df.groupby("category").size().reset_index(name="count")
            st.success("✅ Inbox summarized successfully.")
            st.dataframe(result, width="stretch")

        elif action == "Extract Tasks":
            result = df[df["category"] == "Task"]
            st.success(f"✅ Extracted {len(result)} task emails.")
            st.dataframe(result, width="stretch")

        elif action == "Show Invoices":
            result = df[df["category"] == "Invoice"]
            st.success(f"✅ Found {len(result)} invoice emails.")
            st.dataframe(result, width="stretch")

        elif action == "Show Support Emails":
            result = df[df["category"] == "Support"]
            st.success(f"✅ Found {len(result)} support emails.")
            st.dataframe(result, width="stretch")

        elif action == "Export Summary":
            result = df.groupby("category").size().reset_index(name="count")
            st.success("✅ Summary ready for export.")
            st.dataframe(result, width="stretch")

            csv = result.to_csv(index=False).encode("utf-8")

            st.download_button(
                "Download Email Summary CSV",
                csv,
                "email_summary.csv",
                "text/csv"
            )

        add_log(
            file_name="sample_emails.csv",
            tool_name=f"Email - {action}",
            original_rows=len(df),
            new_rows=len(df),
            status="Success",
            message=f"Ran email automation: {action}"
        )