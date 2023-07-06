from random import choice, shuffle, randint
import os
import json
import logging
from datetime import datetime

logging.basicConfig(filename='app.log', level=logging.INFO)

def load_categories(file):
    try:
        with open(file, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error loading file {file}: {e}")
        return {}

def generate_parameters(num_items, is_range=False):
    parameters = [1, 2, 3, 4] * (num_items // 4) + [1, 2, 3, 4][:num_items % 4]
    parameters[0] = 1
    if num_items > 4:
        parameters[-1] = 5
    shuffle(parameters)
    return parameters

def write_file(file_path, items, aspect_ratio, chaos, stylize, tile, weird):
    with open(file_path, "w") as file:
        file.write("/imagine\n")
        for item in items:
            file.write(f"{item}\n")
        file.write("--v 5.1\n")
        file.write(f"{aspect_ratio}\n")
        file.write(f"{chaos}\n")
        file.write(f"{stylize}\n")
        if tile:
            file.write(f"{tile}\n")
        if weird:
            file.write(f"{weird}\n")

def select_items(num_files, category_counts, categories, output_dir, progress_bar, aspect_ratio, chaos, stylize, tile, weird):
    os.makedirs(output_dir, exist_ok=True)
    for i in range(num_files):
        try:
            current_time = datetime.now().strftime("%Y%m%d%H%M%S")
            file_path = f"{output_dir}/Prompt_{current_time}_{i+1:02d}.txt"
            items = []
            for category, (count, is_range) in category_counts.items():
                if count > 0:
                    if is_range:
                        count = randint(1, count)
                    parameters = generate_parameters(count, is_range)
                    for _ in range(count):
                        item = choice(categories[category])
                        parameter = parameters[_]
                        items.append(f"{item} ::{parameter}")
            shuffle(items)
            write_file(file_path, items, aspect_ratio, chaos, stylize, tile, weird)
            progress_bar.setValue((i+1) / num_files * 100)
        except Exception as e:
            logging.error(f"Failed to write file: {e}")
