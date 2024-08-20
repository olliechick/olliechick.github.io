import collections


def get_urls():
    url_list_file = open('url_list.txt', 'r')
    urls = url_list_file.read().split('\n')
    url_list_file.close()
    print('There are {} URLs.'.format(len(urls)))
    print_duplicate_files(urls)
    return set(urls)


def get_files():
    file_list_file = open('file_list.txt', 'r')
    files = file_list_file.read().split('\n')
    file_list_file.close()
    print('There are {} files.'.format(len(files)))
    print_duplicate_files(files)
    return set(files)


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
    print_duplicate_files(new_files)
    return set(new_files)


def remove_preceding_number_and_underscore(files):
    new_files = []
    for file in files:
        bits = file.split('_')
        first_bit = bits[0]
        new_file_name = ''

        if first_bit.isdigit():
            bits = bits[1:]

        for bit in bits:
            new_file_name += bit + '_'
        new_file_name = new_file_name[:-1]
        new_files.append(new_file_name)
    print_duplicate_files(new_files)
    return set(new_files)


def get_file_name_from_urls(urls):
    new_urls = set()
    for url in urls:
        new_urls.add(url.split('/')[-1])
    return new_urls


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

    # print([x for x in new_files if not seen.add(x)])


def print_differences(files, urls):
    print('\n{} files and {} urls.'.format(len(files), len(urls)))

    print("\nFiles that aren't URLs ({}):\n".format(len(files.difference(urls))))
    for file in files.difference(urls):
        print('*', file)

    print("\nURLs that aren't files ({}):\n".format(len(urls.difference(files))))
    for file in urls.difference(files):
        print('*', file)

    # for i, file in enumerate(list(files)):
    #     print(i, file)


def main():
    urls = get_urls()
    files = get_files()

    urls = get_file_name_from_urls(urls)

    print("\nRemoving '_xxx' and 'xxx_'s from files...")
    files = remove_proceding_underscore_and_number(files)
    # files = remove_preceding_number_and_underscore(files)
    # files = remove_proceding_underscore_and_number(files)

    print("\nRemoving '_xxx' and 'xxx_'s from urls...")
    # urls = remove_proceding_underscore_and_number(urls)
    # urls = remove_preceding_number_and_underscore(urls)

    print_duplicate_files(files)

    print_differences(files, urls)

    print("\n\nFiles")
    print(files)

    print("\n\nURLs")
    print(urls)


if __name__ == '__main__':
    main()
