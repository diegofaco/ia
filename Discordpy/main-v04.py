# CB: 1.0 - Import necessary modules
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QWidget, QLabel
from random import choice, shuffle
import sys
import os
import json
import logging

# CB: 1.1 - Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO)

# CB: 2.0 - Define utility functions
def load_categories(file):
    # CB: 2.1 - Load categories from JSON file
    try:
        with open(file, 'r') as f:
            categories = json.load(f)
        return categories
    except Exception as e:
        logging.error(f"Failed to load categories: {e}")
        return {}

def generate_parameters(num_items):
    # CB: 2.2 - Function to generate parameters with specified odds
    parameters = [1, 2, 3, 4, 5] * (num_items // 5) + [1, 2, 3, 4, 5][:num_items % 5]
    shuffle(parameters)
    parameters[0] = 1  # Ensure at least one ::1
    parameters[-1] = 5  # Ensure at least one ::5
    shuffle(parameters)
    return parameters

def select_items(num_files, num_items, categories):
    # CB: 2.3 - Define item selection and file writing function
    if not os.path.exists("output"):
        os.makedirs("output")
    for i in range(num_files):
        try:
            with open(f"output/Prompt_{i+1:02d}.txt", "w") as file:
                file.write("/imagine\n")
                parameters = generate_parameters(num_items)
                for _ in range(num_items):
                    category = choice(list(categories.keys()))
                    item = choice(categories[category])
                    parameter = parameters[_]
                    file.write(f"{item} ::{parameter}\n")
                file.write("--v 5.1\n")
        except Exception as e:
            logging.error(f"Failed to write file: {e}")

# CB: 3.0 - Define main window class
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Random Item Selector")
        self.categories = load_categories("categories.json")

        # CB: 3.1 - Create widgets
        self.file_label = QLabel("Number of Files:")
        self.file_selector = QComboBox()
        self.file_selector.addItems([str(i) for i in range(1, 11)])  # Add options 1-10

        self.item_label = QLabel("Number of Items:")
        self.item_selector = QComboBox()
        self.item_selector.addItems([str(i) for i in range(1, 11)])  # Add options 1-10

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_process)  # Connect button click to start_process function

        self.result_box = QTextEdit()

        # CB: 3.2 - Arrange widgets in a vertical layout
        layout = QVBoxLayout()

        file_layout = QHBoxLayout()
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.file_selector)
        layout.addLayout(file_layout)

        item_layout = QHBoxLayout()
        item_layout.addWidget(self.item_label)
        item_layout.addWidget(self.item_selector)
        layout.addLayout(item_layout)

        layout.addWidget(self.start_button)
        layout.addWidget(self.result_box)

        # CB: 3.3 - Create a central widget to hold
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    # CB: 3.4 - Define start_process function
    def start_process(self):
        num_files = int(self.file_selector.currentText())
        num_items = int(self.item_selector.currentText())
        select_items(num_files, num_items, self.categories)

# CB: 4.0 - Create application instance and main window
app = QApplication(sys.argv)
main_window = MainWindow()

# CB: 5.0 - Show the window and execute the application
main_window.show()
sys.exit(app.exec_())
