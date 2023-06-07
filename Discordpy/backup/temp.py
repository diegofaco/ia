def remove_blank_lines():
    with open('arquivo.txt', 'r') as f:
        lines = f.readlines()

    with open('arquivo.txt', 'w') as f:
        for line in lines:
            if line.strip():
                f.write(line)

remove_blank_lines()
