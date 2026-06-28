import streamlit as st
import pandas as pd
from io import BytesIO
from database.database import get_logs


def convert_df_to_csv(df):
    return df.to_csv(index=False).encode("utf-8")


def convert_df_to_excel(df):
    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Automation Report")

    return output.getvalue()


def show():
    st.title("📈 Reports")
    st.write("Generate reports from automation activity logs.")

    st.divider()

    logs = get_logs()

    if len(logs) == 0:
        st.info("No logs available yet. Run an automation first.")
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

    st.subheader("📊 Report Summary")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Logs", len(df))
    col2.metric("Successful", len(df[df["Status"] == "Success"]))
    col3.metric("Failed", len(df[df["Status"] == "Failed"]))

    st.divider()

    st.subheader("🔍 Filter Report")

    selected_tool = st.selectbox(
        "Filter by tool",
        ["All"] + sorted(df["Tool"].unique().tolist())
    )

    if selected_tool != "All":
        filtered_df = df[df["Tool"] == selected_tool]
    else:
        filtered_df = df

    st.dataframe(filtered_df, use_container_width=True)

    st.divider()

    st.subheader("⬇️ Export Report")

    csv_data = convert_df_to_csv(filtered_df)
    excel_data = convert_df_to_excel(filtered_df)

    col_a, col_b = st.columns(2)

    with col_a:
        st.download_button(
            "Download CSV Report",
            data=csv_data,
            file_name="automation_report.csv",
            mime="text/csv"
        )

    with col_b:
        st.download_button(
            "Download Excel Report",
            data=excel_data,
            file_name="automation_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )