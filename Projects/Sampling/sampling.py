import pandas as pd
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QGridLayout, QFileDialog, QMessageBox
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest


class AuditTool:
    REQ_COLS = ['Account', 'Account_Description', 'Date', 'Historic', 'ID_Batch', 'Debit', 'Credit']
    INT_COLS = ['Debit', 'Credit']

    def __init__(self, master=None):
        self.master = master
        self.file_input_frame = self.create_frame("File Input", self.select_file, "Select your data file: [Browse...]")
        self.sampling_config_frame = self.create_frame("Sampling Configuration", self.select_sampling_method, "Select sampling method: [Dropdown menu]")
        self.audit_measures_frame = self.create_frame("Audit Measures", self.enter_overall_materiality, "Overall Materiality: [Input field]")
        self.run_sampling_frame = self.create_frame("Run Sampling", self.run_sampling, "Start")
        self.results_frame = self.create_frame("Results", self.display_results, "[Placeholder for results]")

    def create_frame(self, text, command, button_text):
        frame = QWidget(self.master)
        frame_layout = QVBoxLayout()
        frame.setLayout(frame_layout)
        
        label = QLabel(text)
        button = QPushButton(button_text)
        button.clicked.connect(command)
        
        frame_layout.addWidget(label)
        frame_layout.addWidget(button)
        
        return frame

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(None, "Select File", "", "Excel Files (*.xlsx);;CSV Files (*.csv);;Text Files (*.txt)")
        if file_path:
            self.load_data(file_path)

    def load_data(self, file_path):
        try:
            self.data = pd.read_excel(file_path) if file_path.endswith('.xlsx') else pd.read_csv(file_path)
            if not set(self.REQ_COLS).issubset(self.data.columns):
                QMessageBox.critical(None, "Invalid File", "The selected file does not contain the required columns.")
            else:
                self.data = self.data.fillna('')
                QMessageBox.information(None, "File Selected", "File has been successfully loaded.")
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e))

    def view_stats(self):
        desc_stats = self.data[self.INT_COLS].describe()
        self.data[self.INT_COLS].hist()
        outliers = self.data[(np.abs(self.data[self.INT_COLS] - self.data[self.INT_COLS].mean()) > (3 * self.data[self.INT_COLS].std()))]
        sns.pairplot(self.data[self.INT_COLS])
        plt.show()
        print(desc_stats, outliers)

    def select_sampling_method(self):
        # code to select sampling method goes here
        pass

    def enter_overall_materiality(self):
        # code to enter overall materiality goes here
        pass

    def run_sampling(self):
        # code to run sampling goes here
        pass

    def display_results(self):
        # code to display results goes here
        pass


class DataProcessor:
    def __init__(self, data):
        self.data = data

    def interval_selection(self, n):
        return self.data.iloc[range(0, len(self.data), len(self.data) // n)]

    def monetary_unit_sampling(self, n, seed=None):
        np.random.seed(seed or np.random.randint(0, 2**32 - 1))
        total_value = self.data['Value'].sum()
        probabilities = self.data['Value'] / total_value
        return self.data.sample(n, weights=probabilities)

    def stratified_sampling(self, n_dict, min_group_size=0, seed=None):
        np.random.seed(seed or np.random.randint(0, 2**32 - 1))
        groups = self.data.groupby('Group').filter(lambda x: len(x) >= min_group_size)
        return groups.groupby('Group').apply(lambda x: x.sample(n=n_dict.get(x.name, 0)))

    def cluster_sampling(self, n_clusters, seed=None):
        np.random.seed(seed or np.random.randint(0, 2**32 - 1))
        clusters = self.data.groupby('Group')
        selected_clusters = np.random.choice(clusters.groups.keys(), size=n_clusters)
        return self.data[self.data['Group'].isin(selected_clusters)]

    def fibonacci_sampling(self):
        fib_sequence = [0, 1]
        while fib_sequence[-1] < len(self.data):
            fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
        sorted_data = self.data.sort_values(by='Value', ascending=False)
        return sorted_data.iloc[fib_sequence[1:-1]]

    def kmeans_sampling(self, n_clusters, n_samples, seed=None):
        np.random.seed(seed or np.random.randint(0, 2**32 - 1))
        kmeans = KMeans(n_clusters=n_clusters, random_state=seed)
        self.data['Cluster'] = kmeans.fit_predict(self.data)
        sampled_data = self.data.groupby('Cluster').apply(lambda x: x.sample(n_samples))
        return sampled_data.drop('Cluster', axis=1)

    def pca_sampling(self, n_components, n_samples, seed=None):
        np.random.seed(seed or np.random.randint(0, 2**32 - 1))
        pca = PCA(n_components=n_components)
        pca_data = pca.fit_transform(self.data)
        return pd.DataFrame(pca_data, columns=[f'PC{i+1}' for i in range(n_components)]).sample(n=n_samples)

    def quantile_sampling(self, quantile, n_samples, seed=None):
        np.random.seed(seed or np.random.randint(0, 2**32 - 1))
        high_value_data = self.data[self.data['Value'] >= self.data['Value'].quantile(quantile)]
        return high_value_data.sample(n=n_samples)

    def anomaly_detection_sampling(self, contamination, n_samples, seed=None):
        np.random.seed(seed or np.random.randint(0, 2**32 - 1))
        iforest = IsolationForest(contamination=contamination, random_state=seed)
        anomalies = iforest.fit_predict(self.data)

        return self.data[anomalies == -1].sample(n=n_samples)


if __name__ == '__main__':
    app = QApplication([])
    audit_tool = AuditTool()
    app.exec_()
