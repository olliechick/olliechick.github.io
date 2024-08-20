import re

from file_io import get_file_contents, write_file

archive_urls = [
'https://archive.org/download/dom-meg-randell-podcast-july-2021/DMR_Only_Fans_-_Friday_16_July_2021_440962.mp3',
'https://archive.org/download/dom-meg-randell-podcast-july-2021/DMR_Only_Fans_-_Friday_23_July_2021_441027.mp3',
'https://archive.org/download/dom-meg-randell-podcast-july-2021/DMR_Only_Fans_-_Friday_2_July_2021_440865.mp3',
'https://archive.org/download/dom-meg-randell-podcast-july-2021/DMR_Only_Fans_-_Friday_9_July_2021_440914.mp3',
'https://archive.org/download/dom-meg-randell-podcast-july-2021/DMR_Only_Fans_-_Monday_12_July_2021_440925.mp3',
'https://archive.org/download/dom-meg-randell-podcast-july-2021/DMR_Only_Fans_-_Monday_19_July_2021_440984.mp3',
'https://archive.org/download/dom-meg-randell-podcast-july-2021/DMR_Only_Fans_-_Monday_26_July_2021_441039.mp3',
'https://archive.org/download/dom-meg-randell-podcast-july-2021/DMR_Only_Fans_-_Monday_5_July_2021_440882.mp3',
'https://archive.org/download/dom-meg-randell-podcast-july-2021/DMR_Only_Fans_-_Thursday_15_July_2021_440954.mp3',
'https://archive.org/download/dom-meg-randell-podcast-july-2021/DMR_Only_Fans_-_Thursday_1_July_2021_440867.mp3',
'https://archive.org/download/dom-meg-randell-podcast-july-2021/DMR_Only_Fans_-_Thursday_29_July_2021_441113.mp3',
'https://archive.org/download/dom-meg-randell-podcast-july-2021/DMR_Only_Fans_-_Thursday_8_July_2021_440907.mp3',
'https://archive.org/download/dom-meg-randell-podcast-july-2021/DMR_Only_Fans_-_Tuesday_13_July_2021_440935.mp3',
'https://archive.org/download/dom-meg-randell-podcast-july-2021/DMR_Only_Fans_-_Tuesday_20_July_2021_440995.mp3',
'https://archive.org/download/dom-meg-randell-podcast-july-2021/DMR_Only_Fans_-_Tuesday_27_July_2021_441094.mp3',
'https://archive.org/download/dom-meg-randell-podcast-july-2021/DMR_Only_Fans_-_Tuesday_6_July_2021_440892.mp3',
'https://archive.org/download/dom-meg-randell-podcast-july-2021/DMR_Only_Fans_-_Wednesday_14_July_2021_440943.mp3',
'https://archive.org/download/dom-meg-randell-podcast-july-2021/DMR_Only_Fans_-_Wednesday_21_July_2021_441006.mp3',
'https://archive.org/download/dom-meg-randell-podcast-july-2021/DMR_Only_Fans_-_Wednesday_28_July_2021_441104.mp3',
'https://archive.org/download/dom-meg-randell-podcast-july-2021/DMR_Only_Fans_-_Wednesday_7_July_2021_440900.mp3',
'https://archive.org/download/dom-meg-randell-podcast-july-2021/Full_Show_Catchup_-_Friday_16_July_2021_440963.mp3',
'https://archive.org/download/dom-meg-randell-podcast-july-2021/Full_Show_Catchup_-_Friday_23_July_2021_441026.mp3',
'https://archive.org/download/dom-meg-randell-podcast-july-2021/Full_Show_Catchup_-_Friday_2_July_2021_440866.mp3',
'https://archive.org/download/dom-meg-randell-podcast-july-2021/Full_Show_Catchup_-_Friday_30_July_2021_441125.mp3',
'https://archive.org/download/dom-meg-randell-podcast-july-2021/Full_Show_Catchup_-_Friday_9_July_2021_440913.mp3',
'https://archive.org/download/dom-meg-randell-podcast-july-2021/Full_Show_Catchup_-_Monday_12_July_2021_440924.mp3',
'https://archive.org/download/dom-meg-randell-podcast-july-2021/Full_Show_Catchup_-_Monday_19_July_2021_440982.mp3',
'https://archive.org/download/dom-meg-randell-podcast-july-2021/Full_Show_Catchup_-_Monday_26_July_2021_441038.mp3',
'https://archive.org/download/dom-meg-randell-podcast-july-2021/Full_Show_Catchup_-_Monday_5_July_2021_440883.mp3',
'https://archive.org/download/dom-meg-randell-podcast-july-2021/Full_Show_Catchup_-_Thursday_15_2021_440951.mp3',
'https://archive.org/download/dom-meg-randell-podcast-july-2021/Full_Show_Catchup_-_Thursday_1_July_2021_440868.mp3',
'https://archive.org/download/dom-meg-randell-podcast-july-2021/Full_Show_Catchup_-_Thursday_22_July_2021_441017.mp3',
'https://archive.org/download/dom-meg-randell-podcast-july-2021/Full_Show_Catchup_-_Thursday_29_July_2021_441114.mp3',
'https://archive.org/download/dom-meg-randell-podcast-july-2021/Full_Show_Catchup_-_Thursday_8_July_2021_440906.mp3',
'https://archive.org/download/dom-meg-randell-podcast-july-2021/Full_Show_Catchup_-_Tuesday_13_July_2021_440936.mp3',
'https://archive.org/download/dom-meg-randell-podcast-july-2021/Full_Show_Catchup_-_Tuesday_20_July_2021_440996.mp3',
'https://archive.org/download/dom-meg-randell-podcast-july-2021/Full_Show_Catchup_-_Tuesday_27_July_2021_441093.mp3',
'https://archive.org/download/dom-meg-randell-podcast-july-2021/Full_Show_Catchup_-_Tuesday_6_July_2021_440893.mp3',
'https://archive.org/download/dom-meg-randell-podcast-july-2021/Full_Show_Catchup_-_Wednesday_14_July_2021_440942.mp3',
'https://archive.org/download/dom-meg-randell-podcast-july-2021/Full_Show_Catchup_-_Wednesday_21_July_2021_441005.mp3',
'https://archive.org/download/dom-meg-randell-podcast-july-2021/Full_Show_Catchup_-_Wednesday_28_July_2021_441105.mp3',
'https://archive.org/download/dom-meg-randell-podcast-july-2021/Full_Show_Catchup_-_Wednesday_7_July_2021_440899.mp3',
]

