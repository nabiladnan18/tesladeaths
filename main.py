import pandas as pd
import streamlit as st

"""
**Hello World!** _This_ does not invoke st.write()!
"""
data = pd.read_csv("./scraper/data.csv", dtype={"Year": "str"})

# data["Year"] = data["Year"].apply(lambda x: str(x))

st.dataframe(data)
