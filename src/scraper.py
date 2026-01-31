#!/usr/bin/env python

import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep

link = 'https://www.windguru.cz/48963' #id for caparica

class Scraper(object):
    def __init__(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1120,550")
        self.driver = webdriver.Chrome(options=options)

    def scrape(self):
        print('Loading...')
        self.driver.get(link)
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "tabulka"))
        )
        sleep(2)

        forecast = {}

    # windguru use tabulka class to get the table   
    # while True:
        s = BeautifulSoup(self.driver.page_source, "html.parser")
        text_file = open("forecast.txt", "w")
        text_file.write(str(s.find_all('script')))      
        text_file.close()
        table = s.find("table", {"class": "tabulka"}) #find the table with the class tabulka the first one, use find_all if there are multiple tables
        if not table:
            raise RuntimeError(
                "Table 'tabulka' was not found. The site structure may have changed."
            )
        tbody = table.find("tbody")
        if not tbody:
            raise RuntimeError("tbody element not found in the table.")
        rows = tbody.find_all("tr")
        # rows = s.find("table", {"class": "tabulka"}).find("tbody").find_all("tr", {"id": "tabid_0_0_WINDSPD"})

        for row in rows:
            cells = row.find_all("td")
            id = row['id']
            forecast[id] = []
            i = 0
            for cell in cells:
                if ('DIRPW' in id): # or ('DIRPW' in id):
                    print(id + " " + str(i))
                    value = cell.find('span').find('svg').find('g')["transform"]
                else:
                    value = cell.get_text()
                forecast[id].append(value)
                i = i + 1

        print(forecast)

        self.driver.quit()
        return forecast

if __name__ == '__main__':
    scraper = Scraper()
    scraper.scrape()
