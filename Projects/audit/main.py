import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN

class DataProcessor:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_and_clean_data(self):
        # Load the data
        data = pd.read_csv(self.file_path, sep='|', decimal=',', encoding='UTF-16')

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

        # Create 'Transaction Frequency' feature
        transaction_frequency = data.groupby(['Date', 'Account']).size().reset_index(name='Transaction Frequency')
        data = pd.merge(data, transaction_frequency, how='left', on=['Date', 'Account'])

        # Create 'Average Transaction Amount' feature
        average_transaction_amount = data.groupby(['Date', 'Account'])['Transaction Amount'].mean().reset_index(name='Average Transaction Amount')
        data = pd.merge(data, average_transaction_amount, how='left', on=['Date', 'Account'])

        # Create 'Transaction Variance' feature
        transaction_variance = data.groupby(['Date', 'Account'])['Transaction Amount'].var().reset_index(name='Transaction Variance')
        data = pd.merge(data, transaction_variance, how='left', on=['Date', 'Account'])

        return data


class AnomalyDetector:
    def __init__(self, data):
        self.data = data

    def detect_anomalies_isolation_forest(self):
        # Existing code...

    def detect_anomalies_dbscan(self):
        # Select the numerical features
        features = ['Debit', 'Credit', 'Transaction Amount', 'Time Since Last Transaction', 'Transaction Frequency', 'Average Transaction Amount', 'Transaction Variance']
        data_num = self.data.dropna(subset=features)

        # Scale the features
        scaler = StandardScaler()
        data_scaled = scaler.fit_transform(data_num[features])

        # Apply the DBSCAN algorithm
        dbscan = DBSCAN(eps=3, min_samples=2)
        labels = dbscan.fit_predict(data_scaled)

        # Flag transactions that are detected as anomalies
        anomalies = data_num[labels == -1]

        return anomalies


def main():
    # Load and clean the data
    processor = DataProcessor('dataset.txt')
    data = processor.load_and_clean_data()

    # Detect anomalies using Isolation Forest
    detector = AnomalyDetector(data)
    anomalies = detector.detect_anomalies_isolation_forest()

    # Print the anomalies
    print(anomalies)

    # Print a summary of the numerical features
    numerical_features = ['Debit', 'Credit', 'Transaction Amount', 'Time Since Last Transaction', 'Transaction Frequency', 'Average Transaction Amount', 'Transaction Variance']
    print(data[numerical_features].describe())

    # Plot histograms and box plots for numerical features
    for feature in numerical_features:
        plt.figure(figsize=(10, 6))
        sns.histplot(data[feature], bins=30, color='blue', label='Normal')
        sns.histplot(anomalies[feature], bins=30, color='red', label='Anomaly')
        plt.title(f'{feature} Distribution')
        plt.xlabel(feature)
        plt.ylabel('Frequency')
        plt.legend()
        plt.show()

        plt.figure(figsize=(10, 6))
        sns.boxplot(x=data[feature])
        plt.title(f'{feature} Box Plot')
        plt.xlabel(feature)
        plt.show()

    # Plot heatmap for correlation matrix
    plt.figure(figsize=(10, 6))
    sns.heatmap(data[numerical_features].corr(), annot=True, cmap='coolwarm')
    plt.title('Correlation Matrix')
    plt.show()

if __name__ == "__main__":
    main()

