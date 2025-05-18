import requests
import pandas as pd
import sqlite3
import numpy as np
from datetime import datetime
from bs4 import BeautifulSoup


url = r'https://web.archive.org/web/20230902185326/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29'
table_attribs = ["Country", "GDP_USD_millions"]
db_name = 'World_Economies.db'
table_name = 'Countries_by_GDP'
csv_path = './Countries_by_GDP.csv'
first_approach = False  # In The first Approach Data isn't properly cleaned


def extract(url, table_attribs):
    html_content = requests.get(url).text
    if first_approach:
        tables = pd.read_html(html_content)
        target_df = tables[2][["Country/Territory", "UN region", "IMF[1][13]"]]
        target_df.columns = target_df.columns.droplevel(1)
        target_df.columns = ["Country/Territory", "UN region", "GDP_USD_millions", "Year"]
    else:
         df = pd.DataFrame(columns=["Country", "UN region", "GDP_USD_millions", "Year"])
         soup = BeautifulSoup(html_content, "html.parser")
         tables = soup.find_all("table")
         rows = tables[2].find_all("tr")
         for row in rows:
             col = row.find_all("td")
             if col and col[0].find("a"):
                df = pd.concat([df, pd.DataFrame([{"Country": col[0].a.contents[0], "UN region": col[1].a.contents[0], "GDP_USD_millions": col[2].contents[0], "Year": col[2].contents[0]}])], ignore_index=True)
    return target_df

def transform(df):
    ''' This function converts the GDP information from Currency
    format to float value, transforms the information of GDP from
    USD (Millions) to USD (Billions) rounding to 2 decimal places.
    The function returns the transformed dataframe.'''

    return df

def load_to_csv(df, csv_path):
    ''' This function saves the final dataframe as a `CSV` file 
    in the provided path. Function returns nothing.'''

def load_to_db(df, sql_connection, table_name):
    ''' This function saves the final dataframe as a database table
    with the provided name. Function returns nothing.'''

def run_query(query_statement, sql_connection):
    ''' This function runs the stated query on the database table and
    prints the output on the terminal. Function returns nothing. '''

def log_progress(message):
    ''' This function logs the mentioned message at a given stage of the code execution to a log file. Function returns nothing'''

''' Here, you define the required entities and call the relevant 
functions in the correct order to complete the project. Note that this
portion is not inside any function.'''

if __name__ == "__main__":
        extract(url,0)

