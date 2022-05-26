import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import plotly.express as px
now = datetime.utcnow()
today = now.strftime("%Y-%m-%d")

base_url = 'https://raw.githubusercontent.com/dsfsi/covid19za/master/data/'

confirmed_cases_data_url = base_url + 'covid19za_provincial_cumulative_timeline_confirmed.csv'
death_cases_data_url = base_url + 'covid19za_provincial_cumulative_timeline_deaths.csv'
recovery_cases_data_url = base_url+ 'covid19za_provincial_cumulative_timeline_recoveries.csv'
vaccination_data_url = base_url+'covid19za_provincial_cumulative_timeline_vaccination.csv'
test_data_url = base_url+'covid19za_timeline_testing.csv'
hospitalization_data_url = base_url+'nicd_hospital_surveillance_data.csv'

raw_data_confirmed = pd.read_csv(confirmed_cases_data_url)
raw_data_deaths = pd.read_csv(death_cases_data_url)
raw_data_recovered = pd.read_csv(recovery_cases_data_url)
raw_data_vaccinated = pd.read_csv(vaccination_data_url)
raw_data_tests = pd.read_csv(test_data_url)
raw_data_hospitalized = pd.read_csv(hospitalization_data_url)

cases_df = raw_data_confirmed[['date', 'total']]
deaths_df = raw_data_deaths[['date', 'total']]
recovery_df = raw_data_recovered[['date', 'total']]
vaccinated_df = raw_data_vaccinated[['date', 'total']]

merged_df = pd.merge(cases_df, deaths_df, how='outer', on='date')
merged_df = pd.merge(merged_df,recovery_df, how='outer', on='date')

merged_df.rename(columns={'total_x': 'Confirmed', 'total_y':'Deaths', 'total':'Recovered'}, inplace=True)

merged_df['Active'] = merged_df['Confirmed'] - (merged_df['Deaths'] + merged_df['Recovered'])

#merged_df = merged_df['Confirmed'] - merged_df['Confirmed'].shift(1)
merged_df['Daily Confirmed'] = merged_df['Confirmed']- merged_df['Confirmed'].shift(1)
merged_df['Daily Fatalities'] = merged_df['Deaths']- merged_df['Deaths'].shift(1)
merged_df['Daily Recovered'] = merged_df['Recovered']- merged_df['Recovered'].shift(1)
merged_df = merged_df.fillna(0)
# Rename the columns
def explore_page():
    st.write(merged_df)
    fig = px.bar(merged_df, x='date', y='Daily Fatalities',width=1000, height=400, title='Daily Fatalities in South Africa')
    st.write(fig)
    fig = px.bar(merged_df, x='date', y='Daily Confirmed',width=1000, height=400, title='Daily Confirmed Cases')
    st.write(fig)
    fig = px.bar(merged_df, x='date', y='Active',width=1000, height=400, title='Active Cases')
    st.write(fig)

    st.write(f'You can also access the Power BI report on [report](https://app.powerbi.com/view?r=eyJrIjoiYWM5YjkxMjQtMTE2Mi00NzQ3LWJiYjgtYTVhNWYwNDM0OGU2IiwidCI6ImVmY2ExMjYzLWY0MTYtNGVjNi04M2Y3LWU2ZjZlODUxMDViYyJ9)')
