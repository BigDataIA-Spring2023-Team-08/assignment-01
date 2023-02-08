import os
import sqlite3
import pandas as pd
from pathlib import Path
import streamlit as st
from db_goes18 import query_into_dataframe, create_database

database_file_name = 'assignment1.db'
database_file_path = os.path.join(os.path.dirname(__file__),database_file_name)
print("File path", database_file_path)

@st.cache
def get_year():
    db = sqlite3.connect(database_file_path)
    df_year = pd.read_sql_query("SELECT year from goes", db)
    return df_year

year_data = get_year()
year = st.selectbox('Year',[year_data],key = 'year')

def get_day():
     db = sqlite3.connect(database_file_path)
     df_day = pd.read_sql_query("SELECT day from goes", db)

     return df_day
day_data = get_day()
day = st.selectbox('Day',[day_data])

def get_hour():
      db = sqlite3.connect(database_file_path)
      df_hour = pd.read_sql_query("SELECT hour from goes ", db)

      return df_hour
hour_data = get_hour()
hour = st.selectbox('Hour',[hour_data]) 










