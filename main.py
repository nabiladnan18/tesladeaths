from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import streamlit as st
import plotly as pl
import altair as alt
import math

from app.utils import scrape_page_data, find_last_updated, get_table_df

st.set_page_config(layout="wide", page_title="💀 Tesla Deaths")

SOURCE = "https://www.tesladeaths.com"

scraped_page = scrape_page_data(SOURCE)

data = get_table_df(scraped_page)


# with st.sidebar:
#     options = st.selectbox("Options", ["Option 1", "Option 2", "Option3"])
#     range = st.select_slider(label="Slider", options=[*range(0, 10)])


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

st.markdown(
    """
    <p>Last data found on: {date}</p> 
    """.format(date=find_last_updated(scraped_page)),
    unsafe_allow_html=True,
)


deaths_by_country = data.groupby("Country")[["Deaths"]].sum()
total_deaths = data["Deaths"].sum()
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
# line_chart = pl.plot(
#     deaths_by_year,
#     kind="scatter",
#     title="Deaths over time",
#     y="Deaths",
# )

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

# regular barchart
bar_chart = pl.plot(
    deaths_by_country,
    kind="bar",
    title="Deaths by country",
    y="Deaths",
)

df = data.loc[
    :,
    [
        "Country",
        "Tesla driver",
        "Tesla occupant",
        "Other vehicle",
        "Cyclists/ Peds",
    ],
]

df = (
    df.groupby("Country")[
        [
            "Tesla driver",
            "Tesla occupant",
            "Other vehicle",
            "Cyclists/ Peds",
        ]
    ]
    .sum()
    .reset_index()
)


categorywise_deaths_long = pd.melt(
    df,
    id_vars=["Country"],
    value_vars=[
        "Tesla driver",
        "Tesla occupant",
        "Other vehicle",
        "Cyclists/ Peds",
    ],
    value_name="Deaths",
    var_name="Category",
)


stacked_chart = (
    alt.Chart(categorywise_deaths_long)
    .mark_bar()
    .encode(
        x=alt.X("Country", type="nominal").axis(title="Country"),
        y=alt.Y("Deaths", type="quantitative", stack="normalize").axis(
            title="Deaths", format="%"
        ),
        color=alt.Color("Category"),
        tooltip=["Category", "Deaths:Q"],
    )
    .properties(
        height=400,
        title="Category by country",
    )
)

# Dummy Deployment To Test Jenkins Pipeline

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
col4.metric(value=last_year_deaths, label="Deaths in previous year")

col1, col2 = st.columns([6, 4])

col1.plotly_chart(bar_chart, use_container_width=True)
col2.altair_chart(pie_chart, use_container_width=True)

st.altair_chart(stacked_chart, use_container_width=True)
# st.plotly_chart(line_chart, use_container_width=False)

deaths_by_year_no_index = deaths_by_year.reset_index()
deaths_by_year = (
    alt.Chart(deaths_by_year_no_index)
    .mark_bar()
    .encode(
        x=alt.X("Year", type="nominal").axis(title="Years"),
        y=alt.Y("Deaths", type="quantitative"),
        tooltip=["Year:N", "Deaths:Q"],
    )
    .properties(title="Deaths over time")
)
mean_line = (
    alt.Chart(pd.DataFrame({"mean_deaths": [mean_deaths_per_year]}))
    .mark_rule(color="red")
    .encode(y="mean_deaths:Q")
)
final_chart = deaths_by_year + mean_line

st.altair_chart(final_chart, use_container_width=True)
