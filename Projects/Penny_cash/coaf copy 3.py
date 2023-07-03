import tkinter as tk
from tkinter import filedialog, Text, Label, Entry, Button, StringVar, Toplevel, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from prettytable import PrettyTable
import seaborn as sns
import matplotlib.ticker as ticker

# Constants
KEYWORDS = ['Fraude', 'Erro', 'Estorno', 'Fraud']
EXPECTED_COLUMNS = ['Date', 'Debit', 'Credit', 'Historic']
THRESHOLD = 50000

# Functions
def detect_anomalies(df, threshold):
    df['Value'] = df['Debit'] - df['Credit']
    anomalies = df[df['Value'].abs() > threshold].copy()
    anomalies['Type'] = 'Value Anomalies'
    keyword_anomalies = pd.concat([df[df['Historic'].str.contains(keyword, na=False)] for keyword in KEYWORDS])
    keyword_anomalies = keyword_anomalies.drop_duplicates().copy()
    keyword_anomalies['Type'] = 'Keyword Anomalies'
    all_anomalies = pd.concat([anomalies, keyword_anomalies])
    return all_anomalies

def accounting_format(num):
    if num < 0:
        return f'({abs(num):,.2f})'.replace(",", "X").replace(".", ",").replace("X", ".")
    else:
        return f'{num:,.2f}'.replace(",", "X").replace(".", ",").replace("X", ".")

def format_axes(ax, title):
    ax.set_title(title, fontsize=18, pad=10, loc='left', color='darkslategray')
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=15))  # Set x-axis to display day of the year
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))  # Format x-axis as 'Day/Month/Year'
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: accounting_format(x)))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.tick_params(colors='darkslategray', width=0.5, length=0)  # Remove tick lines but keep labels

def plot_anomalies(df, anomalies):
    fig, axs = plt.subplots(3, 1, figsize=(20, 6 * 3))  # Adjust figure size to fill window
    fig.patch.set_facecolor('white')  # Set figure background to white

    # Cumulative Cashflow Plot
    axs[0].plot(df['Date'], df['Cumulative Cashflow'], color='mediumblue', label='Cumulative Cashflow')
    axs[0].scatter(anomalies['Date'], anomalies['Cumulative Cashflow'], color='red', label='Anomalies')  # Highlight anomalies
    format_axes(axs[0], 'Cumulative Cashflow Over Time')

    # Daily Value Over Time Plot
    axs[1].bar(df['Date'], df['Value'], color='skyblue', label='Daily Value')
    format_axes(axs[1], 'Daily Value Over Time')

    # Cumulative Debit and Credit Over Time Plot
    axs[2].plot(df['Date'], df['Cumulative Debit'], color='mediumblue', label='Cumulative Debit')
    axs[2].plot(df['Date'], df['Cumulative Credit'], color='forestgreen', label='Cumulative Credit')
    format_axes(axs[2], 'Cumulative Debit and Credit Over Time')

    # Improve the padding and layout
    plt.tight_layout(pad=2.0)

    return fig

def start_analysis():
    df = pd.read_excel(file_path.get(), thousands='.', decimal=',')
    
    if not set(EXPECTED_COLUMNS).issubset(df.columns):
        messagebox.showerror("Error", "The selected file does not have the expected column names. Please ensure the file has 'Date', 'Debit', 'Credit', and 'Historic' columns.")
        return
    
    df['Date'] = pd.to_datetime(df['Date'], origin='1899-12-30', unit='D')
    df['Debit'] = df['Debit'].astype(float)
    df['Credit'] = df['Credit'].astype(float)
    df['Value'] = df['Debit'] - df['Credit']
    df['Cumulative Value'] = df['Value'].cumsum()
    df['Month'] = df['Date'].dt.month
    anomalies = detect_anomalies(df, THRESHOLD)
    fig = plot_anomalies(df, anomalies)
    
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()
    
    anomalies.to_excel('anomalies.xlsx')

def select_file():
    file_path.set(filedialog.askopenfilename())

root = tk.Tk()
root.geometry('800x600')
file_path = StringVar()

# Create a frame for the buttons
button_frame = tk.Frame(root)
button_frame.pack(side=tk.TOP, anchor=tk.W, padx=10, pady=10)

select_button = Button(button_frame, text="Select Excel File", command=select_file)
select_button.pack(side=tk.LEFT)

keyword_label = Label(button_frame, text=f"Keywords: {', '.join(KEYWORDS)}")
keyword_label.pack(side=tk.LEFT, padx=10)

threshold_label = Label(button_frame, text="Enter threshold:")
threshold_label.pack(side=tk.LEFT)

threshold_entry = Entry(button_frame)
threshold_entry.pack(side=tk.LEFT)
threshold_entry.insert(0, str(THRESHOLD))  # Set the default threshold to 50000

start_button = Button(button_frame, text="Start Analysis", command=start_analysis)
start_button.pack(side=tk.LEFT, padx=10)

root.mainloop()
