# Import necessary libraries
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import IsolationForest
from datetime import timedelta
from statsmodels.tsa.seasonal import seasonal_decompose

# Function to convert Excel's date format to datetime
def convert_excel_date(excel_date):
    if pd.isnull(excel_date):
        return np.nan  # return NaN if excel_date is NaN
    else:
        return pd.to_datetime('1900-01-01') + timedelta(days=int(excel_date))

# Function to validate the 'Date' column
def validate_dates(df):
    return df['Date'].apply(lambda x: isinstance(x, (int, np.integer))).all()

# Load the data
df = pd.read_csv('dataset.txt', sep='|', decimal=',', thousands='.', encoding='utf-16')

# Validate the 'Date' column
if not validate_dates(df):
    print("The 'Date' column should contain integers representing Excel dates.")
else:
    # Convert 'Date' column to datetime and extract features
    df['Date'] = df['Date'].apply(convert_excel_date)
    df.dropna(subset=['Date'], inplace=True)  # drop rows with NaN dates
    df['DayOfWeek'] = df['Date'].dt.dayofweek
    df['Month'] = df['Date'].dt.month
    df['Year'] = df['Date'].dt.year
    df['DayOfMonth'] = df['Date'].dt.day
    df['Quarter'] = df['Date'].dt.quarter
    df['Week'] = df['Date'].dt.isocalendar().week  # extract week

    # Replace NaN values in 'Debit' and 'Credit' columns with 0
    df['Debit'].fillna(0, inplace=True)
    df['Credit'].fillna(0, inplace=True)

    # Create a new column 'TransactionAmount' that is the difference between 'Credit' and 'Debit'
    df['TransactionAmount'] = df['Credit'] - df['Debit']

    # Define the features
    X = df[['DayOfWeek', 'Month', 'Year', 'DayOfMonth', 'Quarter', 'TransactionAmount']]

    # Drop any remaining rows with NaN values
    X = X.dropna()

    # Initialize the model
    model = IsolationForest(contamination=0.05, random_state=0)

    # Fit the model
    model.fit(X)

    # Predict the anomalies in the data
    df['Anomaly'] = model.predict(X)

    # Print the anomaly score of the records
    df['AnomalyScore'] = model.decision_function(X)

    # Data Analysis
    print("Summary statistics for transactions:")
    print(df['TransactionAmount'].describe())

    weekly_totals = df.groupby(['Year', 'Week'])['TransactionAmount'].sum()
    print("\nWeekly totals:")
    print(weekly_totals)

    top_accounts = df['Account'].value_counts().head(10)
    print("\nTop 10 accounts with the highest number of transactions:")
    print(top_accounts)

    # Data Visualization
    fig = px.histogram(df, x='TransactionAmount', nbins=50, title='Distributionof Transaction Amounts')
    fig.show()

    fig = px.scatter(df, x=df.index, y='TransactionAmount', color='Anomaly', title='Anomalies Detected in Transactions')
    fig.show()

    fig = px.histogram(df, x='AnomalyScore', nbins=50, title='Distribution of Anomaly Scores')
    fig.show()

    fig = px.imshow(df[['DayOfWeek', 'Month', 'Year', 'DayOfMonth', 'Quarter', 'TransactionAmount']].corr(), title='Correlation Matrix of Features')
    fig.show()

    if len(df['Date'].unique()) >= 104:  # check if we have at least 104 days of data
        daily_totals = df.set_index('Date').resample('D')['TransactionAmount'].sum()
        try:
            result = seasonal_decompose(daily_totals, model='additive')
            fig = px.line(result.observed.reset_index(), x='Date', y='TransactionAmount', title='Observed Component of Time Series')
            fig.show()
            fig = px.line(result.trend.reset_index(), x='Date', y='TransactionAmount', title='Trend Component of Time Series')
            fig.show()
            fig = px.line(result.seasonal.reset_index(), x='Date', y='TransactionAmount', title='Seasonal Component of Time Series')
            fig.show()
            fig = px.line(result.resid.reset_index(), x='Date', y='TransactionAmount', title='Residual Component of Time Series')
            fig.show()
        except ValueError:
            print("Not enough data for seasonal decomposition.")
    else:
        print("Not enough data for seasonal decomposition.")

    fig = px.scatter_matrix(df[['DayOfWeek', 'Month', 'Year', 'DayOfMonth', 'Quarter', 'TransactionAmount']], title='Pair Plot of Features')
    fig.show()

    fig = px.box(df, x='Month', y='TransactionAmount', title='Boxplot of Transaction Amounts by Month')
    fig.show()
