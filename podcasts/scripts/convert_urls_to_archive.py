"""
Queries the wayback machine for each URL with the domain in `domains`,
and replaces it with an archived version if available.
"""
import re

import requests
import json

from file_io import write_file

successes = 0
fails = 0

def get_archive_version_of_url(url):
    global successes, fails
    response_str = requests.get('https://archive.org/wayback/available?url=' + url).text
    json_acceptable_string = response_str.replace(" '", " \"").replace("',", "\",")
    try:
        response = json.loads(json_acceptable_string)
    except Exception as e:
        print(json_acceptable_string)
        raise e
    try:
        timestamp = response['archived_snapshots']['closest']['timestamp']
        successes += 1
        return url.strip(), ('https://web.archive.org/web/' + timestamp + 'if_/' + url).strip()
    except KeyError:
        print('https://web.archive.org/save/' + url)
        fails += 1
        return url.strip(), url.strip()


def url_in_domains(url, domains):
    full_domains = domains[:]
    for valid_start in domains:
        full_domains += ['http://' + valid_start, 'https://' + valid_start]

    for domain in full_domains:
        if url[:len(domain)] == domain:
            return True

    return False


def convert_urls_to_archive(feed_url, domains, redirect_domains, output):
    if feed_url.startswith('http'):
        file = requests.get(feed_url)
        input_ = file.text
        lines = input_.split('\n')
    else:
        lines_file = open(feed_url, 'r', encoding='utf-8')
        input_ = lines_file.read()
        lines = input_.split('\n')
        lines_file.close()

    replacements = dict()

    for line in lines:
        if len(line) < 3:
            continue  # nothing useful in here

        i = 0
        in_comment = False
        while i <= len(line) - 3:  # while i is not the last or second to last char of the line
            # if it's starting a comment
            if not in_comment and (i <= len(line) - 4 and line[i:i + 4] == '<!--'):
                in_comment = True
                i += 4
                while i < len(line) and line[i:i + 3] != '-->':
                    i += 1

            # if it's in a comment
            elif in_comment:
                while i < len(line) and line[i:i + 3] != '-->':
                    i += 1

            # if it's ending a comment
            if in_comment and line[i:i + 3] == '-->':
                in_comment = False

            # if it's a url
            elif ((i <= len(line) - 7 and line[i:i + 7] == 'http://') or
                  len(line) - 8 >= i >= 16 and line[i:i + 8] == 'https://'):
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

                url_is_valid = url_in_domains(url, domains)
                if url_is_valid:
                    if url not in replacements:
                        url, new_url = get_archive_version_of_url(url)
                        replacements[url] = new_url
                elif url_in_domains(url, redirect_domains):
                    redirected_url = requests.head(url, allow_redirects=True).url
                    _, new_url = get_archive_version_of_url(redirected_url)
                    url = url.strip()
                    replacements[url] = new_url
            i += 1

    print(replacements)

    for url, new_url in replacements.items():
        input_ = input_.replace(url, new_url)

    write_file(output, input_)


def main():
    global successes, fails
    feed_url = 'input.rss'
    # feed_url = '../test.rss'

    domains = ['audio.mediaworks.nz', 'podcast.mediaworks.nz', 'podcast.mediaworks.co.nz']
    redirect_domains = ['feedproxy.google.com']

    output = 'output.rss'

    convert_urls_to_archive(feed_url, domains, redirect_domains, output)
    print("Successes", successes, "; fails", fails)

if __name__ == '__main__':
    main()
