import csv
import os

ENCODING = 'utf-8'


def import_csv(filename):
    """returns a list of lists.
       Inner lists are cells, outer lists are rows.
    """
    output = []
    with open(filename, newline='', encoding=ENCODING) as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            item = []
            for cell in row:
                item.append(cell)
            output.append(item)

    return output


def get_file_contents(filename):
    file = open(filename, 'r',  encoding='utf-8')
    contents = file.read()
    file.close()
    return contents


def write_file(filename, contents):
    file = open(filename, 'w', encoding='utf-8')
    file.write(contents)
    file.close()


def create_directory(dirname):
    if not os.path.exists(dirname):
        os.mkdir(dirname)
