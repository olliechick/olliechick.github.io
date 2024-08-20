"""
Given a string containing URLS, and a string of what each url ends with, prints a list of them.
"""


def extract_urls(s, url_start, url_ending):
    items = s.split(url_start)
    urls = []
    for item in items[1:]:
        url = url_start + item.split(url_ending)[0] + url_ending
        urls.append(url)
        # print(url)

    print(urls)


def main():
    url_start = "https://archive.org"
    url_ending = ".mp3"
    s = """
                  <link itemprop="associatedMedia" href="https://archive.org/download/jab-podcast-2015a/JAB_PODCAST_10Feb15_40061.mp3">
             
        """
    extract_urls(s, url_start, url_ending)


if __name__ == '__main__':
    main()
