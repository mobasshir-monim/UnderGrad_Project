def alphabets_data(file_path):
    data = {}
    with open(file_path, "r") as file:
        lines = file.readlines()
        for i in range(0, len(lines), 2):  # Skip every other line
            key_values = lines[i + 1].strip().split(",")
            key = key_values[0]
            values = list(map(float, lines[i + 1].strip().split(",")[1:]))
            data[key] = values
    return data
