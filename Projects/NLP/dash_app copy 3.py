import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.svm import OneClassSVM
from sklearn.neighbors import LocalOutlierFactor
from scipy.spatial import distance
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
        self.external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
        self.app = Dash(__name__, external_stylesheets=self.external_stylesheets)
        self.setup_layout()
        self.setup_callbacks()
        
    def setup_layout(self):
        self.app.layout = dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H1('Accounting Transactions Dashboard', style={'textAlign': 'center', 'margin': '10px'}),
                    html.Hr(),
                    dbc.Card([
                        dbc.CardHeader("Filters"),
                        dbc.CardBody([
                            html.H3('Filters', style={'textAlign': 'left'}),
                            dcc.DatePickerRange(
                                id='date-range',
                                min_date_allowed=self.data['Date'].min(),
                                max_date_allowed=self.data['Date'].max(),
                                start_date=self.data['Date'].min(),
                                end_date=self.data['Date'].max(),
                                style={'margin': '10px'}
                            ),
                            dcc.Dropdown(
                                id='account',
                                options=[{'label': i, 'value': i} for i in self.data['Account'].unique()],
                                multi=True,
                                style={'margin': '10px'}
                            ),
                            dcc.RangeSlider(
                                id='amount',
                                min=self.data['Net Transaction Amount'].min(),
                                max=self.data['Net Transaction Amount'].max(),
                                value=[self.data['Net Transaction Amount'].min(), self.data['Net Transaction Amount'].max()]
                            ),
                            dcc.Dropdown(
                                id='transaction-type',
                                options=[
                                    {'label': 'Debit', 'value': 'Debit'},
                                    {'label': 'Credit', 'value': 'Credit'},
                                    {'label': 'Net Transaction Amount', 'value': 'Net Transaction Amount'}
                                ],
                                value='Net Transaction Amount',
                                style={'margin': '10px'}
                            ),
                            html.Button('Update', id='update-button', style={'margin': '10px'}),
                        ]),
                    ], style={'margin': '10px'}),
                    html.Hr(),
                    dbc.Card([
                        dbc.CardHeader("Summary"),
                        dbc.CardBody([
                            html.H3('Summary', style={'textAlign': 'left'}),
                            html.H4(id='total-transactions', className='card-title'),
                            html.P(id='total-debit', className='card-text'),
                            html.P(id='total-credit', className='card-text'),
                            html.P(id='total-net', className='card-text'),
                        ]),
                    ], style={'margin': '10px'}),
                    html.Hr(),
                ], style={'padding': '5px', 'margin': '5px', 'font-family': 'Arial', 'font-size': '14px', 'color': '#000000'}),
            ], style={'background-color': '#f8f9fa'}),
            dbc.Row([
                dbc.Col([
                    html.H3('Anomalies', style={'textAlign': 'left', 'margin': '10px'}),
                    dt.DataTable(
                        id='table',
                        columns=[
                            {"name": i, "id": i, 'type': 'numeric', 'format': Format(group=',', decimal_delimiter='.', precision=2, scheme=Scheme.fixed)} if i in ['Debit', 'Credit', 'Net Transaction Amount'] else {"name": i, "id": i} for i in self.anomalies.columns
                        ],
                        data=self.anomalies.to_dict('records'),
                        page_size=10,
                        row_selectable='multi',
                        sort_action='native',  # enables sorting
                        export_format='csv',  # enables exporting
                    ),
                    dcc.Graph(id='graph', style={'margin': '10px'}),
                    dcc.Graph(id='scatter_matrix', figure=px.scatter_matrix(self.data, dimensions=['Debit', 'Credit', 'Net Transaction Amount', 'Time Since Last Transaction']), style={'margin': '10px'})
                ], style={'padding': '5px', 'margin': '5px', 'font-family': 'Arial', 'font-size': '14px', 'color': '#000000'}),
            ], style={'background-color': '#f8f9fa'}),
        ], fluid=True)


    def setup_callbacks(self):
        @self.app.callback(
            [Output('total-transactions', 'children'),
             Output('total-debit', 'children'),
             Output('total-credit', 'children'),
             Output('total-net', 'children')],
            Input('transaction-type', 'value')
        )
        def update_summary(transaction_type):
            total_transactions = 'Total Transactions: ' + str(len(self.data))
            total_debit = 'Total Debit: ' + str(self.data['Debit'].sum()) if transaction_type == 'Debit' else ''
            total_credit = 'Total Credit: ' + str(self.data['Credit'].sum()) if transaction_type == 'Credit' else ''
            total_net = 'Total Net Transaction Amount: ' + str(self.data['Net Transaction Amount'].sum()) if transaction_type == 'Net Transaction Amount' else ''
            return total_transactions, total_debit, total_credit, total_net

        @self.app.callback(
            Output('graph', 'figure'),
            [Input('table', 'selected_rows'),
             Input('transaction-type', 'value')],
            State('table', 'data')
        )
        def update_graph(selected_rows, transaction_type, data):
            if selected_rows is None:
                selected_rows = []
            selected_data = pd.DataFrame(data).iloc[selected_rows] if selected_rows else pd.DataFrame(data)
            figure = px.histogram(selected_data, x=transaction_type)
            return figure

    def run(self):
        self.app.run_server(debug=True)

if __name__ == '__main__':
    data = DataLoader.load_and_clean_data('dataset.txt')
    data = FeatureEngineer.engineer_features(data)
    anomalies = AnomalyDetector.detect_anomalies(data)
    dashboard = Dashboard(data, anomalies)
    dashboard.run()
