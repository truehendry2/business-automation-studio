import streamlit as st
import pandas as pd
from database.database import add_log
from io import BytesIO


def convert_df_to_excel(df):
    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Cleaned Data")

    return output.getvalue()


def convert_df_to_csv(df):
    return df.to_csv(index=False).encode("utf-8")


def show():
    st.title("📊 Excel Automation Toolkit")
    st.write("Upload Excel or CSV files, choose an automation, preview the result, and download the cleaned file.")

    st.divider()

    uploaded_file = st.file_uploader(
        "Upload an Excel or CSV file",
        type=["xlsx", "csv"]
    )

    if uploaded_file is None:
        st.info("Upload a file to start.")
        return

    # Read file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    original_rows = len(df)
    original_columns = len(df.columns)

    # File preview cards
    st.subheader("📁 File Preview")

    col1, col2, col3 = st.columns(3)

    col1.metric("File Name", uploaded_file.name)
    col2.metric("Rows", original_rows)
    col3.metric("Columns", original_columns)

    with st.expander("View Original Data"):
        st.dataframe(df, use_container_width=True)

    st.divider()

    # Tool selector
    st.subheader("⚙️ Choose Automation")

    tool = st.selectbox(
        "Select a tool",
        [
            "Remove duplicate rows",
            "Remove blank rows",
            "Remove blank columns",
            "Trim extra spaces",
            "Sort by column",
            "Rename columns",
            "CSV to Excel",
            "Excel to CSV"
        ]
    )

    result_df = df.copy()
    message = ""

    # Extra inputs for specific tools
    sort_column = None
    rename_old = None
    rename_new = None

    if tool == "Sort by column":
        sort_column = st.selectbox("Choose column to sort by", df.columns)

    if tool == "Rename columns":
        rename_old = st.selectbox("Choose column to rename", df.columns)
        rename_new = st.text_input("New column name")

    st.divider()

    # Run button
    if st.button("🚀 Run Automation"):
        try:
            if tool == "Remove duplicate rows":
                before = len(result_df)
                result_df = result_df.drop_duplicates()
                after = len(result_df)
                message = f"Removed {before - after} duplicate rows."

            elif tool == "Remove blank rows":
                before = len(result_df)
                result_df = result_df.dropna(how="all")
                after = len(result_df)
                message = f"Removed {before - after} blank rows."

            elif tool == "Remove blank columns":
                before = len(result_df.columns)
                result_df = result_df.dropna(axis=1, how="all")
                after = len(result_df.columns)
                message = f"Removed {before - after} blank columns."

            elif tool == "Trim extra spaces":
                text_columns = result_df.select_dtypes(include=["object"]).columns

                for column in text_columns:
                    result_df[column] = result_df[column].astype(str).str.strip()

                message = f"Trimmed extra spaces in {len(text_columns)} text columns."

            elif tool == "Sort by column":
                result_df = result_df.sort_values(by=sort_column)
                message = f"Sorted data by '{sort_column}'."

            elif tool == "Rename columns":
                if rename_new.strip() == "":
                    st.error("Please enter a new column name.")
                    return

                result_df = result_df.rename(columns={rename_old: rename_new})
                message = f"Renamed column '{rename_old}' to '{rename_new}'."

            elif tool == "CSV to Excel":
                message = "Converted CSV data to Excel format."

            elif tool == "Excel to CSV":
                message = "Converted Excel data to CSV format."

            add_log(
                file_name=uploaded_file.name,
                tool_name=tool,
                original_rows=original_rows,
                new_rows=len(result_df),
                status="Success",
                message=message
            )

            st.success(f"✅ Automation Complete: {message}")

            st.subheader("📊 Result Preview")

            col1, col2, col3 = st.columns(3)

            col1.metric("Original Rows", original_rows)
            col2.metric("New Rows", len(result_df))
            col3.metric("Columns", len(result_df.columns))

            st.dataframe(result_df, use_container_width=True)

            st.divider()

            st.subheader("⬇️ Download Result")

            excel_data = convert_df_to_excel(result_df)
            csv_data = convert_df_to_csv(result_df)

            if tool == "Excel to CSV":
                st.download_button(
                    "Download CSV",
                    data=csv_data,
                    file_name="processed_file.csv",
                    mime="text/csv"
                )

            elif tool == "CSV to Excel":
                st.download_button(
                    "Download Excel",
                    data=excel_data,
                    file_name="processed_file.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

            else:
                col_a, col_b = st.columns(2)

                with col_a:
                    st.download_button(
                        "Download Excel",
                        data=excel_data,
                        file_name="processed_file.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

                with col_b:
                    st.download_button(
                        "Download CSV",
                        data=csv_data,
                        file_name="processed_file.csv",
                        mime="text/csv"
                    )

        except Exception as e:
            st.error(f"Something went wrong: {e}")