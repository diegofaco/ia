# CB: 1.0 - Import necessary libraries
import json

# CB: 2.0 - Define function to convert text file to JSON
def convert_to_json(input_file, output_file):
    report = []
    with open(input_file, 'r') as f:
        for line in f:
            element_type = line[0]
            content = line[1:].strip()
            if element_type == 'H':
                report.append({"header": content})
            elif element_type == 'F':
                report.append({"footer": content})
            elif element_type == 'h':
                report.append({"heading": content})
            elif element_type == 's':
                report.append({"subheading": content})
            elif element_type == 'b':
                report.append({"body_text": content})
            elif element_type == 'B':
                report.append({"bullet_points": content.split(', ')})
            elif element_type == 'I':
                report.append({"image": content})
            elif element_type == 'T':
                report.append({"table": [row.split(', ') for row in content.split('; ')]})
    with open(output_file, 'w') as f:
        json.dump(report, f)
