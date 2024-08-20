import requests as requests
from datetime import timedelta, date

DATE = 0
URL = 1


def daterange(date1, date2):
    for n in range(int((date2 - date1).days) + 1):
        yield date1 + timedelta(n)


def get_date_number(dt):
    day = dt.strftime('%d')

    if day[0] == '0':
        day = day[1]

    return day


def get_date_number_with_suffix(dt):
    day = dt.strftime('%d')
    if day[0] == '1':
        return day + 'th'

    if day[0] == '0':
        day = day[1]

    if day[-1] == '1':
        return day + 'st'
    elif day[-1] == '2':
        return day + 'nd'
    elif day[-1] == '3':
        return day + 'rd'
    else:
        return day + 'th'


def is_weekday(dt):
    return int(dt.strftime('%w')) in [1, 2, 3, 4, 5]


def generate_between_dates(start_dt, end_dt, what_to_generate, month_code):
    for dt in daterange(start_dt, end_dt):
        # print(dt.strftime("%y-%m-%d"))
        if is_weekday(dt):
            if what_to_generate == URL:
                url = ('http://podcast.mediaworks.co.nz/TheRockFM/JAB_PODCAST_' + get_date_number(dt)
                       + dt.strftime(month_code + '%y.mp3'))
                print(url)
        elif what_to_generate == DATE:
            print(dt.strftime('%a, %d %b'))  # eg Mon, 23 Sep

            # print(dt.strftime('JMD%y_%B')
            #       + get_date_number_with_suffix(dt))


def main():
    start_dt = date(2014, 1, 3)
    end_dt = date(2014, 12, 25)
    what_to_generate = URL
    month_code = "%b"

    generate_between_dates(start_dt, end_dt, what_to_generate, month_code)


if __name__ == '__main__':
    main()
