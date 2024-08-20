import requests

from file_io import get_file_contents


def main():
    # Input
    filename = 'urls.txt'
    convert_web_archive_url_to_save = True

    # Processing
    urls = get_file_contents(filename).split('\n')
    for url in urls:
        resp = requests.head(url)
        if resp.status_code >= 400:
            if convert_web_archive_url_to_save:
                print(url, resp.status_code)
                print('https://web.archive.org/save/https://audio.mediaworks.nz/' + url.split('/https://audio.mediaworks.nz/')[1])
            else:
                print(url)


if __name__ == '__main__':
    main()
