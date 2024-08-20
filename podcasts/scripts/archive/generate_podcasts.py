'''Generate podcast items from csv'''

import csv
import sys

ENCODING = 'utf-8'


TEXT_PATTERN = '''
<item>
 <title>{name}</title>
 <guid>{url}</guid>
 <description>{description}</description>
 <enclosure url="{url}" length="17680040" type="audio/mpeg"/>
 <category>Arts &amp; Entertainment</category>
 <pubDate>{date} {year} {hour}:00:00 +1200</pubDate>
 </item>'''

TEXT_PATTERN_NO_DESCRIPTION = '''
<item>
 <title>{name}</title>
 <guid>{url}</guid>
 <enclosure url="{url}" length="17680040" type="audio/mpeg"/>
 <category>Arts &amp; Entertainment</category>
 <pubDate>{date} {year} {hour}:00:00 +1200</pubDate>
 </item>'''

SPECIAL_TEXT_PATTERN = '''

    <item>
      <title>{name}</title>
      <description>{description}</description>
      <category>Arts &amp; Entertainment</category>
      <pubDate>{date} {year} {hour}:10:00 +1200</pubDate>
      <guid>{url}</guid>
      <enclosure url="{url}" length="17680040" type="audio/mpeg" />

      <itunes:subtitle></itunes:subtitle>
      <itunes:summary></itunes:summary>
      <itunes:author>Guy, Sharyn and Clint</itunes:author>
      <itunes:keywords></itunes:keywords>
    </item>
    '''


def import_csv(filename):
    '''returns a list of lists.
       Inner lists are cells, outer lists are rows.
    '''
    output = []
    with open(filename, newline='', encoding=ENCODING) as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            item = []
            for cell in row:
                item.append(cell)
            output.append(item)

    return output


def fix_date(date):
    day, daynum, mon = date.split()
    if len(daynum) == 1:
        daynum = '0' + daynum
    if len(daynum) != 2:
        raise Exception
    else:
        return day + ' ' + daynum + ' ' + mon


def encode_ampersands(s):
    s_out = ''
    for c in s:
        if c == '&':
            s_out += '&amp;'
        else:
            s_out += c
    return s_out


def extract_name_from_url(url):
    return url.split('/')[-1].split('.mp3')[0]


def format_text(item, year, hour, auto_generate_titles):
    special = ''
    if len(item) == 4:
        name, date, description, url = item
    elif len(item) == 5:
        special, name, date, description, url = item
    else:
        raise Exception(str(len(item)) + str(item))

    if url is None or url == '':
        return ''

    date = fix_date(date)


    if auto_generate_titles:
        name = description = extract_name_from_url(url)


    name = encode_ampersands(name)
    description = encode_ampersands(description)

    if special == 'y':
        return SPECIAL_TEXT_PATTERN.format(name=name, date=date, url=url, description=description, year=year, hour=hour)
    else:
        # normal episode
        if description is None or description == '':
            return TEXT_PATTERN_NO_DESCRIPTION.format(name=name, date=date, url=url, year=year, hour=hour)
        else:
            return TEXT_PATTERN.format(name=name, date=date, url=url, description=description, year=year, hour=hour)


def generate_podcast_feed(filename, year, hour, auto_generate_titles):
    feed = ''
    items = import_csv(filename)
    for item in items[1:]:
        feed += format_text(item, year, hour, auto_generate_titles)
    print(feed)


def main():
    generate_podcast_feed('JB generator.csv', year=2015, hour=19, auto_generate_titles=True)


if __name__ == '__main__':
    main()
