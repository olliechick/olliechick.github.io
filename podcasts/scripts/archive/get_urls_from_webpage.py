import sys

import requests


def write_to_file(filename, contents):
    outfile = open(filename, 'w')
    outfile.write(contents)
    outfile.close()


def append_to_file(filename, contents):
    outfile = open(filename, 'a')
    outfile.write(contents)
    outfile.close()


def list_to_strln(alist):
    strln = ''
    for item in alist:
        try:
            strln += item.strip() + '\n'
        except:
            strln += str(item) + '\n'
    strln.strip()
    return strln


def get_redirect_path(url):
    urls = []
    response = requests.get(url)
    for resp in response.history:
        urls.append(resp.url)
    urls.append(response.url)
    return urls


def get_best_url(urls, valid_starts, valid_ends):
    best_url = None
    url_is_valid = True

    if valid_starts is None and valid_ends is None:
        return urls[-1], url_is_valid

    for url in urls:
        # check if it's a wanted url
        # must have at least one of the valid
        # Note that the last valid page redirected to is chosen
        if valid_starts is not None:
            for valid_beginning in valid_starts:
                if url[:len(valid_beginning)] == valid_beginning:
                    best_url = url
        if valid_ends is not None:
            for valid_ending in valid_ends:
                if url[-len(valid_ending):] == valid_ending:
                    best_url = url

    # If there was no valid url
    if best_url is None:
        url_is_valid = False
        if len(urls) < 2:
            best_url = urls[0]
        else:
            # redirections
            best_url = urls[-1]

    return best_url, url_is_valid


def get_title(url):
    """Returns the title of the file in the url and its extension.
       Note that an extension will not contain a period (.).
       If no extension, returns None instead."""
    extension_exists = False
    extension = None
    title_start_index = 0
    title_end_index = len(url)
    i = 0
    for c in url[:-1]:
        if c == '/':
            title_start_index = i + 1
        i += 1

    i = title_start_index
    for c in url[title_start_index:]:
        if c == '.':
            title_end_index = i
            extension_exists = True
        i += 1
    if extension_exists:
        extension = url[title_end_index + 1:]

    title = url[title_start_index:title_end_index]
    return title, extension


def remove_dupes(urls):
    seen_files = set()
    new_urls = []
    for url in urls:
        title = get_title(url)
        if title not in seen_files:
            new_urls.append(url)
            seen_files.add(title)
        else:
            print("DUPE: " + url)
    return new_urls


