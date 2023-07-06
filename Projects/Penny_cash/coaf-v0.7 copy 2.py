# TESTE_COAF-v0.7

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog, StringVar, Button, Tk, LEFT, TOP
from scipy.signal import savgol_filter
import threading
import unicodedata
from tkinter import Label
import os
import xlsxwriter
import numpy as np
from tkinter import Checkbutton, BooleanVar

KEYWORDS = ['Fraude', 'Erro', 'Estorno', 'Fraud']
THRESHOLD = 50000

def format_number(num):
    return f"{num:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".").replace("-", "(") + ")" if num < 0 else f"{num:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

class AnomalyDetector:
    def __init__(self, file_path):
        df = pd.read_excel(file_path, thousands='.', decimal=',')
        
        column_mapping = {
            'Debit': ['Debit', 'Debito', 'Débito'],
            'Credit': ['Credit', 'Credito', 'Crédito'],
            'Historic': ['Historic', 'Histórico', 'Historico'],
            'Account': ['Account', 'Conta', 'Conta contábil', 'Conta contabil'],
            'Date': ['Date', 'Data']
        }

        df.columns = df.columns.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.lower()

        for standard_name, possible_names in column_mapping.items():
            for name in possible_names:
                normalized_name = unicodedata.normalize('NFKD', name).encode('ascii', errors='ignore').decode('utf-8').lower()
                df.rename(columns={normalized_name: standard_name}, inplace=True)
                
        if df['Date'].dtype != 'datetime64[ns]':
            df['Date'] = pd.to_datetime(df['Date'], origin='1899-12-30', unit='D')
        df[['Debit', 'Credit']] = df[['Debit', 'Credit']].astype(float)
        df['Value'] = df['Debit'] - df['Credit']
        df[['Cumulative Debit', 'Cumulative Credit']] = df[['Debit', 'Credit']].cumsum()
        df['Cumulative Cashflow'] = df['Cumulative Debit'] - df['Cumulative Credit']
        self.df = df
        self.anomalies = self.detect_anomalies()

    def detect_anomalies(self):
        anomalies = self.df[self.df['Value'].abs() > THRESHOLD].copy()
        anomalies['Type'] = 'Value Anomalies'
        keyword_anomalies = pd.concat([self.df[self.df['Historic'].str.contains(keyword, na=False)] for keyword in KEYWORDS]).drop_duplicates().copy()
        keyword_anomalies['Type'] = 'Keyword Anomalies'
        return pd.concat([anomalies, keyword_anomalies])

class AnomalyVisualizer:
    def __init__(self, detector):
        self.detector = detector
        self.annotations = []

    def get_monthly_summary(self):
        summary = self.df.resample('M', on='Date').agg({
            'Debit': ['count', 'sum'],
            'Credit': ['count', 'sum']
        })
        summary.columns = ['_'.join(col).strip() for col in summary.columns.values]
        return summary
    
    def plot_anomalies(self):
        fig, axs = plt.subplots(3, 1, figsize=(20, 30))
        fig.patch.set_facecolor('white')
        self.plot_cumulative_cashflow(axs[0])
        self.plot_daily_value(axs[1])
        self.plot_debit_credit(axs[2])
        plt.tight_layout(pad=5.0)
        plt.savefig('anomalies.png')
        return fig

    def plot_cumulative_cashflow(self, ax):
        self._plot(ax, 'Cumulative Cashflow', 'Cumulative Cashflow Over Time')

    def plot_daily_value(self, ax):
        ax.bar(self.detector.df.index, self.detector.df['Value'], color='skyblue', label='Daily Value')
        self._annotate(ax, 'Value')
        self._format_axes(ax, 'Daily Value Over Time')

    def plot_debit_credit(self, ax):
        ax.plot(self.detector.df.index, savgol_filter(self.detector.df['Cumulative Debit'], 51, 3), color='darkred', linewidth=2, label='Cumulative Debit')
        ax.plot(self.detector.df.index, savgol_filter(self.detector.df['Cumulative Credit'], 51, 3), color='darkgreen', linewidth=2, label='Cumulative Credit')
        self._format_axes(ax, 'Cumulative Debit and Credit Over Time')

    def _plot(self, ax, y, title):
        ax.plot(self.detector.df.index, savgol_filter(self.detector.df[y], 51, 3), color='steelblue', label=y)
        self._annotate(ax, y)
        self._format_axes(ax, title)

    def _annotate(self, ax, y):
        if y != 'Cumulative Cashflow':
            for _, row in self.detector.anomalies.iterrows():
                ax.plot(row.name, row[y], 'ro')
                annotation = ax.annotate(f"{row['Type']}\n{row['Date'].strftime('%Y-%m-%d')}\n{format_number(row[y])}", (row.name, row[y]), textcoords="offset points", xytext=(0,10), ha='center', fontsize=8, color='red')
                self.annotations.append(annotation)
                annotation.set_visible(False)

    def _format_axes(self, ax, title):
        ax.set_title(title, fontsize=18, pad=10, loc='left', color='darkslategrey')
        ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format_number(x)))
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(colors='darkslategrey', width=0.5, length=0)
        ax.legend(loc='upper right', fontsize='small')
        ax.grid(False)

