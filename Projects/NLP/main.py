import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.svm import OneClassSVM
from sklearn.neighbors import LocalOutlierFactor
from dash import dash_table as dt
from dash import dcc
from dash import html
from dash import Dash
from dash.dependencies import Input, Output, State
import plotly.express as px
import dash_bootstrap_components as dbc

class DataLoader:
    @staticmethod
    def load_and_clean_data(file_path):
        data = pd.read_csv(file_path, sep='|', decimal=',', encoding='UTF-16')
        data['CP'] = data['CP'].fillna("No info")
        data['Date'] = pd.to_datetime(data['Date'], origin='1899-12-30', unit='D')
        data['Net Transaction Amount'] = data['Debit'] - data['Credit']
        data['Day of Week'] = data['Date'].dt.dayofweek
        data = data.sort_values(['Account', 'Date'])
        data['Time Since Last Transaction'] = data.groupby('Account')['Date'].diff().dt.days
        data['Credit-Debit Ratio'] = np.where(data['Debit'] != 0, data['Credit'] / data['Debit'], np.inf)
        data['Account First Char'] = data['Account'].apply(lambda x: x[0])

        return data

class FeatureEngineer:
    @staticmethod
    def engineer_features(data):
        data['Week of Year'] = data['Date'].dt.isocalendar().week
        data['Month'] = data['Date'].dt.month
        data['Quarter'] = data['Date'].dt.quarter
        data['Year'] = data['Date'].dt.year

        return data

class AnomalyDetector:
    @staticmethod
    def detect_anomalies(data):
        features = ['Debit', 'Credit', 'Net Transaction Amount', 'Time Since Last Transaction']
        data_num = data.dropna(subset=features)
        scaler = StandardScaler()
        data_scaled = scaler.fit_transform(data_num[features])

        # KMeans
        kmeans = KMeans(n_clusters=5, random_state=0)
        kmeans.fit(data_scaled)
        distances = kmeans.transform(data_scaled).min(axis=1)
        threshold = distances.mean() + 3*distances.std()
        anomalies_kmeans = data_num[distances > threshold]

        # Isolation Forest
        iforest = IsolationForest(contamination=0.01, random_state=0)
        anomalies_iforest = data_num[iforest.fit_predict(data_scaled) == -1]

        # One-Class SVM
        ocsvm = OneClassSVM(nu=0.01)
        anomalies_ocsvm = data_num[ocsvm.fit_predict(data_scaled) == -1]

        # Local Outlier Factor
        lof = LocalOutlierFactor(n_neighbors=20, contamination=0.01)
        anomalies_lof = data_num[lof.fit_predict(data_scaled) == -1]

        # Ensemble
        anomalies = pd.concat([anomalies_kmeans.drop(columns='Date'), 
                               anomalies_iforest.drop(columns='Date'), 
                               anomalies_ocsvm.drop(columns='Date'), 
                               anomalies_lof.drop(columns='Date')])
        anomalies['vote'] = 1
        anomalies = anomalies.groupby(level=0).sum()
        anomalies = data.loc[anomalies.index]  # Get original data for anomalies
        if 'vote' in anomalies.columns:
            anomalies['vote'] = anomalies['vote'] > 2  # Majority vote
            
        return anomalies

