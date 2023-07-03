import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from scipy.spatial import distance
from dash import dash_table as dt
from dash import dcc
from dash import html
from dash import Dash
from dash.dependencies import Input, Output
import plotly.express as px

def load_and_clean_data(file_path):
    # Load the data
    data = pd.read_csv(file_path, sep='|', decimal=',', encoding='UTF-16')

    # Fill missing 'CP' values with "No info"
    data['CP'] = data['CP'].fillna("No info")

    # Convert the 'Date' column to datetime format
    data['Date'] = pd.to_datetime(data['Date'], origin='1899-12-30', unit='D')

    # Create 'Transaction Amount' feature
    data['Transaction Amount'] = data['Debit'] - data['Credit']

    # Create 'Day of Week' feature
    data['Day of Week'] = data['Date'].dt.dayofweek

    # Create 'Time Since Last Transaction' feature
    data = data.sort_values('Date')
    data['Time Since Last Transaction'] = data.groupby('Account')['Date'].diff().dt.days

    return data

def detect_anomalies_kmeans(data):
    # Select the numerical features
    features = ['Debit', 'Credit', 'Transaction Amount', 'Time Since Last Transaction']
    data_num = data.dropna(subset=features)

    # Scale the features
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data_num[features])

    # Apply the K-means algorithm
    kmeans = KMeans(n_clusters=5, random_state=0)
    kmeans.fit(data_scaled)

    # Calculate the distance to the nearest cluster center
    distances = kmeans.transform(data_scaled).min(axis=1)

    # Flag transactions that are far from any cluster center as potential anomalies
    threshold = distances.mean() + 3*distances.std()
    anomalies = data_num[distances > threshold]

    return anomalies

# Load and clean the data
data = load_and_clean_data('dataset.txt')

# Detect anomalies using K-means
anomalies = detect_anomalies_kmeans(data)

# Create a Dash app
app = Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    dt.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in anomalies.columns],
        data=anomalies.to_dict('records'),
        page_size=10,
    ),
    dcc.Graph(id='graph'),
    dcc.Graph(id='scatter_matrix', figure=px.scatter_matrix(data, dimensions=['Debit', 'Credit', 'Transaction Amount', 'Time Since Last Transaction']))
])

# Define the callback of the app
@app.callback(
    Output('graph', 'figure'),
    Input('table', 'selected_rows'),
)
def update_graph(selected_rows):
    if selected_rows is None:
        selected_rows = []
    figure = px.histogram(anomalies.iloc[selected_rows] if selected_rows else anomalies, x="Transaction Amount")
    return figure

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)