import streamlit as st
import pandas as pd

st.title("Dataset Preview")

df = pd.read_csv(
    "sexual violence.csv",
    encoding='latin1'
)

st.dataframe(df.head())