class Dashboard:
    def __init__(self, data, anomalies):
        self.data = data
        self.anomalies = anomalies
        self.app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

        self.setup_layout()
        self.setup_callbacks()

    def setup_layout(self):
        self.app.layout = dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H1("Transaction Dashboard"),
                    html.P("Use the controls below to update the dashboard."),
                    html.Label("Date Range"),
                    dcc.DatePickerRange(
                        id='date-range',
                        min_date_allowed=self.data['Date'].min(),
                        max_date_allowed=self.data['Date'].max(),
                        start_date=self.data['Date'].min(),
                        end_date=self.data['Date'].max()
                    ),
                    html.Label("Account"),
                    dcc.Dropdown(
                        id='account',
                        options=[{'label': i, 'value': i} for i in self.data['Account'].unique()],
                        multi=True
                    ),
                    html.Label("Transaction Amount"),
                    dcc.RangeSlider(
                        id='amount',
                        min=self.data['Net Transaction Amount'].min(),
                        max=self.data['Net Transaction Amount'].max(),
                        step=1,
                        value=[self.data['Net Transaction Amount'].min(), self.data['Net Transaction Amount'].max()]
                    ),
                    html.Label("Day of Week"),
                    dcc.Dropdown(
                        id='day-of-week',
                        options=[{'label': i, 'value': i} for i in self.data['Day of Week'].unique()],
                        multi=True
                    ),
                    html.Label("Week of Year"),
                    dcc.Dropdown(
                        id='week-of-year',
                        options=[{'label': i, 'value': i} for i in self.data['Week of Year'].unique()],
                        multi=True
                    ),
                    html.Label("Month"),
                    dcc.Dropdown(
                        id='month',
                        options=[{'label': i, 'value': i} for i in self.data['Month'].unique()],
                        multi=True
                    ),
                    html.Label("Quarter"),
                    dcc.Dropdown(
                        id='quarter',
                        options=[{'label': i, 'value': i} for i in self.data['Quarter'].unique()],
                        multi=True
                    ),
                    html.Label("Year"),
                    dcc.Dropdown(
                        id='year',
                        options=[{'label': i, 'value': i} for i in self.data['Year'].unique()],
                        multi=True
                    ),
                    html.Label("Account First Char"),
                    dcc.Dropdown(
                        id='account-first-char',
                        options=[{'label': i, 'value': i} for i in self.data['Account First Char'].unique()],
                        multi=True
                    ),
                ], md=4),
                dbc.Col([
                    dcc.Graph(id='time-series-plot'),
                    dt.DataTable(
                        id='table',
                        columns=[{"name": i, "id": i} for i in self.data.columns],
                        data=self.data.to_dict('records'),
                        style_table={'overflowX': 'auto'},
                        page_size=10,
                        filter_action="native",
                        sort_action="native",
                        sort_mode="multi",
                        selected_rows=[],
                        page_action="native",
                        page_current= 0,
                    ),
                ], md=8),
            ]),
        ], fluid=True)

    def setup_callbacks(self):
        @self.app.callback(
            Output('time-series-plot', 'figure'),
            Output('table', 'data'),
            Input('date-range', 'start_date'),
            Input('date-range', 'end_date'),
            Input('account', 'value'),
            Input('amount', 'value'),
            Input('day-of-week', 'value'),
            Input('week-of-year', 'value'),
            Input('month', 'value'),
            Input('quarter', 'value'),
            Input('year', 'value'),
            Input('account-first-char', 'value'),
        )
        def update_dashboard(start_date, end_date, account, amount, day_of_week, week_of_year, month, quarter, year, account_first_char):
            filtered_data = self.data[(self.data['Date'] >= start_date) & (self.data['Date'] <= end_date)]
            if account is not None:
                filtered_data = filtered_data[filtered_data['Account'].isin(account)]
            if amount is not None:
                filtered_data = filtered_data[(filtered_data['Net Transaction Amount'] >= amount[0]) & (filtered_data['Net Transaction Amount'] <= amount[1])]
            if day_of_week is not None:
                filtered_data = filtered_data[filtered_data['Day of Week'].isin(day_of_week)]
            if week_of_year is not None:
                filtered_data = filtered_data[filtered_data['Week of Year'].isin(week_of_year)]
            if month is not None:
                filtered_data = filtered_data[filtered_data['Month'].isin(month)]
            if quarter is not None:
                filtered_data = filtered_data[filtered_data['Quarter'].isin(quarter)]
            if year is not None:
                filtered_data = filtered_data[filtered_data['Year'].isin(year)]
            if account_first_char is not None:
                filtered_data = filtered_data[filtered_data['Account First Char'].isin(account_first_char)]

            figure = px.line(filtered_data, x='Date', y='Net Transaction Amount', color='Account', title='Net Transaction Amount Over Time')

            return figure, filtered_data.to_dict('records')

    def run(self):
        self.app.run_server(debug=True)

if __name__ == "__main__":
    data_loader = DataLoader()
    feature_engineer = FeatureEngineer()
    anomaly_detector = AnomalyDetector()

    data = data_loader.load_and_clean_data('Dataset.txt')
    data = feature_engineer.engineer_features(data)
    anomalies = anomaly_detector.detect_anomalies(data)

    dashboard = Dashboard(data, anomalies)
    dashboard.run()