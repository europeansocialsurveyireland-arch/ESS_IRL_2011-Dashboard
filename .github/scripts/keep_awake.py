"""Keep the live dashboard awake on Streamlit Community Cloud.

Community Cloud puts an app to sleep when nobody has visited it for a while,
and a plain HTTP request does not count as a visit: only a real browser
session does. This script opens the dashboard in a headless browser, clicks
Streamlit's "wake up" button if the app is asleep, waits until the home page
has actually loaded, and stays connected briefly so the visit registers.

It exits with an error if the dashboard does not load, so the GitHub Actions
run fails and GitHub notifies the repository owner. That makes it double as
a simple uptime check.

Run locally:  APP_URL=https://... python .github/scripts/keep_awake.py
"""

import os
import re
import sys
import time

from playwright.sync_api import sync_playwright

APP_URL = os.environ.get("APP_URL", "https://essirl2011-dashboard.streamlit.app/")

# Text of the home page's main heading (st.title in app/Home.py). If that title
# ever changes, update this so the check still knows what "loaded" looks like.
HOME_HEADING = "Irish Social Attitudes"

# Streamlit's sleep screen shows a button like "Yes, get this app back up!".
WAKE_BUTTON = re.compile(r"get this app back up", re.IGNORECASE)

LOAD_TIMEOUT_S = 300  # waking a sleeping app can take a few minutes
STAY_CONNECTED_S = 20


def all_frames(page):
    # Community Cloud serves the app inside an inner frame, while its sleep
    # screen is part of the outer page. Search both so either layout works.
    return [page.main_frame, *page.main_frame.child_frames]


def main() -> int:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        print(f"Opening {APP_URL}")
        page.goto(APP_URL, wait_until="domcontentloaded", timeout=120_000)

        deadline = time.monotonic() + LOAD_TIMEOUT_S
        clicked_wake = False
        while time.monotonic() < deadline:
            frames = all_frames(page)
            if not clicked_wake:
                for frame in frames:
                    wake = frame.get_by_role("button", name=WAKE_BUTTON)
                    if wake.count():
                        print("The app was asleep. Clicking the wake-up button.")
                        wake.first.click()
                        clicked_wake = True
                        break
            if any(f.get_by_role("heading", name=HOME_HEADING).count() for f in frames):
                break
            time.sleep(5)
        else:
            print(f"FAILED: the home page did not load within {LOAD_TIMEOUT_S} seconds.")
            page.screenshot(path="keep_awake_failure.png", full_page=True)
            browser.close()
            return 1

        errors = sum(f.locator('[data-testid="stException"]').count() for f in all_frames(page))
        if errors:
            print(f"FAILED: the home page loaded but shows {errors} error message(s).")
            browser.close()
            return 1

        print("Dashboard loaded" + (" after waking it up." if clicked_wake else " (it was already awake)."))
        page.wait_for_timeout(STAY_CONNECTED_S * 1000)
        browser.close()
        return 0


if __name__ == "__main__":
    sys.exit(main())
