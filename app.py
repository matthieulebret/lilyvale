import streamlit as st
import altair as alt
# import seaborn as sns

# import plotly.express as px

import numpy as np
import pandas as pd

# from timeit import default_timer as timer
# import calendar
from datetime import date, timedelta,time,datetime
import xlrd
import openpyxl

from streamlit import caching

import io

st.set_page_config('Lilyvale solar farm',layout='wide')


st.title('Lilyvale solar farm generation analysis')

st.image('https://mediacdn.acciona.com/media/zqelbp41/lilyvale-medidas.jpg')

# ###### Generation by project ####
dispatch = pd.read_csv('data_lily.csv',parse_dates=['SETTLEMENTDATE'],dtype={'DUID':'string','SCADAVALUE':'float64'}).iloc[:,1:]
dispatch.columns=['Time','Project','Dispatch']
dispatch['Time'] = pd.to_datetime(dispatch['Time'],errors='coerce')

lily = dispatch


freqlist = ['5min','30min','1H','3H','6h','12H','D','W','M','Q']

selectfreq = st.selectbox('Select frequency',freqlist,index=7)

lily.set_index('Time',inplace=True)
lily = lily.groupby('Project').resample(selectfreq).mean().reset_index()

highlight = alt.selection(type='interval',bind='scales',encodings=['x','y'])
fig = alt.Chart(lily).mark_line().encode(alt.X('Time:T'),alt.Y('Dispatch:Q'),tooltip=[
      {"type": "quantitative", "field": "Dispatch"},
      {"type": "temporal", "field": "Time"}]).add_selection(highlight)
st.altair_chart(fig,use_container_width=True)

with st.expander('Show data'):
    lily

def convert_df(df):
    return df.to_csv().encode('utf-8')

csv = convert_df(lily)

st.download_button(label = 'Download generation history as csv',data=csv,file_name='generation_history.csv',mime='text/csv')
