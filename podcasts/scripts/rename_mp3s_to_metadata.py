"""
Renames MP3 files to the title in metadata.
"""

import os

import eyed3

directory = input("Enter directory: " + os.getcwd() + os.path.sep)

files = os.listdir(directory)

for file in [file for file in files if file[-4:] == '.mp3']:
    full_filepath = os.path.join(directory, file)

    audioFile = eyed3.load(full_filepath)
    new_name = audioFile.tag.title

    if new_name == file:
        # Already has the right name
        pass

    if new_name in os.listdir(directory):
        # Oh no, there's already a file called that!
        print("Error: " + new_name + " is already a file.")

    else:
        os.rename(os.path.join(directory, file), os.path.join(directory, new_name))
