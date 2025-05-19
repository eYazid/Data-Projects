import requests
import pandas as pd
import sqlite3
import logging
import numpy as np
from datetime import datetime
from bs4 import BeautifulSoup


url = r'https://web.archive.org/web/20230902185326/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29'
table_attribs = ["Country", "GDP_USD_millions"]
db_name = 'World_Economies.db'
table_name = 'Countries_by_GDP'
csv_path = './Countries_by_GDP.csv'
first_approach = False  # In The first Approach is depending on read_html method in pandas which will be deprecated


def extract(url, table_attribs):
    html_content = requests.get(url).text
    if first_approach:
        tables = pd.read_html(html_content)
        target_df = tables[2][["Country/Territory", "UN region", "IMF[1][13]"]]
        target_df.columns = target_df.columns.droplevel(1)
        target_df.columns = ["Country/Territory", "UN region", "GDP_USD_millions", "Year"]
    else:
         target_df = pd.DataFrame(columns=["Country", "UN region", "GDP_USD_millions", "Year"])
         soup = BeautifulSoup(html_content, "html.parser")
         tables = soup.find_all("table")
         rows = tables[2].find_all("tr")
         for row in rows:
             col = row.find_all("td")
             if col and col[0].find("a"):
                target_df = pd.concat([target_df, pd.DataFrame([{"Country": col[0].a.contents[0], "UN region": col[1].a.contents[0], "GDP_USD_millions": col[2].contents[0], "Year": col[2].contents[0]}])], ignore_index=True)
    return target_df

def transform(df):
    df["GDP_USD_millions"].apply(lambda x: np.round(float("".join(x.replace('—', "0").split(",")))/1_000,2))
    df.rename(columns={"GDP_USD_millions": "GDP_USD_billions"}, inplace=True)
    return df

def load_to_csv(df, csv_path):
    df.to_csv(csv_path, index=False)

def load_to_db(df, sql_connection, table_name):
    df.to_sql(table_name, sql_connection, if_exists='append', index=False)

def run_query(query_statement, sql_connection):
    pd.read_sql(query_statement, sql_connection)

def log_progress(message):
    timestamp_format = '%Y-%h-%d-%H:%M:%S'
    now = datetime.now()
    timestamp = now.strftime(timestamp_format) 
    with open("./etl_project_log.log","a") as f: 
        f.write(timestamp + ' : ' + message + '\n')


if __name__ == "__main__":
        log_progress('Preliminaries complete. Initiating ETL process')

        df = extract(url, table_attribs)

        log_progress('Data extraction complete. Initiating Transformation process')

        df = transform(df)

        log_progress('Data transformation complete. Initiating loading process')

        load_to_csv(df, csv_path)

        log_progress('Data saved to CSV file')

        sql_connection = sqlite3.connect('World_Economies.db')

        log_progress('SQL Connection initiated.')

        load_to_db(df, sql_connection, table_name)

        log_progress('Data loaded to Database as table. Running the query')

        query_statement = f"SELECT * from {table_name} WHERE GDP_USD_billions >= 100"
        run_query(query_statement, sql_connection)

        log_progress('Process Complete.')

        sql_connection.close()

