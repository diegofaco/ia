import tkinter as tk
from tkinter import filedialog, Text, Label, Entry, Button, StringVar, Toplevel, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from prettytable import PrettyTable
import seaborn as sns
import matplotlib.ticker as ticker

# test
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import make_interp_spline, BSpline
import numpy as np
# end test

sns.set(style="whitegrid", font='Arial', palette='pastel', font_scale=1.2)

KEYWORDS = ['Fraude', 'Erro', 'Estorno', 'Fraud']
EXPECTED_COLUMNS = ['Date', 'Debit', 'Credit', 'Historic']
THRESHOLD = 50000

class AnomalyDetector:
    def __init__(self, file_path):
        self.df = pd.read_excel(file_path, thousands='.', decimal=',')
        self.df['Date'] = pd.to_datetime(self.df['Date'], origin='1899-12-30', unit='D')
        self.df['Debit'] = self.df['Debit'].astype(float)
        self.df['Credit'] = self.df['Credit'].astype(float)
        self.df['Value'] = self.df['Debit'] - self.df['Credit']
        self.df['Cumulative Debit'] = self.df['Debit'].cumsum()
        self.df['Cumulative Credit'] = self.df['Credit'].cumsum()
        self.df['Cumulative Cashflow'] = self.df['Cumulative Debit'] - self.df['Cumulative Credit']
        self.df['Month'] = self.df['Date'].dt.month

    def detect_anomalies(self):
        anomalies = self.df[self.df['Value'].abs() > THRESHOLD].copy()
        anomalies['Type'] = 'Value Anomalies'
        keyword_anomalies = pd.concat([self.df[self.df['Historic'].str.contains(keyword, na=False)] for keyword in KEYWORDS])
        keyword_anomalies = keyword_anomalies.drop_duplicates().copy()
        keyword_anomalies['Type'] = 'Keyword Anomalies'
        all_anomalies = pd.concat([anomalies, keyword_anomalies])
        return all_anomalies

class AnomalyVisualizer:
    def __init__(self, df, anomalies):
        self.df = df.sort_values('Date')
        self.anomalies = anomalies.sort_values('Date')

    def format_axes(self, ax, title):
        ax.set_title(title, fontsize=18, pad=10, loc='left', color='darkslategray')
        ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: self.accounting_format(x)))
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(colors='darkslategray', width=0.5, length=0)
        ax.grid(False)

    def plot_anomalies(self):
        fig, axs = plt.subplots(3, 1, figsize=(20, 30))
        fig.patch.set_facecolor('white')

        # Cumulative Cashflow Plot
        xnew = np.linspace(0, len(self.df['Date']) - 1, 500)
        spl = make_interp_spline(range(len(self.df['Date'])), self.df['Cumulative Cashflow'], k=3)
        cashflow_smooth = spl(xnew)
        axs[0].plot(self.df['Date'], cashflow_smooth, color='steelblue', label='Cumulative Cashflow')
        axs[0].scatter(self.anomalies['Date'], self.anomalies['Cumulative Cashflow'], color='firebrick', label='Anomalies')
        axs[0].legend(loc='upper right')
        self.format_axes(axs[0], 'Cumulative Cashflow Over Time')

        # Daily Value Plot
        spl = make_interp_spline(range(len(self.df['Date'])), self.df['Value'], k=3)
        value_smooth = spl(xnew)
        axs[1].plot(self.df['Date'], value_smooth, color='skyblue', label='Daily Value')
        axs[1].scatter(self.anomalies['Date'], self.anomalies['Value'], color='firebrick', label='Anomalies')
        axs[1].legend(loc='upper right')
        self.format_axes(axs[1], 'Daily Value Over Time')

        # Debit Credit Value Plot
        spl_debit = make_interp_spline(range(len(self.df['Date'])), self.df['Cumulative Debit'], k=3)
        spl_credit = make_interp_spline(range(len(self.df['Date'])), self.df['Cumulative Credit'], k=3)
        debit_smooth = spl_debit(xnew)
        credit_smooth = spl_credit(xnew)
        axs[2].plot(self.df['Date'], debit_smooth, color='steelblue', label='Cumulative Debit')
        axs[2].plot(self.df['Date'], credit_smooth, color='seagreen', label='Cumulative Credit')
        axs[2].scatter(self.anomalies['Date'], self.anomalies['Cumulative Debit'], color='firebrick', label='Debit Anomalies')
        axs[2].scatter(self.anomalies['Date'], self.anomalies['Cumulative Credit'], color='darkorange', label='Credit Anomalies')
        axs[2].legend(loc='upper right')
        self.format_axes(axs[2], 'Cumulative Debit and Credit Over Time')

        plt.tight_layout(pad=5.0)
        return fig
    
