from math import floor


def multiplaylist_check(json_data):  # return True if multiple playlists
    if 'playlist_name' in json_data[0]:
        return False
    if 'playlist_name' in json_data[0][0]:
        return True


def ms_to_readable_time(time_ms):
    raw_minutes = (time_ms / 1000) / 60
    time_minutes = floor(raw_minutes)
    time_seconds = floor((raw_minutes - time_minutes) * 60)
    return time_minutes, time_seconds


def int_list_median(int_list):
    sorted_list = sorted(int_list)  # sort low to high
    if len(sorted_list) % 2 == 0:  # if list length is even, median is mean of two middle points
        second_mid_point = int(len(sorted_list) / 2)  # converted to int for ease of use
        first_mid_point = second_mid_point - 1
        list_median = (sorted_list[first_mid_point] + sorted_list[second_mid_point]) / 2
    else:
        mid_point = floor(len(sorted_list) / 2)  # dividing by 2 gives middle index
        list_median = sorted_list[mid_point]
    return list_median


def normalize_string(string):
    string = string.replace(" ", "-")
    return ''.join(ch for ch in string if ch.isalnum() or ch == "-")  # keep letter, numbers, and '-'


def range_generator(data_list, interval):
    return


def list_getter(playlist_data, function_name):
    return_list = []
    if 'playlist_name' in playlist_data[0]:  # checks if single or multiple playlists
        return_list = function_name(playlist_data)
    elif 'playlist_name' in playlist_data[0][0]:
        for playlist in playlist_data:
            return_list.extend(function_name(playlist))
    return return_list


def duration_calc(playlist_data):  # high, low, mean, median
    duration_list = []
    if 'playlist_name' in playlist_data[0]:
        print('1')
    elif 'playlist_name' in playlist_data[0][0]:
        for playlist in playlist_data:
            print('2')
    return


def popularity_calc(playlist_data):

    def get_popularity_list(playlist_data):
        popularities = []
        for track in playlist_data[1::]:
            popularities.append(track['track_popularity'])
        return popularities

    popularity_list = list_getter(playlist_data, get_popularity_list)

    sum_popularity = sum(popularity_list)
    median_popularity = int_list_median(popularity_list)
    mean_popularity = round(sum_popularity / len(popularity_list), 1)
    low_popularity = min(popularity_list)
    high_popularity = max(popularity_list)

    return low_popularity, high_popularity, median_popularity, mean_popularity


def year_calc(playlist_data):
    return


def genre_calc(playlist_data):
    return
