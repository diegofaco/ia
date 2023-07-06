import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from prettytable import PrettyTable
import seaborn as sns
from scipy.signal import savgol_filter
import tkinter as tk
from tkinter import filedialog, Text, Label, Entry, Button, StringVar, Toplevel

sns.set(style="whitegrid", font='Arial', palette='pastel', font_scale=1.2)

KEYWORDS = ['Fraude', 'Erro', 'Estorno', 'Fraud']
EXPECTED_COLUMNS = ['Date', 'Debit', 'Credit', 'Historic']
THRESHOLD = 50000

class AnomalyDetector:
    def __init__(self, file_path):
        self.df = self.load_data(file_path)
        self.process_data()

    def load_data(self, file_path):
        df = pd.read_excel(file_path, thousands='.', decimal=',')
        df['Date'] = pd.to_datetime(df['Date'], origin='1899-12-30', unit='D')
        df['Debit'] = df['Debit'].astype(float)
        df['Credit'] = df['Credit'].astype(float)
        return df

    def process_data(self):
        self.df['Value'] = self.df['Debit'] - self.df['Credit']
        self.df['Cumulative Debit'] = self.df['Debit'].expanding().sum()
        self.df['Cumulative Credit'] = self.df['Credit'].expanding().sum()
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
        self.df = df
        self.anomalies = anomalies

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

        self.plot_cumulative_cashflow(axs[0])
        self.plot_daily_value(axs[1])
        self.plot_debit_credit(axs[2])  # Corrected method name

        plt.tight_layout(pad=5.0)
        return fig

    def plot_cumulative_cashflow(self, ax):
        ax.plot(self.df.index, self.df['Cumulative Cashflow'], color='steelblue', label='Cumulative Cashflow')
        ax.scatter(self.anomalies.index, self.anomalies['Cumulative Cashflow'], color='firebrick', s=100, label='Anomalies', edgecolor='black', zorder=5)
        ax.legend(loc='upper right', fontsize='small')
        ax.grid(False)
        ax.set_ylabel('Cumulative Cashflow', fontsize=14)
        self.format_axes(ax, 'Cumulative Cashflow Over Time')

        # Add annotations for each anomaly and store them in a list
        self.annotations = []
        for i in self.anomalies.index:
            anomaly_date = self.anomalies.loc[i, 'Date'].strftime('%Y-%m-%d')
            anomaly_value = self.accounting_format(self.anomalies.loc[i, 'Value'])
            anomaly_type = self.anomalies.loc[i, 'Type']
            annotation_text = f"{anomaly_type}\nDate: {anomaly_date}\nValue: {anomaly_value}"
            annotation = ax.annotate(annotation_text, (i, self.anomalies.loc[i, 'Cumulative Cashflow']), textcoords="offset points", xytext=(0,10), ha='center', fontsize=8, color='red')
            self.annotations.append(annotation)

    def plot_daily_value(self, ax):
        ax.bar(self.df.index, self.df['Value'], color='skyblue', label='Daily Value')
        ax.scatter(self.anomalies.index, self.anomalies['Value'], color='firebrick', s=100, label='Anomalies', edgecolor='black', zorder=5)
        ax.legend(loc='upper right', fontsize='small')
        ax.grid(False)
        ax.set_ylabel('Daily Value', fontsize=14)
        self.format_axes(ax, 'Daily Value Over Time')

        # Add annotations for each anomaly
        for i in self.anomalies.index:
            anomaly_date = self.anomalies.loc[i, 'Date'].strftime('%Y-%m-%d')
            anomaly_value = self.accounting_format(self.anomalies.loc[i, 'Value'])
            anomaly_type = self.anomalies.loc[i, 'Type']
            annotation_text = f"{anomaly_type}\nDate: {anomaly_date}\nValue: {anomaly_value}"
            annotation = ax.annotate(annotation_text, (i, self.anomalies.loc[i, 'Value']), textcoords="offset points", xytext=(0,10), ha='center', fontsize=8, color='red')
            self.annotations.append(annotation)

    def plot_debit_credit(self, ax):
        ax.plot(self.df.index, self.df['Cumulative Debit'], color='steelblue', linewidth=2, label='Cumulative Debit')
        ax.plot(self.df.index, self.df['Cumulative Credit'], color='seagreen', linewidth=2, label='Cumulative Credit')
        ax.scatter(self.anomalies.index, self.anomalies['Cumulative Debit'], color='firebrick', s=100, label='Debit Anomalies', edgecolor='black', zorder=5)
        ax.scatter(self.anomalies.index, self.anomalies['Cumulative Credit'], color='darkorange', s=100, label='Credit Anomalies', edgecolor='black', zorder=5)
        ax.legend(loc='upper right', fontsize='large')
        ax.grid(False)
        ax.set_ylabel('Cumulative Debit and Credit', fontsize=14)
        self.format_axes(ax, 'Cumulative Debit and Credit Over Time')

        # Add annotations for each anomaly
        for i in self.anomalies.index:
            anomaly_date = self.anomalies.loc[i, 'Date'].strftime('%Y-%m-%d')
            anomaly_value = self.accounting_format(self.anomalies.loc[i, 'Value'])
            anomaly_type = self.anomalies.loc[i, 'Type']
            annotation_text = f"{anomaly_type}\nDate: {anomaly_date}\nValue: {anomaly_value}"
            annotation = ax.annotate(annotation_text, (i, self.anomalies.loc[i, 'Cumulative Debit']), textcoords="offset points", xytext=(0,10), ha='center', fontsize=8, color='red')
            self.annotations.append(annotation)


class Application:
    def __init__(self, root):
        self.root = root
        self.root.geometry('800x600')
        self.file_path = StringVar()
        self.create_widgets()

    def create_widgets(self):
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
        self.visualizer = AnomalyVisualizer(detector.df, anomalies)
        fig = self.visualizer.plot_anomalies()

        # Add a button to toggle the visibility of the anomaly annotations
        toggle_button = Button(self.root, text="Toggle Anomaly Annotations", command=self.toggle_annotations)
        toggle_button.pack()

        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack()

        anomalies.to_excel('anomalies.xlsx')
        
    def toggle_annotations(self):
        # Toggle the visibility of each annotation
        for annotation in self.visualizer.annotations:
            annotation.set_visible(not annotation.get_visible())
        # Redraw the plot
        plt.draw()
        
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

