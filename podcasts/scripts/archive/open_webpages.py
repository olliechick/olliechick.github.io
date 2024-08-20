import requests

import urllib.request
import webbrowser
from file_io import import_csv

from selenium import webdriver
from time import sleep


def open_21_webpages_from_file(filename, ending):
    urls = import_csv(filename)
    urls = [url for url in urls if (url is not None and len(url) > 0 and len(url[0]) > 4)]
    urls = [url[0] for url in urls]
    urls = [url for url in urls if (url[:4] == 'http' and (ending is None or url[-len(ending):] == ending))]
    for url, _1, _2, _3, _4, _5, _6, _7, _8, _9, _10, _11, _12, _13, _14, _15, _16, _17, _18, _19, _20 in zip(
            *[iter(urls)] * 21):
        url_subset = [_1, _2, _3, _4, _5, _6, _7, _8, _9, _10, _11, _12, _13, _14, _15, _16, _17, _18, _19, _20]
        print(url, 'to', _20)
        # urllib.request.urlretrieve(url[0], 'foo.html')
        # response = requests.get(url[0])
        # print(response)
        # webbrowser.open(url[0])
        driver = webdriver.Chrome()
        driver.get(url)
        for sub_url in url_subset:
            driver.execute_script("window.open('" + sub_url + "');")
        input("Push enter to continue...")
        # driver.quit()


def open_6_webpages_from_file(filename, ending):
    urls = import_csv(filename)
    urls = [url for url in urls if (url is not None and len(url) > 0 and len(url[0]) > 4)]
    urls = [url[0] for url in urls]
    urls = [url for url in urls if (url[:4] == 'http' and (ending is None or url[-len(ending):] == ending))]
    for url, _1, _2, _3, _4, _5 in zip(
            *[iter(urls)] * 6):
        url_subset = [_1, _2, _3, _4, _5]
        print(url, 'to', _5)
        # urllib.request.urlretrieve(url[0], 'foo.html')
        # response = requests.get(url[0])
        # print(response)
        # webbrowser.open(url[0])
        driver = webdriver.Chrome()
        driver.get(url)
        for sub_url in url_subset:
            driver.execute_script("window.open('" + sub_url + "');")
        input("Push enter to continue...")
        # driver.quit()


def open_2_webpages_from_file(filename, ending):
    urls = import_csv(filename)
    urls = [url for url in urls if (url is not None and len(url) > 0 and len(url[0]) > 4)]
    urls = [url[0] for url in urls]
    urls = [url for url in urls if (url[:4] == 'http' and (ending is None or url[-len(ending):] == ending))]
    for url, next_url in zip(*[iter(urls)] * 2):
        print(url, 'and', next_url)
        driver = webdriver.Chrome()
        driver.get(url)
        driver.execute_script("window.open('" + next_url + "');")
        input("Push enter to continue...")
        driver.quit()


def open_webpages_from_file(filename, ending, how_many_at_once):
    if how_many_at_once == 2:
        open_2_webpages_from_file(filename, ending)
    elif how_many_at_once == 6:
        open_6_webpages_from_file(filename, ending)
    elif how_many_at_once == 21:
        open_21_webpages_from_file(filename, ending)
    else:
        raise ValueError("Invalid number of URLs at once ({}).".format(how_many_at_once))


def main():
    filename = 'output.txt'
    # filename = 'test.txt'
    # filename = 'find_one_missing_in_here.txt'

    ending = None
    # ending = 'mp3'

    how_many_at_once = 2

    open_webpages_from_file(filename, ending, how_many_at_once)


if __name__ == '__main__':
    main()
