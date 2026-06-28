import streamlit as st
from database.database import add_log
from services.browser_service import (
    open_website,
    take_screenshot,
    extract_page_text,
    extract_links
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
            "Extract Links"
        ]
    )

    url = st.text_input(
        "Website URL",
        placeholder="https://example.com"
    )

    if st.button("🚀 Run Browser Automation"):
        if not url:
            st.error("Please enter a URL.")
            return

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
                    st.text_area("Extracted Text", result["text"], height=300)

                    message = "Extracted page text."

                elif tool == "Extract Links":
                    links_df = extract_links(url)

                    st.success(f"✅ Extracted {len(links_df)} links.")
                    st.dataframe(links_df, width="stretch")

                    csv = links_df.to_csv(index=False).encode("utf-8")

                    st.download_button(
                        "Download Links CSV",
                        csv,
                        "extracted_links.csv",
                        "text/csv"
                    )

                    message = f"Extracted {len(links_df)} links."

                add_log(
                    file_name=url,
                    tool_name=f"Browser - {tool}",
                    original_rows=1,
                    new_rows=1,
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