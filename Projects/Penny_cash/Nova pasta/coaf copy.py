import tkinter as tk
from tkinter import filedialog, Text, Label, Entry, Button, StringVar, Toplevel, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from prettytable import PrettyTable
import seaborn as sns

# Hardcoded list of keywords
keywords = ['Fraude', 'Erro', 'Estorno', 'Fraud']

# Expected column names
expected_columns = ['Date', 'Debit', 'Credit', 'Historic']

def detect_anomalies(df, threshold):
    df['Value'] = df['Debit'] - df['Credit']
    anomalies = df[df['Value'].abs() > threshold].copy()
    anomalies['Type'] = 'Value Anomalies'
    keyword_anomalies = pd.concat([df[df['Historic'].str.contains(keyword, na=False)] for keyword in keywords])
    keyword_anomalies = keyword_anomalies.drop_duplicates().copy()
    keyword_anomalies['Type'] = 'Keyword Anomalies'
    all_anomalies = pd.concat([anomalies, keyword_anomalies])
    return all_anomalies

def plot_anomalies(df, anomalies):
    df = df.sort_values('Date')
    df['Cumulative Value'] = df['Value'].cumsum()
    fig, axs = plt.subplots(3, 1, figsize=(10, 18))
    axs[0].plot(df['Date'], df['Cumulative Value'], color='blue', label='Cumulative Value')
    colors = {'Value Anomalies': 'yellow', 'Keyword Anomalies': 'green'}
    markers = {'Value Anomalies': '*', 'Keyword Anomalies': 'o'}
    for anomaly_type in anomalies['Type'].unique():
        anomaly_df = anomalies[anomalies['Type'] == anomaly_type]
        anomaly_df = anomaly_df.sort_values('Date')
        anomaly_df['Cumulative Value'] = anomaly_df['Value'].cumsum()
        axs[0].scatter(anomaly_df['Date'], anomaly_df['Cumulative Value'], color=colors[anomaly_type], marker=markers[anomaly_type], label=anomaly_type)
    axs[0].set_xlabel('Date')
    axs[0].set_ylabel('Cumulative Value')
    axs[0].legend()
    axs[0].grid(True)
    axs[0].xaxis.set_major_locator(mdates.MonthLocator())
    axs[0].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    axs[1].bar(df['Date'], df['Value'], color='blue', label='Daily Value')
    for anomaly_type in anomalies['Type'].unique():
        anomaly_df = anomalies[anomalies['Type'] == anomaly_type]
        axs[1].bar(anomaly_df['Date'], anomaly_df['Value'], color=colors[anomaly_type], label=anomaly_type)
    axs[1].set_xlabel('Date')
    axs[1].set_ylabel('Daily Value')
    axs[1].legend()
    axs[1].grid(True)
    axs[1].xaxis.set_major_locator(mdates.MonthLocator())
    axs[1].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    sns.histplot(df['Value'], ax=axs[2], color='blue', label='Value Distribution')
    for anomaly_type in anomalies['Type'].unique():
        anomaly_df = anomalies[anomalies['Type'] == anomaly_type]
        sns.histplot(anomaly_df['Value'], ax=axs[2], color=colors[anomaly_type], label=anomaly_type)
    axs[2].set_xlabel('Value')
    axs[2].set_ylabel('Count')
    axs[2].legend()
    axs[2].grid(True)
    return fig

def start_analysis():
    if not threshold_entry.get():
        print("Please enter a threshold.")
        return
    threshold = float(threshold_entry.get())
    df = pd.read_excel(file_path.get(), thousands='.', decimal=',')
    if not set(expected_columns).issubset(df.columns):
        messagebox.showerror("Error", "The selected file does not have the expected column names. Please ensure the file has 'Date', 'Debit', 'Credit', and 'Historic' columns.")
        return
    df['Date'] = pd.to_datetime(df['Date'], origin='1899-12-30', unit='D')
    df['Debit'] = df['Debit'].astype(float)
    df['Credit'] = df['Credit'].astype(float)
    anomalies = detect_anomalies(df, threshold)
    fig = plot_anomalies(df, anomalies)
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()
    anomalies.to_excel('anomalies.xlsx')

def select_file():
    file_path.set(filedialog.askopenfilename())

def preview_data():
    df = pd.read_excel(file_path.get(), thousands='.', decimal=',')
    preview_window = Toplevel(root)
    text_widget = Text(preview_window)
    table = PrettyTable(df.columns.tolist())
    for row in df.itertuples():
        table.add_row(row)
    text_widget.insert('end', str(table))
    text_widget.pack()

root = tk.Tk()
root.geometry('800x600')
file_path = StringVar()
select_button = Button(root, text="Select Excel File", command=select_file)
select_button.pack()
keyword_label = Label(root, text=f"Keywords: {', '.join(keywords)}")
keyword_label.pack()
threshold_label = Label(root, text="Enter threshold:")
threshold_label.pack()
threshold_entry = Entry(root)
threshold_entry.pack()
start_button = Button(root, text="Start Analysis", command=start_analysis)
start_button.pack()
preview_button = Button(root, text="Preview Data", command=preview_data)
preview_button.pack()
root.mainloop()
