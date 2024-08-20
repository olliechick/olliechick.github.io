"""
Used to generate a list of filenames and URLs from an RSS podcast feed.
It will check that the MP3 files exist in '`root_dir`/`year`/`mp3_filename`.mp3',
and throw an exception if any don't (it will still find it if it is actually named '`mp3_filename`*.mp3').
It will then print out, for each episode, the template formatted accordingly.

Edit the main() function with:
 * the filename of the RSS podcast feed
 * the template, where {n} will be replaced accordingly:
 * * {0} with the mp3 filename (without the .mp3 extension)
 * * {1} with the name of the episode
 * * {2} with the year the episode was published
 * the root directory of the MP3 files
 * whether or not to create files called names/{2}/{0}.txt with the content {1}

 ==== OR =====
 Used to generate a CSV of (title, description) tuples.
"""
import glob

import feedparser
import os.path
import csv

from file_io import write_file, create_directory


def file_exists(dir, file):
    """returns True if the file exist in the directory"""
    return os.path.isfile(os.path.join(dir, file))


def get_mp3_filename(mp3_path):
    """returns filename of mp3, without .mp3 extension"""
    return mp3_path.split('/')[-1].split('.mp3')[0]


def generate_name_list(rss_feed_path, template, root_dir, create_files, check_file_exists=True):
    feed = feedparser.parse(rss_feed_path)

    episodes = []

    for item in feed['items']:
        title = item['title']
        url = item['link']
        year = str(item['published_parsed'].tm_year)
        mp3_name = get_mp3_filename(url)
        dir = os.path.join(root_dir, year)

        if check_file_exists:
            mp3_exists = file_exists(dir, mp3_name + '.mp3')
            if not mp3_exists:
                possibilities = glob.glob(os.path.join(dir, mp3_name + '*.mp3'))
                if len(possibilities) != 1:
                    print(mp3_name, possibilities)
                    raise Exception("len of possibilities == " + str(len(possibilities)) + " for " + mp3_name)
                mp3_name = get_mp3_filename(possibilities[0])

        episode = (mp3_name, title, year)
        episodes.append(episode)

    if create_files:
        for (mp3_name, title, year) in episodes:
            create_directory('names')
            create_directory(os.path.join('names', year))
            write_file(os.path.join('names', year, mp3_name + '.txt'), title)

    templates = [template.format(mp3_name, title, year) for (mp3_name, title, year) in episodes]
    return '\n\n'.join(templates)


def generate_description_csv(rss_feed_path):
    feed = feedparser.parse(rss_feed_path)

    with open('descriptions.csv', 'w', encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for item in feed['items']:
            title = item['title']
            description = item['description'].replace('\n                   ', '')
            writer.writerow([title, description])


def main():
    podcast_feed_filename = '../guysharynclint.rss'
    template = """ffmpeg -loop 1 -i guysharynclint.jpg -i "{2}/{0}.mp3" -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest -vf drawtext="fontfile=./cabin-regular.ttf: \\
textfile='names/{2}/{0}.txt': fontcolor=white: fontsize=16: box=1: boxcolor=black@0.8: \\
boxborderw=5: x=(w-text_w)/2: y=5*(h-text_h)/6" "videos/{1}.mp4\""""
    root_dir = '/media/ollie/extra/Pre-2020 podcasts/Guy, Sharyn and Clint'
    create_files = True
    check_file_exists = False

    selection = input("Enter 0 to generate a name list, or 1 to generate a description CSV: ")
    while selection not in ['0', '1']:
        selection = input("Enter 0 to generate a name list, or 1 to generate a description CSV: ")

    if selection == '0':
        output = generate_name_list(podcast_feed_filename, template, root_dir, create_files, check_file_exists)
        print(output)
    else:
        generate_description_csv(podcast_feed_filename)


if __name__ == '__main__':
    main()
