import pandas as pd
import numpy as np
from dash import dcc, html, Dash
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc

class DataLoader:
    @staticmethod
    def load_and_clean_data(file_path):
        data = pd.read_csv(file_path, sep='|', decimal=',', encoding='UTF-16')
        data['CP'] = data['CP'].fillna("No info")
        data['Date'] = pd.to_datetime(data['Date'], origin='1899-12-30', unit='D')
        data['Net Transaction Amount'] = data['Debit'] - data['Credit']
        data['Day of Year'] = data['Date'].dt.dayofyear
        data = data.sort_values(['Account', 'Date'])
        data['Time Since Last Transaction'] = data.groupby('Account')['Date'].diff().dt.days
        data['Credit-Debit Ratio'] = np.where(data['Debit'] != 0, data['Credit'] / data['Debit'], np.inf)
        data['Account First Char'] = data['Account'].apply(lambda x: x[0])
        return data

class Dashboard:
    def __init__(self, data):
        self.data = data
        self.app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
        self.setup_layout()
        self.setup_callbacks()

    def setup_layout(self):
        self.app.layout = dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H1("Transaction Dashboard"),
                    html.P("Use the controls below to update the dashboard."),
                    html.Label("Account"),
                    dcc.Dropdown(
                        id='account',
                        options=[{'label': i, 'value': i} for i in self.data['Account'].unique()],
                        multi=True
                    ),
                    html.Label("Day of Year"),
                    dcc.RangeSlider(
                        id='day-of-year',
                        min=self.data['Day of Year'].min(),
                        max=self.data['Day of Year'].max(),
                        step=1,
                        value=[self.data['Day of Year'].min(), self.data['Day of Year'].max()]
                    ),
                ], md=4),
                dbc.Col([
                    dcc.Graph(id='heatmap'),
                ], md=8),
            ]),
        ], fluid=True)

    def setup_callbacks(self):
        @self.app.callback(
            Output('heatmap', 'figure'),
            Input('account', 'value'),
            Input('day-of-year', 'value'),
        )
        def update_heatmap(account, day_of_year):
            filtered_data = self.data
            if account is not None:
                filtered_data = filtered_data[filtered_data['Account'].isin(account)]
            if day_of_year is not None:
                filtered_data = filtered_data[(filtered_data['Day of Year'] >= day_of_year[0]) & (filtered_data['Day of Year'] <= day_of_year[1])]
            figure = px.density_heatmap(filtered_data, x='Day of Year', y='Net Transaction Amount', nbinsx=365)
            return figure

    def run(self):
        self.app.run_server(debug=True)

if __name__ == "__main__":
    data_loader = DataLoader()
    data = data_loader.load_and_clean_data('Dataset.txt')
    dashboard = Dashboard(data)
    dashboard.run()
