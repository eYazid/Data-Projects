import requests
import pandas as pd
from bs4 import BeautifulSoup

url = r"https://web.archive.org/web/20230908091635 /https://en.wikipedia.org/wiki/List_of_largest_banks"
exchange_rate = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-PY0221EN-Coursera/labs/v2/exchange_rate.csv"
table_attr = ["Name", "MC_USD_Billion"]
target_attr = ["Name", "MC_USD_Billion", "MC_GBP_Billion", "MC_EUR_Billion",
               "MC_INR_Billion"]
output_csv = r"/Largest_banks_data.csv"
db = "Banks.db"
table_name = "Largest_banks"


def extract():
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    list_tables = soup.find_all("tbody")
    rows = list_tables[1].find_all("tr")
    for row in rows:
        if row.find_all("a"):
            elems = row.text.strip().split("\n")
            data = {"rank": elems[0],
                    "name": elems[2],
                    "market_cap": elems[-1]}
    return

def transform():
    return

def load_to_csv():
    return

def load_to_db():
    return

def log():
    pass




