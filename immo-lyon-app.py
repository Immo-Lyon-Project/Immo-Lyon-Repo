import streamlit as st
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go
import numpy as np

### Config
st.set_page_config(
    page_title="Covid Tracker",
    page_icon="😷",
    layout="wide"
)

DATA_URL = ('https://opendata.ecdc.europa.eu/covid19/nationalcasedeath_eueea_daily_ei/csv/data.csv')

@st.cache(allow_output_mutation=True)
def load_data():
    data = pd.read_csv(DATA_URL)
    return data



### App
st.title("Covid Tracker")

st.markdown("""
            👋 Hello there! Welcome to this simple covid tracker app. We simply track the evolution of cases accross the world. Data comes from the European Centre for Disease Prevention and Control (ECDC)

            Check out data here: [Data on the daily number of new reported COVID-19 cases and deaths by EU/EEA country](https://www.ecdc.europa.eu/en/publications-data/data-daily-new-cases-covid-19-eueea-country)
            """)

st.caption('At the moment of this app, data was lastly collected on December 25th 2021')

data_load_state = st.text('Loading data...')
data = load_data()

data['dateRep']= pd.to_datetime(data['dateRep'])
data.sort_values('dateRep')
data_cumulated_cases = data.groupby(['dateRep'], as_index=False).sum()
data_cumulated_cases.sort_values('dateRep')
data_cumulated_cases['cumSumCases'] = data_cumulated_cases['cases'].cumsum()
data_cumulated_cases['avgCases'] = data_cumulated_cases['cases'].rolling(7).mean()
data_cumulated_cases.fillna(0)

agree = st.checkbox('Show raw data')

if agree:
    st.header("Raw data")
    st.dataframe(data)



st.header("World Analysis")

st.subheader("Cumulated cases")

fig = px.area(data_cumulated_cases, y="cumSumCases", x="dateRep")
st.plotly_chart(fig, use_container_width=True)

st.subheader("New cases")

fig = px.line(data_cumulated_cases, y=["cases", "avgCases"], x="dateRep")
st.plotly_chart(fig, use_container_width=True)