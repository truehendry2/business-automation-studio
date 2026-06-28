import streamlit as st
from database.database import add_log
from services.browser_service import (
    open_website,
    take_screenshot,
    extract_page_text,
    extract_links,
    extract_tables,
    login_with_selectors,
    fill_form_with_selectors
)


def show():
    st.title("🌐 Browser Automation Toolkit")
    st.write("Automate browser tasks using Playwright.")

    st.divider()

    tool = st.selectbox(
        "Choose Browser Automation",
        [
            "Open Website",
            "Extract Page Title",
            "Take Screenshot",
            "Extract Page Text",
            "Extract Links",
            "Extract Tables",
            "Login Automation",
            "Form Automation"
        ]
    )

    url = st.text_input(
        "Website URL",
        placeholder="https://example.com"
    )
    
    username = ""
    password = ""
    username_selector = ""
    password_selector = ""
    submit_selector = ""
    
    if tool == "Login Automation":
        st.subheader("Login Details")
    
        username = st.text_input("Username / Email")
        password = st.text_input("Password", type="password")
    
        st.subheader("CSS Selectors")
    
        username_selector = st.text_input(
            "Username Field Selector",
            placeholder='Example: input[name="username"]'
        )
    
        password_selector = st.text_input(
            "Password Field Selector",
            placeholder='Example: input[name="password"]'
        )
    
        submit_selector = st.text_input(
            "Submit Button Selector",
            placeholder='Example: button[type="submit"]'
        )
    
    form_fields_text = ""
    form_submit_selector = ""
    
    if tool == "Form Automation":
        st.subheader("Form Fields")
    
        st.write(
            "Enter one field per line using this format:"
        )
    
        st.code('input[name="firstName"] | Hendry\ninput[name="email"] | test@example.com')
    
        form_fields_text = st.text_area(
            "Field selectors and values",
            height=180,
            placeholder='input[name="firstName"] | Hendry\ninput[name="email"] | test@example.com'
        )
    
        form_submit_selector = st.text_input(
            "Submit Button Selector (optional)",
            placeholder='Example: button[type="submit"]'
        )

    if st.button("🚀 Run Browser Automation"):
        if not url:
            st.error("Please enter a URL.")
            return

        message = ""
        total_rows = 1

        try:
            with st.spinner("Running browser automation..."):

                if tool in ["Open Website", "Extract Page Title"]:
                    result = open_website(url)

                    st.success("✅ Website opened successfully.")
                    st.write("**Title:**", result["title"])
                    st.write("**URL:**", result["url"])

                    message = f"Extracted page title: {result['title']}"

                elif tool == "Take Screenshot":
                    result = take_screenshot(url)

                    st.success("✅ Screenshot captured.")
                    st.write("**Title:**", result["title"])
                    st.image(result["screenshot_path"], width="stretch")

                    with open(result["screenshot_path"], "rb") as file:
                        st.download_button(
                            "Download Screenshot",
                            data=file,
                            file_name="browser_screenshot.png",
                            mime="image/png"
                        )

                    message = f"Screenshot saved: {result['screenshot_path']}"

                elif tool == "Extract Page Text":
                    result = extract_page_text(url)

                    st.success("✅ Page text extracted.")
                    st.write("**Title:**", result["title"])
                    st.text_area(
                        "Extracted Text",
                        result["text"],
                        height=300
                    )

                    message = "Extracted page text."

                elif tool == "Extract Links":
                    links_df = extract_links(url)

                    total_rows = len(links_df)

                    st.success(f"✅ Extracted {total_rows} links.")
                    st.dataframe(links_df, width="stretch")

                    csv = links_df.to_csv(index=False).encode("utf-8")

                    st.download_button(
                        "Download Links CSV",
                        data=csv,
                        file_name="extracted_links.csv",
                        mime="text/csv"
                    )

                    message = f"Extracted {total_rows} links."

                elif tool == "Extract Tables":
                    tables = extract_tables(url)

                    if len(tables) == 0:
                        st.warning("No tables found on this page.")
                        total_rows = 0
                        message = "No tables found."

                    else:
                        total_rows = 0

                        st.success(f"✅ Extracted {len(tables)} table(s).")

                        for index, table in enumerate(tables):
                            st.subheader(f"Table {index + 1}")

                            st.dataframe(table, width="stretch")

                            table_rows = len(table)
                            total_rows += table_rows

                            csv = table.to_csv(index=False).encode("utf-8")

                            st.download_button(
                                f"Download Table {index + 1} CSV",
                                data=csv,
                                file_name=f"table_{index + 1}.csv",
                                mime="text/csv"
                            )

                        message = (
                            f"Extracted {len(tables)} table(s) "
                            f"with {total_rows} total rows."
                        )

                elif tool == "Login Automation":
                    if not username or not password:
                        st.error("Please enter username and password.")
                        return
                
                    if not username_selector or not password_selector or not submit_selector:
                        st.error("Please enter all CSS selectors.")
                        return
                
                    result = login_with_selectors(
                        url=url,
                        username=username,
                        password=password,
                        username_selector=username_selector,
                        password_selector=password_selector,
                        submit_selector=submit_selector
                    )
                
                    st.success("✅ Login automation completed.")
                    st.write("**Page Title:**", result["title"])
                    st.write("**Current URL:**", result["current_url"])
                
                    st.image(result["screenshot_path"], width="stretch")
                
                    with open(result["screenshot_path"], "rb") as file:
                        st.download_button(
                            "Download Login Screenshot",
                            data=file,
                            file_name="login_result.png",
                            mime="image/png"
                        )
                
                    message = "Completed login automation and captured screenshot."
                    total_rows = 1
                    
                elif tool == "Form Automation":
                    if not form_fields_text.strip():
                        st.error("Please enter at least one form field.")
                        return

                    fields = {}

                    for line in form_fields_text.splitlines():
                        if "|" not in line:
                            st.error(
                                "Invalid format. Use: CSS selector | value"
                            )
                            return

                        selector, value = line.split("|", 1)
                        selector = selector.strip()
                        value = value.strip()

                        if selector and value:
                            fields[selector] = value

                    if len(fields) == 0:
                        st.error("No valid form fields found.")
                        return

                    result = fill_form_with_selectors(
                        url=url,
                        fields=fields,
                        submit_selector=form_submit_selector if form_submit_selector else None
                    )

                    st.success("✅ Form automation completed.")
                    st.write("**Page Title:**", result["title"])
                    st.write("**Current URL:**", result["current_url"])
                    st.write("**Fields Filled:**", result["fields_filled"])

                    st.image(result["screenshot_path"], width="stretch")

                    with open(result["screenshot_path"], "rb") as file:
                        st.download_button(
                            "Download Form Screenshot",
                            data=file,
                            file_name="form_result.png",
                            mime="image/png"
                        )

                    message = f"Filled {result['fields_filled']} form field(s)."
                    total_rows = result["fields_filled"]

                add_log(
                    file_name=url,
                    tool_name=f"Browser - {tool}",
                    original_rows=1,
                    new_rows=total_rows,
                    status="Success",
                    message=message
                )

        except Exception as e:
            st.error(f"Automation failed: {e}")

            add_log(
                file_name=url,
                tool_name=f"Browser - {tool}",
                original_rows=1,
                new_rows=0,
                status="Failed",
                message=str(e)
            )