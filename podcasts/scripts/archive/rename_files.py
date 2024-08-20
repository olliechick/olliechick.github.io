import os

NOTHING = 0
PRINT = 1
RENAME = 2


def remove_proceding_underscore_and_number(files):
    new_files = []
    for file in files:
        bits = file.split('_')
        last_bit = bits[-1].split('.mp3')[0]
        new_file_name = ''
        if last_bit.isdigit():
            for bit in bits[:-1]:
                new_file_name += bit + '_'

            new_file_name = new_file_name[:-1] + '.mp3'
        else:
            for bit in bits:
                new_file_name += bit + '_'
            new_file_name = new_file_name[:-1]
        new_files.append(new_file_name)
    return new_files


def print_duplicate_files(files):
    seen = {}
    dupes = set()
    for x in files:
        if x not in seen:
            seen[x] = 1
        else:
            if seen[x] == 1:
                dupes.add(x)
            seen[x] += 1
    if len(dupes) != 0:
        print("Duplicates:\n")
        for dupe in dupes:
            print(dupe)
    else:
        print("No duplicates.")


def remove_underscore_number_from_names(directory, what_to_do):
    old_filenames = [filename for filename in os.listdir(directory) if filename.endswith('.mp3')]
    new_filenames = remove_proceding_underscore_and_number(old_filenames)
    print(len(set(new_filenames)))
    print_duplicate_files(new_filenames)

    num_of_spaces = len(max(old_filenames, key=len)) + 2

    number_of_files = len(old_filenames)
    if len(old_filenames) != len(new_filenames):
        input("ERROR! there aren't as many new filenames as old filenames!")

    for old_file, new_file in zip(old_filenames, new_filenames):
        if what_to_do == PRINT:
            print(old_file, ' ' * (num_of_spaces - len(old_file)), new_file)
        elif what_to_do == RENAME:
            os.rename(directory + old_file, directory + new_file)
            if len(os.listdir(directory)) != number_of_files:
                input("ERROR! There is no longer {} files! ({} was just processed.)".format(number_of_files, old_file))
    print("There were {} files.".format(len(new_filenames)))


def main():
    directory = '/home/ollie/Documents/Archives/Podcasts/jbs FROM PHONE (originals)/'
    what_to_do = NOTHING

    remove_underscore_number_from_names(directory, what_to_do)


if __name__ == '__main__':
    main()
