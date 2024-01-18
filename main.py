from datetime import datetime
from dateutil.relativedelta import relativedelta

import pandas as pd
import streamlit as st
import plotly as pl
import altair as alt
import math


data = pd.read_csv("./scraper/data.csv")
# data["Year"] = data["Year"].apply(lambda x: str(x))

st.markdown(
    """
    <style>
        .flex-container {
            display: flex;
            flex-direction: column;  
        }

        .flex-child {
            flex: 1;
        }  

        .flex-child:first-child {
            margin-right: 20px;
        } 

        p {
            text-align: left;
            margin-bottom: 0px;
        }
    </style>

    <div class="flex-container">
        <div class="flex-child">
            <h1>💀 Tesla Deaths </h1>
            <h3>A statistical representation of number of deaths in which a Tesla vehicle was involved.</h3>
        </div>
        <div class="first-child">
            <h5><em>DISCLAIMER: Made for educational purposes. I do not own the data!</em> 🙅</h5>
            <p style="margin-bottom:20px">🙏 Inspired by <a href='https://tesladeaths.com'>https://tesladeaths.com</a></p>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)
# Tesla Deaths Stats


# st.dataframe(data, hide_index=True)
deaths_by_country = data.groupby("Country")[["Deaths"]].sum()
total_deaths = data["Deaths"].sum()

bar_chart = pl.plot(
    deaths_by_country, kind="bar", title="Deaths by country", y="Deaths"
)


grouped_df = deaths_by_country.reset_index()
grouped_df["Percentage"] = (grouped_df["Deaths"] / grouped_df["Deaths"].sum()) * 100

pie_chart = (
    alt.Chart(
        grouped_df, width=500, height=500, title="Percentage of deaths by country"
    )
    .mark_arc()
    .encode(
        alt.Color("Country:N"),
        alt.Tooltip(["Country:N", "Percentage:Q"]),
        theta="Percentage:Q",
    )
)
deaths_by_year = data.groupby("Year")["Deaths"].sum()
mean_deaths_per_year = math.ceil(deaths_by_year.mean())
line_chart = pl.plot(deaths_by_year, kind="line", title="Deaths over time", y="Deaths")

now = datetime.now()
now_year = now.year
last_year = now - relativedelta(years=1)
last_year = last_year.year

current_year_deaths = data[data["Year"] == now_year]["Deaths"].sum()

last_year_deaths = data[data["Year"] == last_year]["Deaths"].sum()
last_year_average = data[data["Year"] == last_year]["Deaths"].mean()

col1, col2, col3, col4 = st.columns(4)

st.markdown(
    """
    <style>
        p {
            text-align: left;
            margin-bottom: 20px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

col1.metric(value=total_deaths, label="Total Deaths")
col2.metric(
    value=mean_deaths_per_year,
    label="Average Deaths",
    delta=-int(last_year_average),
    delta_color="inverse",
    help="""

    Mean deaths per year since 2013

    """,
)
col3.metric(
    value=current_year_deaths,
    label="Deaths YTD",
    delta=-int(last_year_deaths),
    delta_color="inverse",
)
col4.metric(value=last_year_deaths, label=f"Deaths in {last_year}")

st.plotly_chart(bar_chart, use_container_width=False)
st.altair_chart(pie_chart, use_container_width=False)
st.plotly_chart(line_chart, use_container_width=False)

with st.sidebar:
    options = st.selectbox("Options", ["Option 1", "Option 2", "Option3"])
    range = st.select_slider(label="Slider", options=[*range(0, 10)])