def generate_contents(lines, output_file, incrementally_write, valid_starts, valid_ends, edit_url, text_template,
                      headings, print_comments=True, only_get_enclosed_urls=False, traverse=False,
                      include_extra_urls=True, keep_duplicates=False):
    """ Generates a list of URLs.
        It will only get URLs that start with strings in the list valid_starts
            (it is OK if they also start with http or https) OR end with strings in valid_ends.
        If print_comments, it will print any <!-- comments -->.
        If only_get_enclosed_urls, it will only print ULRs preceded by '<enclosure url="'.
        If traverse, it will follow redirects.
        If include_extra_urls, it will include more than 1 URL per <item> if they are there.
    """
    output = ''
    num_of_items = 0
    num_of_urls_in_item = 0
    wanted_urls = []
    wanted_full_urls = []
    invalid_urls = []
    invalid_full_urls = []
    failed_urls = []
    failed_full_urls = []
    wanted_urls_outside_item = []
    wanted_full_urls_outside_item = []
    item_no = 1

    in_comment = False
    in_item = False
    outside_item_heading, invalid_heading, failed_heading, footer = headings

    for line_index, line in enumerate(lines):
        print("Processing line " + str(line_index + 1) + " of " + str(len(lines)), end="\r")
        sys.stdout.flush()
        is_a_url = False
        normal = False
        if len(line) < 3:
            continue  # nothing useful in here

        i = 0
        while i <= len(line) - 3:  # while i is not the last or second to last char of the line
            failed_request = False

            # if it's starting a comment
            if not in_comment and (i <= len(line) - 4 and line[i:i + 4] == '<!--'):
                in_comment = True
                if print_comments:
                    output += '\n<COMMENT>\n\n<!--'
                i += 4
                while i < len(line) and line[i:i + 3] != '-->':
                    if print_comments:
                        output += line[i]
                    i += 1

            # if it's in a comment
            elif in_comment:
                while i < len(line) and line[i:i + 3] != '-->':
                    if print_comments:
                        output += line[i]
                    i += 1

            # if it's ending a comment
            if in_comment and line[i:i + 3] == '-->':
                in_comment = False
                if print_comments:
                    output += '-->\n\n</COMMENT>\n'

            # if it's starting an item
            elif not in_comment and i <= len(line) - 6 and line[i:i + 6] == '<item>':
                in_item = True
                num_of_urls_in_item = 0
                num_of_items += 1
                output += "<item " + str(item_no) + ">\n"
                item_no += 1

            # if it's ending an item
            elif in_item and i <= len(line) - 7 and line[i:i + 7] == '</item>':
                in_item = False
                if num_of_urls_in_item == 0 and print_comments:
                    print("NO URLS IN ITEM.")
                output += "</item>\n"

            # if it's a url
            elif ((i <= len(line) - 7 and line[i:i + 7] == 'http://') or
                  len(line) - 8 >= i >= 16 and line[i:i + 8] == 'https://') and \
                    (not only_get_enclosed_urls or line[i - 16:i] == '<enclosure url="'):
                is_a_url = True
                url = ''

                # find ending char
                if i > 0:
                    starting_char = line[i - 1]
                    if starting_char == '>':
                        ending_char = ['<']
                    else:
                        ending_char = [starting_char]
                else:
                    ending_char = [' ', '	', '\n']

                # goes through characters until ending character
                while i < len(line) and line[i] not in ending_char:
                    url += line[i]
                    i += 1

                url = edit_url(url)
                urls = [url]
                if traverse:
                    # get the url, and the entire redirect path - stored in urls
                    try:
                        urls = get_redirect_path(url)
                    except requests.exceptions.RequestException:
                        failed_request = True

                url, url_is_valid = get_best_url(urls, valid_starts, valid_ends)

                # Extract the title (extension is not used)
                title, extension = get_title(url)

                # Count number of URLs in item
                # If we're in an <item>, the URL is valid, the request worked, and we haven't already got it
                if in_item and url_is_valid and not failed_request and (url not in wanted_urls):
                    num_of_urls_in_item += 1

                normal = url_is_valid and (url not in wanted_urls)

                # Append url and full_url to appropriate list - failed, normal, and invalid
                if failed_request and (url not in failed_urls):  # failed
                    number = len(failed_urls)
                    full_url = text_template.format(url=url, title=title, number=number)
                    failed_urls.append(url)
                    failed_full_urls.append(full_url)

                elif normal:  # normal
                    number = len(wanted_urls)
                    full_url = text_template.format(url=url, title=title, number=number)
                    if num_of_urls_in_item == 1 or include_extra_urls:
                        wanted_urls.append(url)
                        wanted_full_urls.append(full_url)
                        output += url

                elif url and not url_is_valid and (url not in invalid_urls):  # invalid
                    number = len(invalid_urls)
                    full_url = text_template.format(url=url, title=title, number=number)
                    invalid_urls.append(url)
                    invalid_full_urls.append(full_url)
                else:
                    print('BAD URL: ', url)
            # print('\n\n===========\n\n' + list_to_strln(wanted_full_urls)
            #       + outside_item_heading
            #       + list_to_strln(wanted_full_urls_outside_item)
            #       + invalid_heading
            #       + list_to_strln(invalid_full_urls)
            #       + failed_heading
            #       + list_to_strln(failed_full_urls)
            #       + footer)
            i += 1

        if incrementally_write and normal and num_of_urls_in_item >= 2:
            if output_file is None:
                print(url)
            else:
                append_to_file(output_file, full_url)

    if not keep_duplicates:
        wanted_full_urls = remove_dupes(wanted_full_urls)

    output += '\n\n\n\n' + list_to_strln(wanted_full_urls) \
              + outside_item_heading \
              + list_to_strln(wanted_full_urls_outside_item) \
              + invalid_heading \
              + list_to_strln(invalid_full_urls) \
              + failed_heading \
              + list_to_strln(failed_full_urls) \
              + footer

    print("Number of items:", num_of_items)
    return output