# text
class AdditionalVisualizer:
    def __init__(self, df):
        self.df = df

    def plot_transaction_volume(self):
        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111, projection='3d')
        x = self.df['Date'].dt.date.unique()
        y1 = self.df.groupby(self.df['Date'].dt.date)['Value'].count()
        y2 = self.df.groupby(self.df['Date'].dt.date)['Value'].sum()
        ax.bar(x, y1, zs=0, zdir='y', color='skyblue', alpha=0.8)
        ax.plot(x, y2, zs=0, zdir='y', color='steelblue')
        ax.set_ylabel('Transaction Volume')
        ax.set_zlabel('Transaction Amount')
        return fig
# end text

class Application:
    def __init__(self, root):
        self.root = root
        self.root.geometry('800x600')
        self.file_path = StringVar()

        button_frame = tk.Frame(self.root)
        button_frame.pack(side=tk.TOP, anchor=tk.W, padx=10, pady=10)

        select_button = Button(button_frame, text="Select Excel File", command=self.select_file)
        select_button.pack(side=tk.LEFT)

        keyword_label = Label(button_frame, text=f"Keywords: {', '.join(KEYWORDS)}")
        keyword_label.pack(side=tk.LEFT, padx=10)

        threshold_label = Label(button_frame, text="Enter threshold:")
        threshold_label.pack(side=tk.LEFT)

        self.threshold_entry = Entry(button_frame)
        self.threshold_entry.pack(side=tk.LEFT)
        self.threshold_entry.insert(0, str(THRESHOLD))

        start_button = Button(button_frame, text="Start Analysis", command=self.start_analysis)
        start_button.pack(side=tk.LEFT, padx=10)

        preview_button = Button(button_frame, text="Preview Anomalies", command=self.preview_anomalies)
        preview_button.pack(side=tk.LEFT)

    def select_file(self):
        self.file_path.set(filedialog.askopenfilename())

    def start_analysis(self):
        detector = AnomalyDetector(self.file_path.get())
        anomalies = detector.detect_anomalies()
        visualizer = AnomalyVisualizer(detector.df, anomalies)
        fig = visualizer.plot_anomalies()

        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack()

        anomalies.to_excel('anomalies.xlsx')

        additional_visualizer = AdditionalVisualizer(detector.df)
        new_window = Toplevel(self.root)
        new_window.geometry('800x600')

        fig_transaction_volume = additional_visualizer.plot_transaction_volume()
        canvas_transaction_volume = FigureCanvasTkAgg(fig_transaction_volume, master=new_window)
        canvas_transaction_volume.draw()
        canvas_transaction_volume.get_tk_widget().pack()

    def preview_anomalies(self):
        detector = AnomalyDetector(self.file_path.get())
        anomalies = detector.detect_anomalies()
        anomalies['Value'] = anomalies['Value'].apply(AnomalyVisualizer.accounting_format)
        preview_window = Toplevel(self.root)
        text_widget = Text(preview_window)
        table = PrettyTable(anomalies.columns.tolist())
        for row in anomalies.itertuples():
            table.add_row(row[1:])
        text_widget.insert('end', str(table))
        text_widget.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
