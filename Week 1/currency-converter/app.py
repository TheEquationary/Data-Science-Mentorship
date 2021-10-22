from os import name
import streamlit as st
from PIL import Image
import pandas as pd
import requests
import json

image = Image.open('logo.png')
st.image(image, width=390)

st.title('Currency cinverter app')
st.markdown("""This app coverts currency from one country to another!""")
st.sidebar.header('Input Options')

currency_list = ['USD', 'EUR', 'GBP', 'INR', 'AUD', 'CAD', 'SGD', 'CHF']
base_price_unit = st.sidebar.selectbox('Select base currency for conversion', currency_list)
symbols_price_unit = st.sidebar.selectbox('Select target currency', currency_list)

@st.cache
def load_data():
    url = ''.join(['https://api.ratesapi.io/api/latest?base=', base_price_unit, '&symbols=', symbols_price_unit])
    response = requests.get(url)
    data = response.json()
    base_currency = pd.Series(data['base'], name='base_currency')
    rates_df = pd.DataFrame.from_dict(data['rates'].items())
    rates_df.columns = ['converted_currency', 'price']
    conversion_date = pd.Series(data['date'], name='date')
    df = pd.concat([base_currency, rates_df, conversion_date], axis=1)
    return df

df = load_data()

st.header('Currency conversion')

st.write(df)

expander_bar = st.beta_expander("About")
expander_bar.markdown("""
* **Python libraries:** streamlit, pandas, pillow, requests, json
* **Data source:** [ratesapi.io](https://ratesapi.io/) which is based on data published by [European Central Bank](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html)
* **Credit:** App built by [Chanin Nantasenamat](http://twitter.com/thedataprof) (aka [Data Professor](http://youtube.com/dataprofessor))
""")