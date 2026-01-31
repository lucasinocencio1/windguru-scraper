#!/usr/bin/env python

import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep

from mapping import format_forecast, print_forecast

LINK = "https://www.windguru.cz/48963"  # id for caparica


class Scraper:
    def __init__(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1120,550")
        self.driver = webdriver.Chrome(options=options)

    def scrape(self, url: str | None = None) -> list[dict]:
        url = url or LINK
        print("Loading...")
        self.driver.get(url)
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "tabulka"))
        )
        sleep(2)

        forecast = {}

        # Windguru uses tabulka class for the forecast table
        s = BeautifulSoup(self.driver.page_source, "html.parser")
        table = s.find("table", {"class": "tabulka"})
        if not table:
            raise RuntimeError(
                "Table 'tabulka' was not found. The site structure may have changed."
            )
        tbody = table.find("tbody")
        if not tbody:
            raise RuntimeError("tbody element not found in the table.")
        rows = tbody.find_all("tr")

        for row in rows:
            cells = row.find_all("td")
            row_id = row["id"]
            forecast[row_id] = []
            for cell in cells:
                if "DIRPW" in row_id or "WAVEDIR" in row_id:
                    try:
                        span = cell.find("span")
                        svg = span.find("svg") if span else None
                        g = svg.find("g") if svg else None
                        value = (
                            g["transform"]
                            if g and g.get("transform")
                            else (cell.get_text(strip=True) or "-")
                        )
                    except (AttributeError, TypeError):
                        value = cell.get_text(strip=True) or "-"
                else:
                    value = cell.get_text(strip=True) or "-"
                forecast[row_id].append(str(value))

        self.driver.quit()

        formatted = format_forecast(forecast)
        print_forecast(formatted)
        return formatted


if __name__ == "__main__":
    scraper = Scraper()
    data = scraper.scrape()

    # Save to JSON for later use
    with open("forecast.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("\n→ Saved to forecast.json")
