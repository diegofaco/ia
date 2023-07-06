import tkinter as tk
from tkinter import filedialog, Text, Label, Entry, Button, StringVar, Toplevel, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from prettytable import PrettyTable
import seaborn as sns
import matplotlib.ticker as ticker
from scipy.signal import savgol_filter
import re

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

    def accounting_format(self, num):
        if num < 0:
            return f'({abs(num):,.2f})'.replace(",", "X").replace(".", ",").replace("X", ".")
        else:
            return f'{num:,.2f}'.replace(",", "X").replace(".", ",").replace("X", ".")

    def plot_anomalies(self):
        fig, axs = plt.subplots(3, 1, figsize=(20, 30))
        fig.patch.set_facecolor('white')

        # Cumulative Cashflow Plot
        y_smooth = savgol_filter(self.df['Cumulative Cashflow'], 51, 3)
        axs[0].plot(self.df['Date'], y_smooth, color='steelblue', label='Cumulative Cashflow')
        axs[0].scatter(self.anomalies['Date'], self.anomalies['Cumulative Cashflow'], color='firebrick', s=100, label='Anomalies', edgecolor='black', zorder=5)
        axs[0].legend(loc='upper right', fontsize='small')
        axs[0].grid(False)
        axs[0].set_ylabel('Cumulative Cashflow', fontsize=14)
        self.format_axes(axs[0], 'Cumulative Cashflow Over Time')

        # Daily Value Plot
        axs[1].bar(self.df['Date'], self.df['Value'], color='skyblue', label='Daily Value')
        axs[1].scatter(self.anomalies['Date'], self.anomalies['Value'], color='firebrick', s=100, label='Anomalies', edgecolor='black', zorder=5)
        axs[1].legend(loc='upper right', fontsize='small')
        axs[1].grid(False)
        axs[1].set_ylabel('Daily Value', fontsize=14)
        self.format_axes(axs[1], 'Daily Value Over Time')

        # Debit Credit Value Plot
        axs[2].plot(self.df['Date'], self.df['Cumulative Debit'], color='steelblue', linewidth=2, label='Cumulative Debit')
        axs[2].plot(self.df['Date'], self.df['Cumulative Credit'], color='seagreen', linewidth=2, label='Cumulative Credit')
        axs[2].scatter(self.anomalies['Date'], self.anomalies['Cumulative Debit'], color='firebrick', s=100, label='Debit Anomalies', edgecolor='black', zorder=5)
        axs[2].scatter(self.anomalies['Date'], self.anomalies['Cumulative Credit'], color='darkorange', s=100, label='Credit Anomalies', edgecolor='black', zorder=5)
        axs[2].legend(loc='upper right', fontsize='large')
        axs[2].grid(False)
        axs[2].set_ylabel('Cumulative Debit and Credit', fontsize=14)
        self.format_axes(axs[2], 'Cumulative Debit and Credit Over Time')

        plt.tight_layout(pad=5.0)
        return fig

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
