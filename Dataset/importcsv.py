import pandas as pd
from sqlalchemy import create_engine

# Connection details
user = "root"
password = "admin" 
host = "127.0.0.1"
port = 3306
database = "Food"  

# CSV file path
csv_file_path = "/Users/karthikdoguparthi/Downloads/Studies/Labmentix/LocalFoodWastageManagementSystem/Dataset/providers_data.csv"

# Read CSV into DataFrame
df = pd.read_csv(csv_file_path)

# Create MySQL connection engine
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")

# Upload DataFrame to MySQL table
df.to_sql("providers_data", con=engine, if_exists="append", index=False)  
# if_exists="append" adds data, use "replace" to overwrite table

print("CSV data uploaded successfully!")