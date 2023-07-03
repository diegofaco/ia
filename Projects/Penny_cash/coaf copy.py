import tkinter as tk
from tkinter import filedialog, Text, Label, Entry, Button, StringVar, Toplevel, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from prettytable import PrettyTable
import seaborn as sns
import matplotlib.ticker as ticker

sns.set(style="whitegrid", font='Arial', palette='pastel', font_scale=1.2)

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

def accounting_format(num):
    if num < 0:
        return f'({abs(num):,.2f})'.replace(",", "X").replace(".", ",").replace("X", ".")
    else:
        return f'{num:,.2f}'.replace(",", "X").replace(".", ",").replace("X", ".")

def format_axes(ax, title, xlabel, ylabel):
    ax.set_title(title, fontsize=18, pad=20)
    ax.set_xlabel(xlabel, fontsize=16, labelpad=20)
    ax.set_ylabel(ylabel, fontsize=16, labelpad=20)
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: accounting_format(x)))
    ax.spines['top'].set_visible(False)  # Remove top border
    ax.spines['right'].set_visible(False)  # Remove right border

def format_axes(ax, title, xlabel, ylabel):
    ax.set_title(title, fontsize=18, pad=20, loc='left')  # Set title location to left
    ax.set_xlabel(xlabel, fontsize=16, labelpad=20)
    ax.set_ylabel(ylabel, fontsize=16, labelpad=20)
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))  # Set x-axis to display integers
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: accounting_format(x)))
    ax.spines['top'].set_visible(False)  # Remove top border
    ax.spines['right'].set_visible(False)  # Remove right border

def format_axes(ax, title):
    ax.set_title(title, fontsize=18, pad=20, loc='left')  # Set title location to left
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))  # Set x-axis to display integers
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: accounting_format(x)))
    ax.spines['top'].set_visible(False)  # Remove top border
    ax.spines['right'].set_visible(False)  # Remove right border

def format_axes(ax, title):
    ax.set_title(title, fontsize=18, pad=10, loc='left')  # Set title location to left and closer to the plot
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))  # Set x-axis to display integers
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: accounting_format(x)))
    ax.spines['top'].set_visible(False)  # Remove top border
    ax.spines['right'].set_visible(False)  # Remove right border

def format_axes(ax, title):
    ax.set_title(title, fontsize=18, pad=10, loc='left')  # Set title location to left and closer to the plot
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))  # Set x-axis to display integers
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: accounting_format(x)))
    ax.spines['top'].set_visible(False)  # Remove top border
    ax.spines['right'].set_visible(False)  # Remove right border

def plot_anomalies(df, anomalies):
    # Sort DataFrame by date and calculate cumulative values
    df = df.sort_values('Date')
    df['Cumulative Debit'] = df['Debit'].cumsum()
    df['Cumulative Credit'] = df['Credit'].cumsum()
    df['Cumulative Cashflow'] = df['Cumulative Debit'] - df['Cumulative Credit']
    df['DayOfYear'] = df['Date'].dt.dayofyear  # Convert date to day of year

    # Calculate cumulative values for anomalies
    anomalies = anomalies.sort_values('Date')
    anomalies['Cumulative Debit'] = anomalies['Debit'].cumsum()
    anomalies['Cumulative Credit'] = anomalies['Credit'].cumsum()
    anomalies['Cumulative Cashflow'] = anomalies['Cumulative Debit'] - anomalies['Cumulative Credit']
    anomalies['DayOfYear'] = anomalies['Date'].dt.dayofyear  # Convert date to day of year

    # Initialize figure and axes
    fig, axs = plt.subplots(4, 1, figsize=(20, 30))  # Adjust figure size to fill window

    # Cumulative Cashflow Plot
    axs[0].plot(df['DayOfYear'], df['Cumulative Cashflow'], color='mediumblue', label='Cumulative Cashflow')
    axs[0].scatter(anomalies['DayOfYear'], anomalies['Cumulative Cashflow'], color='red', label='Anomalies')  # Highlight anomalies
    format_axes(axs[0], 'Cumulative Cashflow Over Time')

    # Debit Credit Value Plot
    axs[1].plot(df['DayOfYear'], df['Cumulative Debit'], color='mediumblue', label='Cumulative Debit')
    axs[1].plot(df['DayOfYear'], df['Cumulative Credit'], color='forestgreen', label='Cumulative Credit')
    axs[1].scatter(anomalies['DayOfYear'], anomalies['Cumulative Debit'], color='red', label='Debit Anomalies')  # Highlight anomalies
    axs[1].scatter(anomalies['DayOfYear'], anomalies['Cumulative Credit'], color='orange', label='Credit Anomalies')  # Highlight anomalies
    format_axes(axs[1], 'Cumulative Debit and Credit Over Time')

    # Box Plot
    sns.boxplot(x=df['DayOfYear'], y=df['Value'], ax=axs[2], palette='cool')
    format_axes(axs[2], 'Boxplot of Daily Values')

    # Daily Value Plot
    axs[3].bar(df['DayOfYear'], df['Value'], color='skyblue', label='Daily Value')  # Change bar width back
    axs[3].scatter(anomalies['DayOfYear'], anomalies['Value'], color='red', label='Anomalies') # Highlight anomalies
    format_axes(axs[3], 'Daily Value Over Time')

    # Improve the padding and layout
    plt.tight_layout(pad=5.0)

    return fig

