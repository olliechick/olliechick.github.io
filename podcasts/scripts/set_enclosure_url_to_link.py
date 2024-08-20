"""
Writes to output.rss a version of `podcast_feed_filename` with enclosure URLs replaced with <link> url.

Specifically, `<enclosure url="THIS">` is replaced by `<link>THIS</link>`.
"""
import re

from file_io import get_file_contents, write_file


def set_enclosure_url_to_link(rss_feed_path):
    feed = get_file_contents(rss_feed_path)
    items = feed.split('<item>')
    output = items[0]

    reg = """<enclosure
                    url=\"http.*omny.*\"
                    length=\""""
    p = re.compile(reg)

    for item in items[1:]:
        if len(item.split('<link>')) > 1:
            new_url = item.split('<link>')[1].split('</link>')[0].strip()
            print(new_url)
            new_string = p.sub("""<enclosure
                            url=\"""" + new_url + """"
                            length=\"""", item)

            output += '<item>' + new_string
        else:
            output += '<item>' + item

    write_file("output.rss", output)


def main():
    podcast_feed_filename = '../sean.rss'
    set_enclosure_url_to_link(podcast_feed_filename)


if __name__ == '__main__':
    main()