def generate_url_list(url, output_file, incrementally_write, valid_starts, valid_ends, edit_url, text_template,
                      headings,
                      print_comments=False,
                      traverse=False, online=True, include_extra_urls=True, keep_duplicates=False):
    if valid_starts is not None:
        new_valid_starts = valid_starts[:]
        for valid_start in valid_starts:
            new_valid_starts += ['http://' + valid_start, 'https://' + valid_start]
        valid_starts = new_valid_starts

    print("Downloading feed...")
    try:
        if online:
            file = requests.get(url)
            lines = file.text.split('\n')
        else:
            lines_file = open(url, 'r')
            lines = lines_file.read().split('\n')
            lines_file.close()

        print('Connection successful.')
        contents = generate_contents(lines, output_file, incrementally_write, valid_starts, valid_ends, edit_url,
                                     text_template, headings, print_comments=print_comments, traverse=traverse,
                                     include_extra_urls=include_extra_urls, keep_duplicates=keep_duplicates)
        print('\nDone!\n\n')

    except requests.exceptions.RequestException:
        contents = "Error, couldn't get webpage at " + url

    return contents


def generate_mp3_list(input_url, valid_starts, valid_ends, edit_url, text_template, traverse, output_file,
                      incrementally_write, headings, print_comments=False, online=True,
                      include_extra_urls=True, keep_duplicates=False):
    """Outputs to output_file a list of links to mp3 URLs in the file pointed to by the input URL.
    If output_file is None, then it prints it."""

    url_list = generate_url_list(input_url, output_file, incrementally_write, valid_starts, valid_ends, edit_url,
                                 text_template, headings, traverse=traverse, print_comments=print_comments,
                                 online=online, include_extra_urls=include_extra_urls, keep_duplicates=keep_duplicates)

    if not incrementally_write:
        if output_file is None:
            print(url_list)
        else:
            write_to_file(output_file, url_list)


def main():
    # ========== User-specified input ==========

    # input_url = 'https://olliechick.me/podcasts/clintkaratammy.rss'
    # input_url = 'https://pod.neocities.org/test.html'
    # input_url = 'https://olliechick.me/podcasts/jayjaydomrandell.rss'
    # input_url = 'https://olliechick.co.nz/podcasts/jonobensharyn.rss'
    # input_url = '../stuff.txt'
    input_url = '../../dommegrandell.rss'
    # input_url = '../../test.rss'

    valid_starts = None
    valid_starts = ['web.archive.org']#, 'podcast.mediaworks.nz']#, 'omnystudio.com', 'traffic.omny.fm']
    valid_ends = None  # ['.mp3']
    traverse = incrementally_write = False
    print_comments = False
    output_file = 'output.txt'  # to print, use None
    include_extra_urls = False
    keep_duplicates = True

    outside_item_heading = '\n\n==Valid URLs outside item==\n\n'
    invalid_heading = '\n\n==Invalid URLs==\n\n'
    failed_heading = '\n\n==Failed URLs==\n\n'
    footer = ''

    # text_template = '{url}'
    text_template = 'https://web.archive.org/save/{url}\n'
    # text_template = '<a href="https://web.archive.org/save/{url}">link {number}: {url}</a><br/>'.format(url=url)

    def edit_url(url, title='', number=''):
        # ZM podcasts
        # bits = url.split('/')
        # protocol, foo.html, host, foo.html, foo.html, episode_id, mp3_name = bits
        # url = 'https://api.spreaker.com/v2/episodes/{}/play'.format(episode_id)

        return url

    # =========================================

    headings = outside_item_heading, invalid_heading, failed_heading, footer

    generate_mp3_list(input_url, valid_starts, valid_ends, edit_url, text_template, traverse, output_file,
                      incrementally_write, headings, print_comments=print_comments, online=input_url.startswith('http'),
                      include_extra_urls=include_extra_urls, keep_duplicates=keep_duplicates)


if __name__ == '__main__':
    main()
