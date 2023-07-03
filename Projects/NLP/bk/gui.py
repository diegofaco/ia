# gui.py

import tkinter as tk
from sentiment_analysis import SentimentAnalysis

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.input_label = tk.Label(self, text="Enter text:")
        self.input_label.pack()

        self.input_text = tk.Entry(self)
        self.input_text.pack()

        self.analyze_button = tk.Button(self)
        self.analyze_button["text"] = "Analyze"
        self.analyze_button["command"] = self.analyze_text
        self.analyze_button.pack()

        self.output_label = tk.Label(self, text="")
        self.output_label.pack()

    def analyze_text(self):
        text = self.input_text.get()
        sentiment = SentimentAnalysis().predict(text)
        self.output_label["text"] = "Sentiment: " + sentiment

root = tk.Tk()
app = Application(master=root)
app.mainloop()
