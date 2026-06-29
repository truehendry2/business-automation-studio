from playwright.sync_api import sync_playwright
from pathlib import Path
from datetime import datetime
from io import StringIO
import pandas as pd


SCREENSHOT_DIR = Path("screenshots/browser")
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

DOWNLOAD_DIR = Path("downloads/browser")
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)


def open_website(url: str) -> dict:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=30000)
        title = page.title()
        browser.close()

    return {
        "url": url,
        "title": title,
        "status": "Success"
    }


def take_screenshot(url: str) -> dict:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = SCREENSHOT_DIR / f"screenshot_{timestamp}.png"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1366, "height": 768})
        page.goto(url, timeout=30000)
        page.screenshot(path=str(file_path), full_page=True)
        title = page.title()
        browser.close()

    return {
        "url": url,
        "title": title,
        "screenshot_path": str(file_path),
        "status": "Success"
    }


def extract_page_text(url: str) -> dict:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=30000)
        text = page.locator("body").inner_text()
        title = page.title()
        browser.close()

    return {
        "url": url,
        "title": title,
        "text": text[:5000],
        "status": "Success"
    }


def extract_links(url: str) -> pd.DataFrame:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=30000)

        links = page.locator("a").evaluate_all(
            """
            elements => elements.map(a => ({
                text: a.innerText,
                href: a.href
            }))
            """
        )

        browser.close()

    return pd.DataFrame(links)

def extract_tables(url: str) -> list[pd.DataFrame]:
    """
    Opens a website, extracts HTML tables, and returns them as DataFrames.
    """

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=30000)

        html = page.content()

        browser.close()

    tables = pd.read_html(StringIO(html))

    return tables

def login_with_selectors(
    url: str,
    username: str,
    password: str,
    username_selector: str,
    password_selector: str,
    submit_selector: str
) -> dict:
    """
    Logs into a website using user-provided CSS selectors.
    Takes a screenshot after login.
    """

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = SCREENSHOT_DIR / f"login_result_{timestamp}.png"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1366, "height": 768})

        page.goto(url, timeout=30000)

        page.fill(username_selector, username)
        page.fill(password_selector, password)
        page.click(submit_selector)

        page.wait_for_timeout(3000)

        title = page.title()
        current_url = page.url

        page.screenshot(path=str(screenshot_path), full_page=True)

        browser.close()

    return {
        "url": url,
        "current_url": current_url,
        "title": title,
        "screenshot_path": str(screenshot_path),
        "status": "Success"
    }

def fill_form_with_selectors(
    url: str,
    fields: dict,
    submit_selector: str | None = None
) -> dict:
    """
    Opens a website, fills form fields using CSS selectors, optionally submits the form,
    and captures a screenshot of the result.
    """

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = SCREENSHOT_DIR / f"form_result_{timestamp}.png"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1366, "height": 768})

        page.goto(url, timeout=30000)

        for selector, value in fields.items():
            page.fill(selector, value)

        if submit_selector:
            page.click(submit_selector)
            page.wait_for_timeout(3000)

        title = page.title()
        current_url = page.url

        page.screenshot(path=str(screenshot_path), full_page=True)

        browser.close()

    return {
        "url": url,
        "current_url": current_url,
        "title": title,
        "fields_filled": len(fields),
        "screenshot_path": str(screenshot_path),
        "status": "Success"
    }

def download_file_from_selector(
    url: str,
    download_selector: str
) -> dict:
    """
    Opens a website, clicks a download link/button using a CSS selector,
    saves the downloaded file, and returns the file path.
    """

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        page = browser.new_page(
            viewport={"width": 1366, "height": 768},
            accept_downloads=True
        )

        page.goto(url, timeout=30000)

        with page.expect_download() as download_info:
            page.click(download_selector)

        download = download_info.value

        suggested_name = download.suggested_filename
        saved_file_name = f"{timestamp}_{suggested_name}"
        saved_path = DOWNLOAD_DIR / saved_file_name

        download.save_as(str(saved_path))

        title = page.title()
        current_url = page.url

        browser.close()

    return {
        "url": url,
        "current_url": current_url,
        "title": title,
        "downloaded_file": str(saved_path),
        "file_name": saved_file_name,
        "status": "Success"
    }