class Application:
    def __init__(self, root):
        self.root = root
        self.root.geometry('800x600')
        self.file_path = StringVar()
        self._create_widgets()

        config_info = f'Limite: {THRESHOLD}\nPalavras-chave: {", ".join(KEYWORDS)}'
        Label(self.root, text=config_info, justify=LEFT).pack(side=TOP, anchor='nw')
        
        self.view_excel_button = Button(self.root, text="Ver Anomalias no Excel", command=self._view_anomalies_in_excel, state='disabled')
        self.view_excel_button.pack(side=TOP, anchor='nw')

    def _create_widgets(self):
        Button(self.root, text="Selecionar Arquivo Excel", command=self._select_file).pack(side=TOP, anchor='nw')
        self.start_analysis_button = Button(self.root, text="Iniciar Análise", command=self._start_analysis, state='disabled')
        self.start_analysis_button.pack(side=TOP, anchor='nw')
        self.clear_analysis_button = Button(self.root, text="Limpar Análise", command=self._clear_analysis, state='disabled')
        self.clear_analysis_button.pack(side=TOP, anchor='nw')
        self.toggle_annotations_button = Button(self.root, text="Alternar Anotações", command=self._toggle_annotations, state='disabled')
        self.toggle_annotations_button.pack(side=TOP, anchor='nw')

    def _select_file(self):
        self.file_path.set(filedialog.askopenfilename())
        self.start_analysis_button['state'] = 'normal'

    def _start_analysis(self):
        if hasattr(self, 'canvas'):
            self.canvas.get_tk_widget().pack_forget()
        self.start_analysis_button['state'] = 'disabled'
        self.clear_analysis_button['state'] = 'normal'
        self._run_analysis()

    def _run_analysis(self):
        self.detector = AnomalyDetector(self.file_path.get())
        self.visualizer = AnomalyVisualizer(self.detector)
        fig, axs = plt.subplots(3, 1, figsize=(20, 13))  # reduce the height here
        fig.patch.set_facecolor('white')
        self.visualizer.plot_cumulative_cashflow(axs[0])
        self.visualizer.plot_daily_value(axs[1])
        self.visualizer.plot_debit_credit(axs[2])
        plt.tight_layout(pad=5.0)
        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        self.root.bind('<Configure>', self._on_resize)
        self.toggle_annotations_button['state'] = 'normal'
        self.view_excel_button['state'] = 'normal'


    def _view_anomalies_in_excel(self):
        self.root.after(0, self._save_plots_and_create_excel)

    def _save_plots_and_create_excel(self):
        fig = self.visualizer.plot_anomalies()
        fig.set_size_inches(10, 10)
        fig.savefig('anomalies.png')

        workbook = xlsxwriter.Workbook('anomalies.xlsx')

        writer = pd.ExcelWriter('anomalies.xlsx', engine='xlsxwriter')
        self.detector.df.to_excel(writer, sheet_name='Data', index_label='Line Count')
        self.detector.anomalies.to_excel(writer, sheet_name='Anomalies', index_label='Line Count')

        
        workbook = writer.book
        data_worksheet = writer.sheets['Data']
        data_worksheet.hide_gridlines(1)
        data_worksheet.autofilter(0, 0, len(self.detector.df), len(self.detector.df.columns))
        header_format = workbook.add_format({'bold': True, 'bg_color': '#D7E4BC', 'border': 1})
        cell_format = workbook.add_format({'border': 1})
        number_format = workbook.add_format({'num_format': '#,##0.00_ ;[Red](#,##0.00)', 'border': 1})
        for i, column in enumerate(['Line Count'] + list(self.detector.df.columns)):
            data_worksheet.write(0, i, column, header_format)
            for j, value in enumerate(self.detector.df[column] if i > 0 else self.detector.df.index):
                if isinstance(value, float):
                    if not pd.isnull(value) and np.isfinite(value):  # Check if the value is not NaN or INF
                        data_worksheet.write(j + 1, i, value, number_format)
                    else:
                        data_worksheet.write(j + 1, i, '')
                else:
                    data_worksheet.write(j + 1, i, value, cell_format)

        
        anomalies_worksheet = writer.sheets['Anomalies']
        anomalies_worksheet.hide_gridlines(1)
        anomalies_worksheet.autofilter(0, 0, len(self.detector.anomalies), len(self.detector.anomalies.columns))
        for i, column in enumerate(['Line Count'] + list(self.detector.anomalies.columns)):
            anomalies_worksheet.write(0, i, column, header_format)
            for j, value in enumerate(self.detector.anomalies[column] if i > 0 else self.detector.anomalies.index):
                if isinstance(value, float):
                    if not pd.isnull(value) and np.isfinite(value):  # Check if the value is not NaN or INF
                        anomalies_worksheet.write(j + 1, i, value, number_format)
                    else:
                        anomalies_worksheet.write(j + 1, i, '')
                else:
                    anomalies_worksheet.write(j + 1, i, value, cell_format)
        graphs_worksheet = workbook.add_worksheet('Graphs')
        graphs_worksheet.hide_gridlines(1)
        graphs_worksheet.insert_image('A1', 'anomalies.png')

        anomalies_worksheet.activate()

        writer.close()

        os.startfile('anomalies.xlsx')

    def _on_resize(self, event):
        # get the size of the window
        width, height = event.width, event.height
        # adjust the size of the figure
        self.visualizer.fig.set_size_inches(width / self.visualizer.fig.dpi, height / self.visualizer.fig.dpi)
        # redraw the canvas
        self.canvas.draw()
        
    def _update_gui(self, fig):
        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()
        self.toggle_annotations_button['state'] = 'normal'
        
    def _clear_analysis(self):
        if hasattr(self, 'canvas'):
            self.canvas.get_tk_widget().pack_forget()
            del self.canvas
            del self.detector
            del self.visualizer
        self.clear_analysis_button['state'] = 'disabled'
        self.toggle_annotations_button['state'] = 'disabled'
        self.start_analysis_button['state'] = 'normal'

    def _toggle_annotations(self):
        for annotation in self.visualizer.annotations:
            annotation.set_visible(not annotation.get_visible())
        self.canvas.draw()

if __name__ == "__main__":
    root = Tk()
    app = Application(root)
    root.mainloop()
