import pandas as pd
from plotnine import *
from datetime import timedelta

# Load the data
df = pd.read_excel('Dataset.xlsx', engine='openpyxl')

# Convert Excel date format to datetime
df['Date'] = pd.to_datetime('1900-01-01') + pd.to_timedelta(df['Date'], 'D')

# Convert 'Debit' and 'Credit' columns to numeric
df['Debit'] = df['Debit'].str.replace('.', '').str.replace(',', '.').astype(float)
df['Credit'] = df['Credit'].str.replace('.', '').str.replace(',', '.').astype(float)

# Display the first few rows
print(df.head())