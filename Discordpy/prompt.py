# CB: 1.0 - Importing necessary libraries
import os
import random
import logging
from configparser import ConfigParser
from datetime import datetime
from pathlib import Path

# CB: 1.1 - Setting up logging
logging.basicConfig(filename='app.log', filemode='a',
                    format='%(name)s - %(levelname)s - %(message)s')

# CB: 1.2 - Defining global parameters
PARAMETER_1 = " ::1"
PARAMETER_5 = " ::5"

# CB: 2.0 - FileGenerator class definition
class FileGenerator:
    # CB: 2.1 - Initialization
    def __init__(self, folder_path, output_folder, num_files, 
                 parameters, probabilities):
        self.folder_path = folder_path
        self.output_folder = output_folder
        self.num_files = num_files
        self.parameters = parameters
        self.probabilities = probabilities

    # CB: 2.2 - File reading method
    def read_file(self, file_path):

        # CB: 2.2.1 - File reading with error handling
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                return [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            logging.error(f"File {file_path} not found.")
            raise FileNotFoundError(f"File {file_path} not found.")
        except PermissionError:
            logging.error(f"Permission denied for file {file_path}.")
            raise PermissionError(f"Permission denied for file {file_path}.")
        except UnicodeDecodeError:
            logging.error(f"File {file_path} contains characters that cannot be decoded.")
            raise UnicodeDecodeError(f"File {file_path} contains characters that cannot be decoded.")

    # CB: 2.3 - Random parameter selection method
    def get_random_parameter(self):
        return random.choices(self.parameters, self.probabilities)[0]

    # CB: 2.4 - Parameter requirement check method
    def ensure_required_parameters(self, items):
        required_parameters = [PARAMETER_1, PARAMETER_5]
        for param in required_parameters:
            if not any(param in item for item in items):
                items[random.randint(0, len(items) - 1)] += param

    # CB: 2.5 - File generation method
    def generate_files(self):
        # CB: 2.5.1 - File list creation with error handling
        try:
            file_list = [file for file in os.listdir(self.folder_path) 
                         if file.endswith('.txt')]
        except FileNotFoundError:
            logging.error(f"Folder {self.folder_path} not found.")
            raise FileNotFoundError(f"Folder {self.folder_path} not found.")
        except PermissionError:
            logging.error(f"Permission denied for folder {self.folder_path}.")
            raise PermissionError(f"Permission denied for folder {self.folder_path}.")

        # CB: 2.5.2 - Single file generation loop
        for i in range(1, self.num_files + 1):
            self.generate_single_file(i, file_list)

    # CB: 2.6 - Single file generation method
    def generate_single_file(self, i, file_list):
        # CB: 2.6.1 - File path and item list setup
        file_path = self.output_folder / f"Prompt_{i}.txt"
        items = []

        # CB: 2.6.2 - File list shuffling
        random.shuffle(file_list)

        # CB: 2.6.3 - File processing loop
        for random_file in file_list:
            self.process_file(self.folder_path / random_file, items)

        # CB: 2.6.4 - Ensuring required parameters
        self.ensure_required_parameters(items)

        # CB: 2.6.5 - Content creation
        content = "/image\n" + '\n'.join(items) + "\n--v 5.1"

        # CB: 2.6.6 - File writing with error handling
        try:
            with open(file_path, 'w', encoding='utf-8', errors='ignore') as file:
                file.write(content)
            logging.info(f"File {file_path} successfully created.")
        except PermissionError:
            logging.error(f"Permission denied for file {file_path}.")
            return


    # CB: 2.7 - File processing method
    def process_file(self, random_file, items):
        # CB: 2.7.1 - Maximum item number extraction with error handling
        try:
            max_num_items = int(random_file.name.split(".")[0])
        except ValueError:
            logging.error(f"File name {random_file} cannot be converted to integer.")
            raise ValueError(f"File name {random_file} cannot be converted to integer.")

        # CB: 2.7.2 - File reading and item selection
        lines = self.read_file(random_file)
        if max_num_items == 0 or max_num_items > len(lines):
            return

        # CB: 2.7.3 - Random item selection
        num_items = min(max_num_items, len(lines))
        selected_items = random.sample(lines, num_items)

        # CB: 2.7.4 - Parameter sequence checking and item addition
        for item in selected_items:
            num_parameters = sum(item.count(param) for param in self.parameters)
        if num_parameters == 0:
            logging.info(f"Adding random parameter to item: {item}")
            item += self.get_random_parameter()
            logging.info(f"Item after adding parameter: {item}")
        elif num_parameters > 1:
            logging.error(f"Two or more parameters together in {item}.")
            raise ValueError(f"Two or more parameters together in {item}.")
        items.append(item)

# CB: 3.0 - Main execution
if __name__ == "__main__":
    # CB: 3.1 - Configuration setup
    config = ConfigParser()
    config.read('config.ini')
    folder_path = Path(config.get('DEFAULT', 'folder_path'))
    num_files = config.getint('DEFAULT', 'num_files')
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_folder = Path.cwd() / "dados" / current_time  # Update the output folder path

    # CB: 3.2 - Parameter and probability setup
    parameters = [PARAMETER_1, " ::2", " ::3", " ::4", PARAMETER_5]
    probabilities = [0.4, 0.25, 0.2, 0.1, 0.05]

    # CB: 3.3 - Output folder creation with error handling
    try:
        os.makedirs(output_folder, exist_ok=True)
    except Exception as e:
        logging.error(f"Cannot create directory {output_folder}. Error: {e}")
        exit(1)

    # CB: 3.4 - File generation
    try:
        file_generator = FileGenerator(folder_path, output_folder, num_files,
                                       parameters, probabilities)
        logging.info("FileGenerator instance created successfully.")
        file_generator.generate_files()
        logging.info("File generation process started.")
    except Exception as e:
        logging.error(f"Error in file generation process: {e}")