manual_mappings = {
    'https://omny.fm/shows/dom-meg-randell-podcast-the-edge-1/full-show-catchup-thursday-4-february-2021-1': 'https://archive.org/download/dom-meg-randell-podcast-jan-apr-2021/Full_Show_Catchup_-_Thursday_4_February_2021_81564.mp3',
    'https://omny.fm/shows/dom-meg-randell-podcast-the-edge-1/full-show-catchup-thursday-4-february-2021':
        'https://archive.org/download/dom-meg-randell-podcast-jan-apr-2021/Full_Show_Catchup_-_Thursday_4_February_2021_80887.mp3'
}


def normalise_url(url):
    return url.lower().replace(', ', '-').replace(',_', '-').replace(',-', '-').replace('_', '-').replace('!',
                                                                                                          '').replace(
        ' & ', '-') \
        .replace(', ', '-').replace(' ', '-').replace('---', '-').replace('--', '-')


def standardise_url_name(url):
    # if url.endswith('-2019'):
    #     url = re.sub('-2019$', '', url)
    url = url.replace('4-february-2021-1', '4-march-2021')
    url = url.replace('podcast-catchup', 'catchup-podcast')
    url = url.replace('ctachup', 'catchup')
    url = url.replace('-2020', '')
    if url.endswith('dom-meg-randell-catchup-.mp3'):
        url = url.replace('dom-meg-randell-catchup-.mp3', 'dom-meg-randell-catchup-tuesday-24-march.mp3')
    return url


