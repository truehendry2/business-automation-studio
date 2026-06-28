import streamlit as st
import requests
from bs4 import BeautifulSoup
from database.database import add_log


def show():
    st.title("🌐 Browser Automation")
    st.write("Version 1.0 — Extract website titles, links, and page information.")

    st.divider()

    url = st.text_input("Enter website URL", "https://example.com")

    action = st.selectbox(
        "Choose browser automation",
        [
            "Get Page Title",
            "Extract Links",
            "Count Images",
            "Download Page HTML"
        ]
    )

    if st.button("🚀 Run Browser Automation"):
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            if action == "Get Page Title":
                title = soup.title.string if soup.title else "No title found"
                st.success("✅ Page title extracted.")
                st.write(title)
                message = f"Extracted title from {url}"

            elif action == "Extract Links":
                links = []

                for link in soup.find_all("a"):
                    href = link.get("href")
                    text = link.get_text(strip=True)

                    if href:
                        links.append({
                            "Text": text,
                            "URL": href
                        })

                st.success(f"✅ Extracted {len(links)} links.")
                st.dataframe(links, use_container_width=True)
                message = f"Extracted {len(links)} links from {url}"

            elif action == "Count Images":
                images = soup.find_all("img")
                st.success(f"✅ Found {len(images)} images.")
                st.write(f"Total images: {len(images)}")
                message = f"Counted {len(images)} images from {url}"

            elif action == "Download Page HTML":
                st.success("✅ HTML downloaded successfully.")
                st.download_button(
                    "Download HTML",
                    response.text,
                    "page.html",
                    "text/html"
                )
                message = f"Downloaded HTML from {url}"

            add_log(
                file_name=url,
                tool_name=f"Browser - {action}",
                original_rows=1,
                new_rows=1,
                status="Success",
                message=message
            )

        except Exception as e:
            st.error(f"Something went wrong: {e}")

            add_log(
                file_name=url,
                tool_name=f"Browser - {action}",
                original_rows=0,
                new_rows=0,
                status="Failed",
                message=str(e)
            )