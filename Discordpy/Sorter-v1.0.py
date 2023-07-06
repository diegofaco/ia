import sys
import os
import json
import logging
from random import sample, randint, choice, shuffle
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QGridLayout, QFileDialog, QProgressBar, QCheckBox, QMessageBox, QLineEdit
from PyQt5.QtGui import QFont, QIcon

logging.basicConfig(filename='app.log', level=logging.INFO)

OPTIONS = {
    "NUM": [""] + [str(i) for i in range(101)],
    "ASPECT_RATIO": [""] + [f"--ar {i}:{j}" for i in range(1, 10) for j in range(1, 10)],
    "CHAOS": [""] + [f"--c {i}" for i in range(0, 101, 5)],
    "STYLIZE": [""] + [f"--s {i}" for i in range(0, 1001, 10)],
    "TILE": ["", "--tile"],
    "WEIRD": [""] + [f"--weird {i}" for i in range(0, 3001, 10)]
}

class Utils:
    @staticmethod
    def load_categories(file):
        try:
            with open(file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.error(f"Error loading file {file}: {e}")
            return {}

    @staticmethod
    def generate_parameters(num_items):
        parameters = sample([1, 2, 3, 4, 5], k=num_items)
        return parameters

    @staticmethod
    def write_file(file_path, data):
        with open(file_path, "w") as file:
            json.dump(data, file)

    @staticmethod
    def generate_items(category_counts, categories):
        items = []
        for category, (count, is_range) in category_counts.items():
            if count > 0:
                if is_range:
                    count = randint(1, count)
                parameters = Utils.generate_parameters(count)
                for _ in range(count):
                    item = choice(categories[category])
                    parameter = parameters[_]
                    items.append(f"{item} ::{parameter}")
        shuffle(items)
        logging.info(f"Generated items: {items}")  # Add logging
        return items

    @staticmethod
    def select_items(num_files, category_counts, categories, output_dir, progress_bar, user_input, aspect_ratio, chaos, stylize, tile, weird):
        os.makedirs(output_dir, exist_ok=True)
        for i in range(num_files):
            try:
                current_time = datetime.now().strftime("%Y%m%d%H%M%S")
                file_path = f"{output_dir}/Prompt_{current_time}_{os.getpid()}_{i+1:02d}.json"
                items = Utils.generate_items(category_counts, categories)
                data = Utils.build_data(user_input, items, aspect_ratio, chaos, stylize, tile, weird)
                Utils.write_file(file_path, data)
                progress_bar.setValue(int((i+1) / num_files * 100))  # Convert to int
                logging.info(f"File written: {file_path}")  # Add logging
            except Exception as e:
                logging.error(f"Failed to write file: {e}")

    @staticmethod
    def build_data(user_input, items, aspect_ratio, chaos, stylize, tile, weird):
        data = {
            "user_input": user_input,
            "items": items,
            "aspect_ratio": aspect_ratio,
            "chaos": chaos,
            "stylize": stylize,
            "tile": tile,
            "weird": weird
        }
        return data

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Random Item Selector")
        self.categories = Utils.load_categories("categories.json")
        self.create_widgets()
        self.arrange_widgets()
        self.statusBar().showMessage('Ready')

    def create_combobox(self, options, default=None):
        combobox = QComboBox()
        combobox.addItems(options)
        if default:
            combobox.setCurrentIndex(options.index(default))
        return combobox

    def create_widgets(self):
        self.file_label = QLabel("Number of Files:")
        self.file_selector = self.create_combobox(OPTIONS["NUM"], "0")
        self.category_selectors = {category: (self.create_combobox(OPTIONS["NUM"], "0"), QCheckBox("Range?")) for category in self.categories.keys()}
        self.aspect_ratio_selector = self.create_combobox(OPTIONS["ASPECT_RATIO"], "--ar 1:1")
        self.chaos_selector = self.create_combobox(OPTIONS["CHAOS"], "--c 0")
        self.stylize_selector = self.create_combobox(OPTIONS["STYLIZE"], "--s 0")
        self.tile_selector = self.create_combobox(OPTIONS["TILE"], "")
        self.weird_selector = self.create_combobox(OPTIONS["WEIRD"], "--weird 0")
        self.user_input = QLineEdit()
        self.start_button = QPushButton("Generate Files")
        self.start_button.setStyleSheet("QPushButton { background-color: #2ecc71; font-weight: bold; color: white; } QPushButton:hover { background-color: #27ae60; }")
        self.start_button.setIcon(QIcon('start_icon.png'))
        self.start_button.clicked.connect(self.start_process)
        self.result_box = QTextEdit()
        self.progress_bar = QProgressBar(self)

    @staticmethod
    def write_file(file_path, data):
        with open(file_path, "w") as file:
            for item in data["items"]:
                file.write(f"{item}\n")
            file.write(f"{data['user_input']}\n")
            file.write(f"{data['aspect_ratio']}\n")
            file.write(f"{data['chaos']}\n")
            file.write(f"{data['stylize']}\n")
            file.write(f"{data['tile']}\n")
            file.write(f"{data['weird']}\n")

    def arrange_widgets(self):
        layout = QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(self.file_label, 0, 0)
        layout.addWidget(self.file_selector, 0, 1)
        row = 1
        for category, (selector, checkbox) in self.category_selectors.items():
            layout.addWidget(QLabel(f"{category} Items:"), row, 0)
            layout.addWidget(selector, row, 1)
            layout.addWidget(checkbox, row, 2)
            row += 1
        layout.addWidget(QLabel("Aspect Ratio:"), row, 0)
        layout.addWidget(self.aspect_ratio_selector, row, 1)
        row += 1
        layout.addWidget(QLabel("Chaos:"), row, 0)
        layout.addWidget(self.chaos_selector, row, 1)
        row += 1
        layout.addWidget(QLabel("Stylize:"), row, 0)
        layout.addWidget(self.stylize_selector, row, 1)
        row += 1
        layout.addWidget(QLabel("Tile:"), row, 0)
        layout.addWidget(self.tile_selector, row, 1)
        row += 1
        layout.addWidget(QLabel("Weird:"), row, 0)
        layout.addWidget(self.weird_selector, row, 1)
        row += 1
        layout.addWidget(QLabel("User Input:"), row, 0)
        layout.addWidget(self.user_input, row, 1)
        row += 1
        layout.addWidget(self.start_button, row, 0, 1, 2)
        layout.addWidget(self.result_box, row+1, 0, 1, 2)
        layout.addWidget(self.progress_bar, row+2, 0, 1, 2)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def start_process(self):
        try:
            num_files = int(self.file_selector.currentText())
            category_counts = {category: (int(selector.currentText()), checkbox.isChecked()) for category, (selector, checkbox) in self.category_selectors.items()}
            output_dir = QFileDialog.getExistingDirectory(self, 'Select Output Directory')
            user_input = self.user_input.text()
            aspect_ratio = self.aspect_ratio_selector.currentText()
            chaos = self.chaos_selector.currentText()
            stylize = self.stylize_selector.currentText()
            tile = self.tile_selector.currentText()
            weird = self.weird_selector.currentText()
            Utils.select_items(num_files, category_counts, self.categories, output_dir, self.progress_bar, user_input, aspect_ratio, chaos, stylize, tile, weird)
            self.statusBar().showMessage('Files generated successfully')
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            self.statusBar().showMessage('Error generating files')

app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec_())
