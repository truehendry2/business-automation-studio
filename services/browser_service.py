from playwright.sync_api import sync_playwright
from pathlib import Path
from datetime import datetime
import pandas as pd


SCREENSHOT_DIR = Path("screenshots/browser")
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)


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