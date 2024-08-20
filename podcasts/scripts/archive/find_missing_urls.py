import requests as requests
from datetime import date
from generate_urls import get_date_number_with_suffix


def get_month_names(month):
    month_names = {
        1: ['Janurary', 'Januaray'],
        2: ['Febuary'],
        3: [],
        4: [],
        5: [],
        6: [],
        7: [],
        8: [],
        9: ['Sept', 'Septemeber', 'Septmeber'],
        10: ['Octber', 'Octobear'],
        11: ['Novemember', 'Novembear'],
        12: ['Decemeber', 'Decembre', 'Decmeber']
    }
    for m in month_names.items():
        dt = date(2000, m[0], 1)
        m[1].append(dt.strftime('%b'))
        m[1].append(dt.strftime('%B'))
    return month_names[month]


def get_date_number(dt):
    day = dt.strftime('%d')

    if day[0] == '0':
        day = day[1]

    return day


def get_all_combos(dt):
    prefix = dt.strftime('http://podcast.mediaworks.co.nz/TheEdge/Audio/JayJayMikeDom/')
    middle_bits = []
    for month_name in get_month_names(dt.month):
        middle_bits += [
            # JMD
            # _Jan15th _January15th _Jan15 _January15
            dt.strftime('JMD%y_') + month_name + get_date_number_with_suffix(dt),
            dt.strftime('JMD%y_') + month_name + get_date_number(dt),
            # Jan15th January15th Jan15 January15
            dt.strftime('JMD%y') + month_name + get_date_number_with_suffix(dt),
            dt.strftime('JMD%y') + month_name + get_date_number(dt),
            # JD
            # _Jan15th _January15th _Jan15 _January15
            dt.strftime('JD%y_') + month_name + get_date_number_with_suffix(dt),
            dt.strftime('JD%y_') + month_name + get_date_number(dt),
            # Jan15th January15th Jan15 January15
            dt.strftime('JD%y') + month_name + get_date_number_with_suffix(dt),
            dt.strftime('JD%y') + month_name + get_date_number(dt),
            # JM
            # _Jan15th _January15th _Jan15 _January15
            dt.strftime('JM%y_') + month_name + get_date_number_with_suffix(dt),
            dt.strftime('JM%y_') + month_name + get_date_number(dt),
            # Jan15th January15th Jan15 January15
            dt.strftime('JM%y') + month_name + get_date_number_with_suffix(dt),
            dt.strftime('JM%y') + month_name + get_date_number(dt),
            # MD
            # _Jan15th _January15th _Jan15 _January15
            dt.strftime('MD%y_') + month_name + get_date_number_with_suffix(dt),
            dt.strftime('MD%y_') + month_name + get_date_number(dt),
            # Jan15th January15th Jan15 January15
            dt.strftime('MD%y') + month_name + get_date_number_with_suffix(dt),
            dt.strftime('MD%y') + month_name + get_date_number(dt), ]
    suffix = '.mp3'
    new_middle_bits = []
    for middle_bit in middle_bits:
        new_middle_bits.append(middle_bit + '_')
    middle_bits.extend(new_middle_bits)

    return [prefix + i + suffix for i in middle_bits]


def print_non_404s(urls):
    for url in urls:
        response = requests.get(url)
        if response.status_code != 404:
            print(response.status_code, url)


def find_missing_dates(verbose):
    dates = [
        date(2010, 6, 1),
        date(2010, 6, 2),
        date(2010, 6, 3),
        date(2010, 6, 10),
        date(2010, 6, 18),
        date(2010, 6, 29),
        date(2010, 7, 22),
        date(2010, 7, 23),
        date(2010, 7, 30),
        date(2010, 9, 23),
        date(2010, 10, 4),
        date(2010, 10, 28),
        date(2010, 11, 24),
        date(2010, 11, 30),
        date(2010, 12, 17),
        date(2010, 12, 21),

        date(2011, 1, 19),
        date(2011, 2, 18),
        date(2011, 4, 26),
        date(2011, 5, 13),
        date(2011, 6, 17),
        date(2011, 7, 14),
        date(2011, 8, 9),
        date(2011, 10, 3),
        date(2011, 12, 23),

        date(2012, 5, 28),
        date(2012, 8, 28),
        date(2012, 9, 24),
        date(2012, 11, 20),

        date(2013, 3, 8),
        date(2013, 3, 22),
        date(2013, 4, 22),
        date(2013, 5, 9),
        date(2013, 5, 24),
        date(2013, 8, 5),
        date(2013, 11, 5),

        date(2014, 4, 2),
        date(2014, 7, 10),
        date(2014, 8, 15),
        date(2014, 10, 8),

        date(2015, 3, 10),
        date(2015, 3, 17),
        date(2015, 3, 20),
        date(2015, 7, 10),
    ]
    for dt in dates:
        if verbose:
            print(dt.strftime('%d %b %y'))
        urls = get_all_combos(dt)
        print_non_404s(urls)


def main():
    find_missing_dates(True)


if __name__ == '__main__':
    main()
