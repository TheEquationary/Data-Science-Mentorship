import streamlit as st
import numpy as np
import pandas as pd
import requests
import json
import pytesseract
from PIL import Image
import re

response = requests.get("http://127.0.0.1:8000/get-taken-id")
id_list = response.json()

@st.cache
def get_total(selected_id):
    response = requests.get(f"http://127.0.0.1:8000/get-total-by-id/{selected_id}")
    return response.json()

st.title("PDF Invoice total calculator")

st.subheader("""Total calculation Web App""")

selected_id = st.selectbox('Select unique invoice ID', id_list)
st.write(f"Total calculated:")
st.write(get_total(selected_id))

st.header("Or")
path = st.text_input("Enter path of PDF invoice file")
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
text = str(((pytesseract.image_to_string(Image.open(f"{path}")))))
text = text.replace(',', '')
lst = re.findall('[-+]?([0-9]+\.[0-9]*)[^%]', text)
lst = np.array([float(i) for i in lst])
st.write(lst.max())