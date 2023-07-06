import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog, StringVar, Button, Tk
from scipy.signal import savgol_filter

KEYWORDS = ['Fraude', 'Erro', 'Estorno', 'Fraud']
THRESHOLD = 50000

class AnomalyDetector:
    def __init__(self, file_path):
        df = pd.read_excel(file_path, thousands='.', decimal=',')
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
        self.xaxis_mode = 'operations'
        self.annotations = []

    def plot_anomalies(self):
        fig, axs = plt.subplots(3, 1, figsize=(20, 30))
        fig.patch.set_facecolor('white')
        self.plot_cumulative_cashflow(axs[0])
        self.plot_daily_value(axs[1])
        self.plot_debit_credit(axs[2])
        plt.tight_layout(pad=5.0)
        return fig

    def plot_cumulative_cashflow(self, ax):
        self._plot(ax, 'Cumulative Cashflow', 'Cumulative Cashflow Over Time')

    def plot_daily_value(self, ax):
        ax.bar(self._x(), self.detector.df['Value'], color='skyblue', label='Daily Value')
        self._annotate(ax, 'Value')
        self._format_axes(ax, 'Daily Value Over Time')

    def plot_debit_credit(self, ax):
        ax.plot(self._x(), self.detector.df['Cumulative Debit'], color='steelblue', linewidth=2, label='Cumulative Debit')
        ax.plot(self._x(), self.detector.df['Cumulative Credit'], color='seagreen', linewidth=2, label='Cumulative Credit')
        self._annotate(ax, 'Cumulative Debit')
        self._annotate(ax, 'Cumulative Credit')
        self._format_axes(ax, 'Cumulative Debit and Credit Over Time')

    def _x(self):
        return self.detector.df['Date'] if self.xaxis_mode == 'dates' else self.detector.df.index

    def _plot(self, ax, y, title):
        ax.plot(self._x(), savgol_filter(self.detector.df[y], 51, 3), color='steelblue', label=y)
        self._annotate(ax, y)
        self._format_axes(ax, title)

    def _annotate(self, ax, y):
        for _, row in self.detector.anomalies.iterrows():
            annotation = ax.annotate(f"{row['Type']}\n{row['Date'].strftime('%Y-%m-%d')}\n{row[y]:,.2f}", (row.name, row[y]), textcoords="offset points", xytext=(0,10), ha='center', fontsize=8, color='darkslategrey')
            self.annotations.append(annotation)
            annotation.set_visible(False)

    def _format_axes(self, ax, title):
        ax.set_title(title, fontsize=18, pad=10, loc='left', color='darkslategrey')
        ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")))
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

    def _create_widgets(self):
        Button(self.root, text="Select Excel File", command=self._select_file).pack(side='left')
        Button(self.root, text="Start Analysis", command=self._start_analysis).pack(side='left')
        self.toggle_button = Button(self.root, text="Toggle X-Axis", command=self._toggle_xaxis)
        self.toggle_button.pack(side='left')
        self.toggle_button['state'] = 'disabled'
        self.toggle_annotations_button = Button(self.root, text="Toggle Annotations", command=self._toggle_annotations)
        self.toggle_annotations_button.pack(side='left')
        self.toggle_annotations_button['state'] = 'disabled'

    def _select_file(self):
        self.file_path.set(filedialog.askopenfilename())

    def _start_analysis(self):
        self.detector = AnomalyDetector(self.file_path.get())
        self.visualizer = AnomalyVisualizer(self.detector)
        fig = self.visualizer.plot_anomalies()
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack()
        self.toggle_button['state'] = 'normal'
        self.toggle_annotations_button['state'] = 'normal'

    def _toggle_xaxis(self):
        self.visualizer.xaxis_mode = 'dates' if self.visualizer.xaxis_mode == 'operations' else 'operations'
        self.canvas.get_tk_widget().pack_forget()
        fig = self.visualizer.plot_anomalies()
        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

    def _toggle_annotations(self):
        for annotation in self.visualizer.annotations:
            annotation.set_visible(not annotation.get_visible())
        plt.draw()

if __name__ == "__main__":
    root = Tk()
    app = Application(root)
    root.mainloop()
