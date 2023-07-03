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

def format_axes(ax, title):
    ax.set_title(title, fontsize=18, pad=10, loc='left', color='darkslategray')  # Set title location to left and closer to the plot
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))  # Set x-axis to display integers
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: accounting_format(x)))
    ax.spines['top'].set_visible(False)  # Remove top border
    ax.spines['right'].set_visible(False)  # Remove right border
    ax.spines['left'].set_visible(False)  # Remove left border
    ax.spines['bottom'].set_visible(False)  # Remove bottom border
    ax.tick_params(colors='darkslategray', width=0.5)  # Set tick color to darkslategray and reduce linewidth
    ax.get_xaxis().set_ticks([])  # Remove x-axis tick marks
    ax.get_yaxis().set_ticks([])  # Remove y-axis tick marks

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

def format_axes(ax, title):
    ax.set_title(title, fontsize=18, pad=10, loc='left', color='darkslategray')  # Set title location to left and closer to the plot
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))  # Set x-axis to display integers
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: accounting_format(x)))
    ax.spines['top'].set_visible(False)  # Remove top border
    ax.spines['right'].set_visible(False)  # Remove right border
    ax.spines['left'].set_linewidth(0.5)  # Reduce left border linewidth
    ax.spines['bottom'].set_linewidth(0.5)  # Reduce bottom border linewidth
    ax.tick_params(colors='darkslategray', width=0.5)  # Set tick color to darkslategray and reduce linewidth

def format_axes(ax, title):
    ax.set_title(title, fontsize=18, pad=10, loc='left', color='darkslategray')  # Set title location to left and closer to the plot
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))  # Set x-axis to display integers
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: accounting_format(x)))
    ax.spines['top'].set_visible(False)  # Remove top border
    ax.spines['right'].set_visible(False)  # Remove right border
    ax.spines['left'].set_linewidth(0.5)  # Reduce left border linewidth
    ax.spines['bottom'].set_linewidth(0.5)  # Reduce bottom border linewidth
    ax.tick_params(colors='darkslategray', width=0.5)  # Set tick color to darkslategray and reduce linewidth

def plot_anomalies(df, anomalies):
    # Sort DataFrame by date and calculate cumulative values
    df = df.sort_values('Date')
    df['Cumulative Debit'] = df['Debit'].cumsum()
    df['Cumulative Credit'] = df['Credit'].cumsum()
    df['Cumulative Cashflow'] = df['Cumulative Debit'] - df['Cumulative Credit']

    # Calculate cumulative values for anomalies
    anomalies = anomalies.sort_values('Date')
    anomalies['Cumulative Debit'] = anomalies['Debit'].cumsum()
    anomalies['Cumulative Credit'] = anomalies['Credit'].cumsum()
    anomalies['Cumulative Cashflow'] = anomalies['Cumulative Debit'] - anomalies['Cumulative Credit']

    # Convert date to 'dd/mm/yyyy' format
    df['Date'] = df['Date'].dt.strftime('%d/%m/%Y')
    anomalies['Date'] = anomalies['Date'].dt.strftime('%d/%m/%Y')

    # Initialize figure and axes
    num_subplots = 3
    fig, axs = plt.subplots(num_subplots, 1, figsize=(20, 6 * num_subplots))  # Adjust figure size to fill window
    fig.patch.set_facecolor('white')  # Set figure background to white

    # Cumulative Cashflow Plot
    axs[0].plot(df['Date'], df['Cumulative Cashflow'], color='steelblue', label='Cumulative Cashflow')
    axs[0].scatter(anomalies['Date'], anomalies['Cumulative Cashflow'], color='firebrick', label='Anomalies')  # Highlight anomalies
    axs[0].legend(loc='upper right')  # Move legend to upper right corner
    format_axes(axs[0], 'Cumulative Cashflow Over Time')

    # Daily Value Plot
    axs[1].bar(df['Date'], df['Value'], color='skyblue', label='Daily★ Value')  # Change bar width back
    axs[1].scatter(anomalies['Date'], anomalies['Value'], color='firebrick', label='Anomalies')  # Highlight anomalies
    axs[1].legend(loc='upper right')  # Move legend to upper right corner
    format_axes(axs[1], 'Daily Value Over Time')

    # Debit Credit Value Plot
    axs[2].plot(df['Date'], df['Cumulative Debit'], color='steelblue', label='Cumulative Debit')
    axs[2].plot(df['Date'], df['Cumulative Credit'], color='seagreen', label='Cumulative Credit')
    axs[2].scatter(anomalies['Date'], anomalies['Cumulative Debit'], color='firebrick', label='Debit Anomalies')  # Highlight anomalies
    axs[2].scatter(anomalies['Date'], anomalies['Cumulative Credit'], color='darkorange', label='Credit Anomalies')  # Highlight anomalies
    axs[2].legend(loc='upper right')  # Move legend to upper right corner
    format_axes(axs[2], 'Cumulative Debit and Credit Over Time')

    # Improve the padding and layout
    plt.tight_layout(pad=2.0 * num_subplots)  # Adjust padding based on the number of subplots

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

def plot_histogram(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(df['Value'], bins=30, color='skyblue', edgecolor='white')
    format_axes(ax, 'Histogram of Daily Values')
    return fig

def plot_scatter(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(df['Date'], df['Value'], alpha=0.5)
    format_axes(ax, 'Scatter Plot of Daily Values')
    return fig

def show_additional_plots(df):
    # Create a new window
    new_window = Toplevel(root)
    new_window.geometry('800x600')

    # Create scatter plot
    fig_scatter = plot_scatter(df)
    canvas_scatter = FigureCanvasTkAgg(fig_scatter, master=new_window)
    canvas_scatter.draw()
    canvas_scatter.get_tk_widget().pack()

    # Create histogram
    fig_histogram = plot_histogram(df)
    canvas_histogram = FigureCanvasTkAgg(fig_histogram, master=new_window)
    canvas_histogram.draw()
    canvas_histogram.get_tk_widget().pack()

    # Create heatmap
    fig_heatmap = plot_heatmap(df)
    canvas_heatmap = FigureCanvasTkAgg(fig_heatmap, master=new_window)
    canvas_heatmap.draw()
    canvas_heatmap.get_tk_widget().pack()


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
    show_additional_plots(df)  # Show additional plots
    
    anomalies.to_excel('anomalies.xlsx')
    show_additional_plots(df)

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