def plot_histogram(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df['Value'], bins=30, kde=True, ax=ax)
    ax.set_title('Distribution of Values', loc='left')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout(pad=5.0)
    return fig

def plot_scatter(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x='Debit', y='Credit', data=df, ax=ax)
    ax.set_title('Scatter Plot of Debit vs Credit', loc='left')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout(pad=5.0)
    return fig

def plot_heatmap(df):
    df['Month'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day
    pivot = df.pivot_table(values='Value', index='Day', columns='Month')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(pivot, cmap='coolwarm', ax=ax)
    ax.set_title('Heatmap of Value over Month and Day', loc='left')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout(pad=5.0)
    return fig


def start_analysis():
    threshold = 50000  # Set the threshold as standard
    df = pd.read_excel(file_path.get(), thousands='.', decimal=',')
    
    if not set(expected_columns).issubset(df.columns):
        messagebox.showerror("Error", "The selected file does not have the expected column names. Please ensure the file has 'Date', 'Debit', 'Credit', and 'Historic' columns.")
        return
    
    df['Date'] = pd.to_datetime(df['Date'], origin='1899-12-30', unit='D')
    df['Debit'] = df['Debit'].astype(float)
    df['Credit'] = df['Credit'].astype(float)
    df['Value'] = df['Debit'] - df['Credit']
    df['Cumulative Value'] = df['Value'].cumsum()
    df['Month'] = df['Date'].dt.month
    anomalies = detect_anomalies(df, threshold)
    fig = plot_anomalies(df, anomalies)
    
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()
    
    anomalies.to_excel('anomalies.xlsx')


def select_file():
    file_path.set(filedialog.askopenfilename())

def preview_anomalies():
    threshold = 50000  # Set the threshold as standard
    df = pd.read_excel(file_path.get(), thousands='.', decimal=',')
    
    if not set(expected_columns).issubset(df.columns):
        messagebox.showerror("Error", "The selected file does not have the expected column names. Please ensure the file has 'Date', 'Debit', 'Credit', and 'Historic' columns.")
        return
    
    df['Date'] = pd.to_datetime(df['Date'], origin='1899-12-30', unit='D')
    df['Debit'] = df['Debit'].astype(float)
    df['Credit'] = df['Credit'].astype(float)
    df['Value'] = df['Debit'] - df['Credit']
    df['Cumulative Value'] = df['Value'].cumsum()
    df['Month'] = df['Date'].dt.month
    anomalies = detect_anomalies(df, threshold)
    
    anomalies['Value'] = anomalies['Value'].apply(accounting_format)  # Format the 'Value' column
    preview_window = Toplevel(root)
    text_widget = Text(preview_window)
    table = PrettyTable(anomalies.columns.tolist())
    for row in anomalies.itertuples():
        table.add_row(row[1:])  # Exclude the index from the row
    text_widget.insert('end', str(table))
    text_widget.pack()

    
root = tk.Tk()
root.geometry('800x600')
file_path = StringVar()

# Create a frame for the buttons
button_frame = tk.Frame(root)
button_frame.pack(side=tk.TOP, anchor=tk.W, padx=10, pady=10)

select_button = Button(button_frame, text="Select Excel File", command=select_file)
select_button.pack(side=tk.LEFT)

keyword_label = Label(button_frame, text=f"Keywords: {', '.join(keywords)}")
keyword_label.pack(side=tk.LEFT, padx=10)

threshold_label = Label(button_frame, text="Enter threshold:")
threshold_label.pack(side=tk.LEFT)

threshold_entry = Entry(button_frame)
threshold_entry.pack(side=tk.LEFT)
threshold_entry.insert(0, "50000")  # Set the default threshold to 50000

start_button = Button(button_frame, text="Start Analysis", command=start_analysis)
start_button.pack(side=tk.LEFT, padx=10)

preview_button = Button(button_frame, text="Preview Anomalies", command=preview_anomalies)
preview_button.pack(side=tk.LEFT)

root.mainloop()
