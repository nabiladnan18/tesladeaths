import pandas as pd
import streamlit as st
import plotly as pl
import altair as alt

data = pd.read_csv("./scraper/data.csv", dtype={"Year": "str"})
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
            <p>🙏 Inspired by <a href='https://tesladeaths.com'>https://tesladeaths.com</a></p>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)
# Tesla Deaths Stats


# st.dataframe(data, hide_index=True)
deaths_by_country = data.groupby("Country")[["Deaths"]].sum()
bar_chart = pl.plot(
    deaths_by_country, kind="bar", title="Deaths by country", y="Deaths"
)
st.plotly_chart(bar_chart, use_container_width=True)

grouped_df = deaths_by_country.reset_index()
grouped_df["Percentage"] = (grouped_df["Deaths"] / grouped_df["Deaths"].sum()) * 100
pie_chart = (
    alt.Chart(grouped_df)
    .mark_arc()
    .encode(
        alt.Color("Country:N"),
        alt.Tooltip(["Country:N", "Percentage:Q"]),
        theta="Percentage:Q",
    )
    .properties(width=500, height=500, title="Percentage of deaths by country")
)
st.altair_chart(pie_chart, use_container_width=True)
