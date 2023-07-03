import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import ttk

class AuditTool:
    """Class for the audit tool."""

    REQ_COLS = ['Account', 'Account_Description', 'Date', 'Historic', 'ID_Batch', 'Debit', 'Credit']
    INT_COLS = ['Debit', 'Credit']

    def __init__(self, master=None):
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        # File Input
        self.file_input_frame = ttk.LabelFrame(self.master, text="File Input")
        self.file_input_frame.pack(fill="both", expand=True)
        self.select_file_button = ttk.Button(self.file_input_frame, text="Select your data file: [Browse...]")
        self.select_file_button.pack(side="left")

        # Sampling Configuration
        self.sampling_config_frame = ttk.LabelFrame(self.master, text="Sampling Configuration")
        self.sampling_config_frame.pack(fill="both", expand=True)
        self.sampling_method_dropdown = ttk.Combobox(self.sampling_config_frame, values=["Method 1", "Method 2", "Method 3"])
        self.sampling_method_dropdown.pack(side="left")

        # Audit Measures
        self.audit_measures_frame = ttk.LabelFrame(self.master, text="Audit Measures")
        self.audit_measures_frame.pack(fill="both", expand=True)
        self.overall_materiality_entry = ttk.Entry(self.audit_measures_frame)
        self.overall_materiality_entry.pack(side="left")

        # Statistical Data/Graphs
        self.stats_data_frame = ttk.LabelFrame(self.master, text="Statistical Data/Graphs")
        self.stats_data_frame.pack(fill="both", expand=True)

        # Run Sampling
        self.run_sampling_frame = ttk.LabelFrame(self.master, text="Run Sampling")
        self.run_sampling_frame.pack(fill="both", expand=True)
        self.start_button = ttk.Button(self.run_sampling_frame, text="Start")
        self.start_button.pack(side="left")

        # Results
        self.results_frame = ttk.LabelFrame(self.master, text="Results")
        self.results_frame.pack(fill="both", expand=True)

    def select_file(self):
        self.file_path = filedialog.askopenfilename()

    def preview_data(self):
        print(self.read_data().head())

    def view_stats(self):
        data = self.read_data()
        desc_stats, dist, outliers = self.analyze(data)
        print(desc_stats, dist, outliers)

    def read_data(self):
        """Read data from a file."""
        file_readers = {'.xlsx': pd.read_excel, '.csv': pd.read_csv, '.txt': pd.read_csv}
        return file_readers.get(self.file_path[self.file_path.rfind('.'):], lambda x: None)(self.file_path)

    def analyze(self, data):
        """Perform statistical analysis on the data."""
        desc_stats = data[AuditTool.INT_COLS].describe()
        dist = data[AuditTool.INT_COLS].hist()
        outliers = data[(np.abs(data[AuditTool.INT_COLS] - data[AuditTool.INT_COLS].mean()) > (3 * data[AuditTool.INT_COLS].std()))]
        sns.pairplot(data[AuditTool.INT_COLS])
        plt.show()
        return desc_stats, dist, outliers

    def random_selection(self, data, n):
        return data.sample(n=n, random_state=np.random.RandomState())

    def haphazard_selection(self, data, n):
        return data.sample(n=n, random_state=np.random.RandomState()).reset_index(drop=True)

    def interval_selection(self, data, n):
        return data.iloc[range(0, len(data), len(data) // n)]

    def monetary_unit_sampling(self, data, col, val):
        return data[data[col].cumsum() <= val]

    def stratified_sampling(self, data, col, n):
        return data.groupby(col).apply(lambda x: x.sample(n=n))

    def judgemental_sampling(self, data, crit):
        return data.query(crit)

root = tk.Tk()
app = AuditTool(master=root)
root.mainloop()
