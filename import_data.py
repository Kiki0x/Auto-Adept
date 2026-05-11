import pandas as pd
from sqlalchemy import create_engine

print("Loading CSV file...")
df = pd.read_csv('cars_dataset.csv')

# 1. Clean up column names and make them all lowercase so MySQL is happy
df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '').str.replace('/', '_')

# 2. The Magic Fix: Drop any duplicate columns the original dataset author accidentally left in!
df = df.loc[:, ~df.columns.duplicated()]

# Connecting with your specific password
db_password = 'root123'
engine = create_engine(f'mysql+pymysql://root:{db_password}@localhost:3306/car_mentor_db')

print("Importing cars into MySQL... This might take a few seconds.")
df.to_sql(name='cars', con=engine, if_exists='replace', index=False)

print("✅ Success! All cars have been imported into your database.")
 
