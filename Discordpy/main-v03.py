# CB: 1.0 - Import necessary modules
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QPushButton, QTextEdit, QVBoxLayout, QWidget
from random import choice
import sys
import os

# CB: 1.1 - Load categories from JSON file
import json

def load_categories(file):
    with open(file, 'r') as f:
        categories = json.load(f)
    return categories

# CB: 2.0 - Define main window class
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Random Item Selector")

        # CB: 2.1 - Create widgets
        self.file_selector = QComboBox()
        self.file_selector.addItems([str(i) for i in range(1, 11)])  # Add options 1-10

        self.item_selector = QComboBox()
        self.item_selector.addItems([str(i) for i in range(1, 11)])  # Add options 1-10

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_process)  # Connect button click to start_process function

        self.result_box = QTextEdit()

        # CB: 2.2 - Arrange widgets in a vertical layout
        layout = QVBoxLayout()
        layout.addWidget(self.file_selector)
        layout.addWidget(self.item_selector)
        layout.addWidget(self.start_button)
        layout.addWidget(self.result_box)

        # CB: 2.3 - Create a central widget to hold the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    # CB: 2.4 - Define start_process function
    def start_process(self):
        num_files = int(self.file_selector.currentText())
        num_items = int(self.item_selector.currentText())
        self.select_items(num_files, num_items)

    # CB: 2.5 - Define item selection and file writing function
    def select_items(self, num_files, num_items):
        # Define item categories and possible items
        categories = {
            "Art_Style": ["Art Nouveau", "Art Deco", "Baroque", "Rococo", "Neoclassicism", "Romanticism", "Renaissance", "Dutch Golden Age", "Realism", "Impressionism", "Neo-Impressionism", "Pointillism", "Fauvism", "Expressionism", "Cubism", "Futurism", "Geometric", "Dadaism", "Minimalism", "Pop Art", "Still Life", "Ukiyo-e", "Watercolors", "Mural", "Surrealism", "Abstract Expressionism", "Tonalism", "Luminism", "Precisionism", "Symbolism", "Suprematism", "Constructivism", "De Stijl", "Op Art", "Photorealism"],
            "Camera": ["Sony a7R IV Sony FE 24-70mm f/2.8 GM", "Canon EOS 5D Mark IV Canon EF 50mm f/1.2L", "Nikon D850 Nikon AF-S NIKKOR 70-200mm f/2.8E", "Fujifilm X-T4 Fujinon XF16mm F1.4 R WR", "Olympus OM-D E-M1 Mark III M.ZuikoDigital ED 60mm f/2.8 Macro", "Sony a7 III Sony FE 85mm f/1.8", "Canon EOS R Canon RF 15-35mm f/2.8L IS USM", "Nikon Z7 Nikon Z 24-70mm f/2.8 S", "Fujifilm GFX 50R Fujinon GF32-64mmF4 R LM WR", "Panasonic Lumix DC-GH5 Leica DG Vario-Elmarit 12-60mm f/2.8-4 ASPH", "Sony a6000 Sony E 35mm f/1.8 OSS", "Canon EOS M50 Canon EF-M 22mm f/2 STM", "Nikon D5600 Nikon AF-S DX NIKKOR 35mm f/1.8G", "Fujifilm X100F Fujinon 23mm f/2", "Olympus PEN-F M.Zuiko Digital 17mm f/1.8", "Sony a7S III Sony FE 24mm f/1.4 GM", "Canon EOS R6 Canon RF 28-70mm f/2L USM", "Nikon Z6 II Nikon Z 50mm f/1.8 S", "Fujifilm X-Pro3 Fujinon XF 56mm f/1.2 R", "Olympus OM-D E-M10 Mark IV M.Zuiko Digital ED 14-42mm f/3.5-5.6 EZ", "Leica M10-R with Leica Summilux-M 35mm f/1.4 ASPH", "Canon EOS R5 with Canon RF 85mm F1.2L USM DS", "Nikon Z7 II with Nikkor Z 50mm f/1.8 S", "Sony Alpha A7 III with Sony FE 24-70mm f/2.8 GM", "Fujifilm X-T4 with Fujinon XF 16mm F1.4 R WR", "Olympus OM-D E-M1 Mark III with M.Zuiko Digital ED 12-40mm f/2.8 PRO", "Panasonic Lumix S1R with Lumix S PRO 70-200mm F4 O.I.S.", "Hasselblad X1D II 50C with XCD 3,5/45P", "Sigma fp with Sigma 35mm F1.2 DG DN Art", "Nikon D850 with AF-S NIKKOR 14-24mm f/2.8G ED", "Canon EOS-1D X Mark III with Canon EF 70-200mm f/2.8L IS III USM", "Sony Alpha A1 with Sony FE 12-24mm F2.8 GM", "Fujifilm GFX 100S with GF 110mmF2 R LM WR", "Leica SL2-S with Leica Vario-Elmarit-SL 24-90mm f/2.8-4 ASPH"]
        }

        # Select random items and write them to files
        for i in range(num_files):
            with open(f"output{i+1}.txt", "w") as file:
                for _ in range(num_items):
                    category = choice(list(categories.keys()))
                    item = choice(categories[category])
                    file.write(f"{category}: {item}\n")

        # Display a message in the result box
        self.result_box.setText(f"Successfully created {num_files} file(s) with {num_items} item(s) each.")

# CB: 3.0 - Create application instance and main window
app = QApplication(sys.argv)
main_window = MainWindow()

# CB: 4.0 - Show the window and execute the application
main_window.show()
sys.exit(app.exec_())