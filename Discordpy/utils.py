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
def select_items(num_files, category_counts, categories, output_dir, progress_bar, aspect_ratio, chaos, stylize, tile):
    # CB: 2.3.1 - Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    # CB: 2.3.2 - Loop over the number of files to be created
    for i in range(num_files):
        try:
            # CB: 2.3.3 - Generate filename based on current time
            current_time = datetime.now().strftime("%Y%m%d%H%M%S")
            # CB: 2.3.4 - Open file for writing
            with open(f"{output_dir}/Prompt_{current_time}_{i+1:02d}.txt", "w") as file:
                # CB: 2.3.5 - Write initial line to file
                file.write("/imagine\n")
                # CB: 2.3.6 - Loop over categories and their counts
                for category, count in category_counts.items():
                    if count > 0: # Only generate items if count is greater than 0
                        # CB: 2.3.7 - Generate parameters for items
                        parameters = generate_parameters(count)
                        # CB: 2.3.8 - Loop over the count of items to be generated
                        for _ in range(count):
                            # CB: 2.3.9 - Select random item from category
                            item = choice(categories[category])
                            # CB: 2.3.10 - Get parameter for item
                            parameter = parameters[_]
                            # CB: 2.3.11 - Write item and parameter to file
                            file.write(f"{item} ::{parameter}\n")
                # CB: 2.3.12 - Write additional parameters to file
                file.write("--v 5.1\n")
                file.write(f"{aspect_ratio}\n")
                file.write(f"{chaos}\n")
                file.write(f"{stylize}\n")
                if tile:
                    file.write(f"{tile}\n")
            # CB: 2.3.13 - Update the progress bar
            progress_bar.setValue((i+1) / num_files * 100)
        except Exception as e:
            # CB: 2.3.14 - Log any errors that occur during file writing
            logging.error(f"Failed to write file: {e}")


