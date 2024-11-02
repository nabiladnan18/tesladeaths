import re

import streamlit as st
from requests_html import HTMLSession, Element, HTMLResponse
import pandas as pd
import logging


logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s:%(message)s", level=logging.INFO
)


@st.cache_resource
def scrape_page_data(source) -> HTMLResponse:
    session = HTMLSession()
    r = session.get(source)
    return r


def find_last_updated(r: HTMLResponse) -> str:
    html = r.html.find("em")
    pattern = re.compile("\d{4}-\d{2}-\d{2}")
    last_updated_on = []
    for em in html:
        match = pattern.search(em.text)
        if match:
            last_updated_on.append(match.group())

    return last_updated_on[0]


def get_table_elements(r: HTMLResponse) -> Element:
    return r.html.find("#dttable", first=True)


def get_table_headers(table: Element) -> list:
    table_headers = table.find("th")[:12]

    return [row.text for row in table_headers]


def get_table_data(table: Element) -> list:
    # The last 14 tr's do not have useful data
    # The first tr has all the headings
    table_data = table.find("tr")[1:]
    rows = [row.text.split("\n")[:12] for row in table_data]

    return rows


def convert_dates(date_string) -> pd.DatetimeIndex:
    try:
        result_date = pd.to_datetime(date_string)
    except:
        logging.warning(
            f"""Could not create valid string for {date_string}. Assigning a random date."""
        )
        date_parts = date_string.split("/")
        for index, date_part in enumerate(date_parts):
            try:
                int(date_part)
            except ValueError:
                date_parts[index] = "12"
                return convert_dates("/".join(date_parts))
    else:
        return result_date


def get_table_df(r: HTMLResponse) -> pd.DataFrame:
    headers = get_table_headers(get_table_elements(r))
    rows = get_table_data(get_table_elements(r))

    df = pd.DataFrame(rows, columns=headers)

    # Converting necessary columns into int64 dtype
    integer_columns = df.columns[6:12]
    df[integer_columns] = (
        df[integer_columns].apply(pd.to_numeric, errors="coerce").fillna(0).astype(int)
    )

    df = clean_table(df)

    # Converting Date column with meaningful dates
    df["Date"] = df["Date"].apply(convert_dates)

    # Converting Years to strings
    df["Year"] = df["Year"].apply(pd.to_numeric)

    # Fix Holland --> Netherlands
    df["Country"].replace({"Holland": "Netherlands"}, inplace=True)

    return df


def clean_table(df: pd.DataFrame) -> pd.DataFrame:
    cutoff_point = df[df["Case #"] == "1"].index.values[0] + 1
    df = df.iloc[:cutoff_point]

    return df
