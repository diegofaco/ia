

import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import ttk

class DataProcessor:

    REQ_COLS = ['Account', 'Account_Description', 'Date', 'Historic', 'ID_Batch', 'Debit', 'Credit']
    INT_COLS = ['Debit', 'Credit']

    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.read_data()

    def read_data(self):
        file_readers = {'.xlsx': pd.read_excel, '.csv': pd.read_csv, '.txt': pd.read_csv}
        return file_readers.get(self.file_path[self.file_path.rfind('.'):], lambda x: None)(self.file_path)

    def analyze(self):
        desc_stats = self.data[self.INT_COLS].describe()
        dist = self.data[self.INT_COLS].hist()
        outliers = self.data[(np.abs(self.data[self.INT_COLS] - self.data[self.INT_COLS].mean()) > (3 * self.data[self.INT_COLS].std()))]
        sns.pairplot(self.data[self.INT_COLS])
        plt.show()
        return desc_stats, dist, outliers

# Create a test dataset
data = pd.DataFrame({
    'Value': np.random.rand(1000),  # 1000 random numbers between 0 and 1
})

# Create a DataProcessor with the test dataset
processor = DataProcessor(data)

# Run the random_selection method with known inputs
output = processor.random_selection(n=10, num_clusters=5, seed=123)

# Check the properties of the output
assert isinstance(output, pd.DataFrame), "Output is not a DataFrame"
assert set(output.columns) == set(data.columns), "Output columns do not match input columns"
assert output.shape[0] == 10, "Output does not contain the correct number of samples"
assert output['Cluster'].nunique() == 5, "Output does not contain samples from all clusters"
