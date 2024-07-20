import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from playlist_parser import import_csv

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)


def chart_title_gen(stat_type, comparison_type):
    # stat types: genre, track_popularity, track_duration_ms
    # value types: occurrences, ...
    title_object = {}
    match stat_type:
        case 'genres':
            title_object['chart_title'] = "Artist Genres"
            title_object['xaxis_title'] = "Genre"
        case 'track_duration_ms':
            title_object['chart_title'] = "Track Durations"
            title_object["xaxis_title"] = "Duration (seconds)"
        case 'track_popularity':
            title_object['chart_title'] = "Track Popularity"
            title_object["xaxis_title"] = "Popularity"
    match comparison_type:
        case 'occurrences':
            title_object['yaxis_title'] = 'Occurrences'
    return title_object


def csv_list_convert(string):
    replace_characters = ['[', ']', "'"]
    new_string = string
    for character in replace_characters:
        if character in new_string:
            new_string = new_string.replace(character, '')
    new_string = new_string.split(', ')
    return new_string


def csv_genre_aggregator(csv_data):
    genre_dict = {}
    for track in csv_data['genres']:
        list_convert = csv_list_convert(track)
        for genre in list_convert:
            if genre not in genre_dict:
                genre_dict[genre] = 1
            if genre in genre_dict:
                genre_dict[genre] += 1
    return genre_dict


def interval_gen(filtered_json_data, interval):
    new_data = {}
    return


def data_filter(json_data, minimum, maximum, limit):
    new_data = {}
    for key, value in json_data.items():
        if minimum <= value <= maximum and key != '':  # exclude empty, ie. no genre
            new_data[key] = value
    new_data = dict(sorted(new_data.items(), key=lambda item: item[1], reverse=True))
    if limit > 0:
        limit_data = {}
        count = 1
        for key, value in new_data.items():
            if count <= limit:
                limit_data[key] = value
                count += 1
        new_data = limit_data
    return new_data


def bar_chart_gen(json_data, stat_type, comparison_type):
    data_keys = list(json_data.keys())
    data_values = list(json_data.values())

    plt.figure(figsize=(10, 14))  # dimensions
    plt.style.use('seaborn-v0_8-darkgrid')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(np.arange(0, max(data_values) + 1, 2))  # y tick interval

    title_object = chart_title_gen(stat_type, comparison_type)
    plt.title(title_object['chart_title'])
    plt.xlabel(title_object['xaxis_title'])
    plt.ylabel(title_object['yaxis_title'])

    plt.bar(data_keys, data_values, width=0.8)
    plt.savefig(f'charts/bar.png')
    plt.show()
    return
