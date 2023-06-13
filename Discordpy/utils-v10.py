# CB: 1.0 - Import necessary modules
from random import choice, shuffle
import os
import json
import logging
from datetime import datetime

# CB: 1.1 - Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO)

# CB: 2.0 - Define utility functions
def load_categories(file):
    # CB: 2.1 - Load categories from JSON file
    try:
        with open(file, 'r') as f:
            categories = json.load(f)
        return categories
    except FileNotFoundError:
        logging.error(f"File not found: {file}")
        return {}
    except json.JSONDecodeError as e:
        logging.error(f"Failed todecode JSON from file: {file}. Error: {e}")
        return {}

def generate_parameters(num_items):
    # CB: 2.2 - Function to generate parameters with specified odds
    parameters = [1, 2, 3, 4] * (num_items // 4) + [1, 2, 3, 4][:num_items % 4]
    shuffle(parameters)
    parameters[0] = 1 # Ensure at least one ::1
    if num_items > 4:
        parameters[-1] = 5 # Ensure at least one ::5
    shuffle(parameters)
    return parameters

# CB: 2.3 - Define item selection and file writing function
def select_items(num_files, category_counts, categories, output_dir, progress_bar):
    os.makedirs(output_dir, exist_ok=True)
    for i in range(num_files):
        try:
            current_time = datetime.now().strftime("%Y%m%d%H%M%S")
            with open(f"{output_dir}/Prompt_{current_time}_{i+1:02d}.txt", "w") as file:
                file.write("/imagine\n")
                for category, count in category_counts.items():
                    if count > 0: # Only generate items if count is greater than 0
                        parameters = generate_parameters(count)
                        for _ in range(count):
                            item = choice(categories[category])
                            parameter = parameters[_]
                            file.write(f"{item} ::{parameter}\n")
                file.write("--v 5.1\n")
            progress_bar.setValue((i+1) / num_files * 100)  # Update the progress bar
        except Exception as e:
            logging.error(f"Failed to write file: {e}")
