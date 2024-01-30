import streamlit as st
# set width
st.set_page_config(layout="wide")
import pandas as pd
import plotly.express as px
from utils.bi_dashboar_utils import *

data = get_data()

st.title('Business Intelligence Dashboard')
st.write('This dashboard is a demo of a BI dashboard built with Streamlit. Of the superstore dataset')
#Write filter row
write_filter_row(data)

#Write KPI row
write_kpi_row(data)

#Write row with map and top 10 states
col1, col2 = st.columns([0.25,0.75])
with col1:
    fig = get_top_10_states(data, state = st.session_state['state'])
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = get_map(data)
    st.plotly_chart(fig, use_container_width=True)

#Two columns with time series data over the top 10 products
col1, col2 = st.columns(2)
with col1:
    get_time_series_plot(data)

with col2:

    # A plot showing revenue over time for either all or the selected state
    fig = get_revenue_plot(data)









