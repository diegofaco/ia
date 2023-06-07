import os

# CODEBLOCK: 1.0 - Define directory and files
dir_path = os.path.dirname(os.path.realpath(__file__))
tabulate_dir = os.path.join(dir_path, 'tabulate')
txt_files = [f for f in os.listdir(tabulate_dir) if f.endswith('.txt')]

# CODEBLOCK: 1.1 - Open input files with utf-8 encoding
file_handles = [open(os.path.join(tabulate_dir, f), 'r', encoding='utf-8') for f in txt_files]

# CODEBLOCK: 1.2 - Open output file with utf-8 encoding
with open(os.path.join(dir_path, 'table.txt'), 'w', encoding='utf-8') as out_file:
    # CODEBLOCK: 1.2.1 - Write headers
    out_file.write('|' + '|'.join(txt_files) + '|\n')
    
    # CODEBLOCK: 1.2.2 - Write rows
    while True:
        rows = []
        end_of_files = 0
        for file_handle in file_handles:
            line = file_handle.readline().strip()
            if line == '':
                end_of_files += 1
                rows.append('')
            else:
                rows.append(line)
        if end_of_files == len(file_handles):
            break
        out_file.write('|' + '|'.join(rows) + '|\n')

# CODEBLOCK: 1.3 - Close all file handles
for file_handle in file_handles:
    file_handle.close()