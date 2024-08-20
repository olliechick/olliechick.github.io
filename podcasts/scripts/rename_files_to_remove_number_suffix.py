"""
Renames files in the given directory to remove the number suffix.

`my_file_1234.mp3` is renamed to `my_file.mp3`

For each file that cannot be renamed, an error message is displayed.
"""
import os

directory = input("Enter directory: " + os.getcwd() + os.path.sep)

files = os.listdir(directory)

for file in files:
    number = file.split('_')[-1].split('.')[0]
    if number.isdigit():
        # This is a file we need to rename
        new_name = '_'.join(file.split('_')[:-1]) + '.' + '.'.join(file.split('_')[-1].split('.')[1:])

        if new_name in os.listdir(directory):
            # Oh no, there's already a file called that!
            print("Error: " + new_name + " is already a file.")

        else:
            os.rename(os.path.join(directory, file), os.path.join(directory, new_name))
