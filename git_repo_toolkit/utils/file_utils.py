import os


def save_in_file(file_name, content):
    directory = os.path.dirname(file_name)
    if not os.path.exists(directory) and directory != '':
        os.makedirs(directory)
    with open(file_name, "w") as file:
        file.write(content)
