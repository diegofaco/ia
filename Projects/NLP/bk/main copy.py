# Import necessary libraries
import pandas as pd
from sklearn.ensemble import IsolationForest
from datetime import timedelta
import numpy as np

# Function to convert Excel's date format to datetime
def convert_excel_date(excel_date):
    if pd.isnull(excel_date):
        return pd.to_datetime('1900-01-01')  # return a default value if excel_date is NaN
    else:
        return pd.to_datetime('1900-01-01') + timedelta(days=int(excel_date))

# Load the data
df = pd.read_csv('dataset.txt', sep='|', decimal=',', thousands='.', encoding='ISO-8859-1')

# Print the column names
print("Column names: ", df.columns)

# Convert 'Date' column to datetime and extract features
df['Date'] = df['Date'].apply(convert_excel_date)
df['DayOfWeek'] = df['Date'].dt.dayofweek
df['Month'] = df['Date'].dt.month
df['Year'] = df['Date'].dt.year

# Replace NaN values in 'Debit' and 'Credit' columns with 0
df['Debit'].fillna(0, inplace=True)
df['Credit'].fillna(0, inplace=True)

# Create a new column 'TransactionAmount' that is the difference between 'Credit' and 'Debit'
df['TransactionAmount'] = df['Credit'] - df['Debit']

# Define the features
X = df[['DayOfWeek', 'Month', 'Year', 'TransactionAmount']]

# Print the shape of X
print("Shape of X before dropping NaN values: ", X.shape)

# Drop any remaining rows with NaN values
X = X.dropna()

# Print the shape of X
print("Shape of X after dropping NaN values: ", X.shape)

# Initialize the model
model = IsolationForest(contamination=0.05, random_state=0)

# Fit the model
model.fit(X)

# Predict the anomalies in the data
df['Anomaly'] = model.predict(X)

# Print the anomaly score of the records
df['AnomalyScore'] = model.decision_function(X)

# Filter the DataFrame to only include the anomalies
anomalies = df[df['Anomaly'] == -1]

# Print the anomalies
print(anomalies)