def set_enclosure_url_to_link(rss_feed_path):
    feed = get_file_contents(rss_feed_path)
    items = feed.split('<item>')
    output = items[0]

    enclosure_url_regex = re.compile("""<enclosure
                    url=\"http.*omny.*\n?.*\"
                    length=\"""")
    media_url_regex = re.compile("""<media:content
                    url=\"http.*omny.*\n?.*\"
                    type=\"audio/mpeg\">
                <media:player
                        url=\"http.*omny.*\"/>
            </media:content>""")

    for item in items[1:]:
        feed_title = item.split('<title>')[1].split('</title>')[0].strip() if len(item.split('<title>')) > 1 else ''
        feed_title = feed_title.replace('&amp;', '&')
        if len(item.split('<link>')) > 1:
            feed_link_url = item.split('<link>')[1].split('</link>')[0].strip()
            feed_link_url_filename = normalise_url(feed_link_url.split('/')[-1] + '.mp3')
            feed_link_url_filename_no_mp3 = normalise_url(feed_link_url.split('/')[-1])
            matching_archive_urls = []
            if feed_link_url in manual_mappings and manual_mappings[feed_link_url] in archive_urls:
                matching_archive_urls.append(manual_mappings[feed_link_url])
            else:
                for archive_url in archive_urls:
                    adjusted_archive_url = '_'.join(archive_url.split('_')[:-1]) + '.' + '.'.join(
                        archive_url.split('_')[-1].split('.')[1:])
                    archive_url_filename = normalise_url(archive_url.split('/')[-1])
                    adjusted_archive_url_filename = normalise_url(adjusted_archive_url.split('/')[-1])
                    feed_title_urlised = normalise_url(feed_title)
                    if archive_url_filename == feed_link_url_filename or adjusted_archive_url_filename == feed_link_url_filename or \
                            adjusted_archive_url_filename.startswith(feed_title_urlised) or \
                            standardise_url_name(adjusted_archive_url_filename).startswith(standardise_url_name(
                                feed_title_urlised)):
                        # archive_url_filename.startswith(feed_link_url_filename_no_mp3) or \
                        # adjusted_archive_url_filename.startswith(feed_link_url_filename_no_mp3) or \
                        matching_archive_urls.append(archive_url)
                    # print("Feed:")
                    # print(feed_link_url_filename_no_mp3)
                    # print(feed_title)
                    # print(feed_title_urlised)
                    # print(standardise_url_name(feed_title_urlised))
                    # print("Archived:")
                    # print(archive_url_filename)
                    # print(adjusted_archive_url_filename)
                    # print(standardise_url_name(adjusted_archive_url_filename))
            if len(matching_archive_urls) > 0:
                if len(matching_archive_urls) > 1:
                    print("❌ ERROR: " + matching_archive_urls[0] + " and " + matching_archive_urls[1] + " are the same")
                actual_url = matching_archive_urls[0].replace(' ', '%20').replace('&', '&amp;')
                print('✅', feed_link_url_filename, '->', matching_archive_urls[0].split('/')[-1])
                new_string = enclosure_url_regex.sub("""<enclosure
                                            url=\"""" + actual_url + """"
                                            length=\"""", item)
                new_string = media_url_regex.sub("""<media:content
                    url=\"""" + actual_url + """\"
                    type="audio/mpeg">
            </media:content>""", new_string)

                output += '<item>' + new_string
            else:
                print("❌ ERROR", feed_link_url)

        else:
            output += '<item>' + item

    write_file("output.rss", output)


def main():
    podcast_feed_filename = './input.rss'
    set_enclosure_url_to_link(podcast_feed_filename)


if __name__ == '__main__':
    main()
