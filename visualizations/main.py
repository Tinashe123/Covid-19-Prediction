from Explore import explore_page
from Predict import predict_page
import streamlit as st
from datetime import datetime, timedelta
now = datetime.utcnow()
today = now.strftime("%Y-%m-%d")

selection = st.sidebar.selectbox('Select', ('Explore', 'Predict'))


st.header(today)
if selection == 'Explore':
    explore_page()
else:
    model = st.sidebar.selectbox('Select Model', ('SIR Model', 'LSTM'))
    if model == 'SIR Model':
        st.header(f'{model} selected')
        predict_page()
    else:
        st.header(f'{model} selected')
        st.write('LSTM Loading...')




