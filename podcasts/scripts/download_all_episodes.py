"""
Downloads all episodes of a podcast from a given feed URL, and saves them as the name of the podcast,
and modifies the date to be the date the episode was published.

Edit the main function with the appropriate data
"""
import os
import time
import urllib.request

import feedparser


def get_mp3_filename(mp3_path):
    """returns filename of mp3, without .mp3 extension"""
    return mp3_path.split('/')[-1].split('.mp3')[0]


def set_date(filename, timestamp):
    """ Sets date of file `filename` to the time in the POSIX timestamp `timestamp`. """
    os.utime(filename, (timestamp, timestamp))


def download_episodes(feed_url, directory):
    feed = feedparser.parse(feed_url)
    os.mkdir(directory)

    for item in feed['items']:
        title = item['title']
        for char in '<>:"/\\|?*':
            title = title.replace(char, '_')
        filename = os.path.join(directory, title + '.mp3')

        url = item['link']
        timestamp = time.mktime(item['published_parsed'])

        print("Downloading " + filename)
        urllib.request.urlretrieve(url, filename)
        set_date(filename, timestamp)


def main():
    feed_url = 'https://rss.acast.com/the-real-pod'
    directory = 'realpod'
    download_episodes(feed_url, directory)


if __name__ == '__main__':
    main()
