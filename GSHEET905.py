# Directly connected to the google sheets attempt
import streamlit as st
from streamlit_gsheets import GSheetsConnection

url = "https://docs.google.com/spreadsheets/d/14n6SMM0OtUjeE2fci37hSG0UdjKsdJTp5EyTWJiCT4Q/edit?gid=0#gid=0"

conn = st.connection("gsheets", type=GSheetsConnection)

data = conn.read(spreadsheet=url, usecols=[0, 1])
st.dataframe(data)
