import os
import pandas as pd
from sqlalchemy import create_engine
import streamlit as st 

# Load credentials from st.secrets
DB_USER = st.secrets["mysql"]["DB_USER"]
DB_PASS = st.secrets["mysql"]["DB_PASS"]
DB_HOST = st.secrets["mysql"]["DB_HOST"]
DB_PORT = st.secrets["mysql"]["DB_PORT"]
DB_NAME = st.secrets["mysql"]["DB_NAME"]

# Create DB engine
engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Folder to save cleaned CSVs
output_folder = "cleaned_data"
os.makedirs(output_folder, exist_ok=True)

# List of tables to export
tables_to_export = ["providers_data", "receivers_data", "food_listings_data", "claims_data"]

for table in tables_to_export:
    query = f"SELECT * FROM {table};"
    df = pd.read_sql(query, engine)
    file_path = os.path.join(output_folder, f"{table}.csv")
    df.to_csv(file_path, index=False)
    print(f"Exported {table} to {file_path}")