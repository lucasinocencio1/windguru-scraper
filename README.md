## windguru-scraper


A Python script for scraping surf forecasts from Windguru￼to bring your favorite spot informations.

The script uses the spot ID to fetch forecast data, for example (https://www.windguru.cz/[id]):

https://www.windguru.cz/48963 -> caparica spot

It retrieves the first forecast table found on the page. If you want multiple tables, you can adapt the code to use find_all instead.

How to run:

```
python src/scraper.py
```