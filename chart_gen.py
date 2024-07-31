import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from parsing_tools import import_csv

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)


def chart_title_gen(stat_type, comparison_type):
    # stat types: genre, track_popularity, track_duration_ms
    # value types: occurrences, ...
    title_object = {}
    match stat_type:
        case 'genres':
            title_object['chart_title'] = "Most Submitted Genres*"
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


# TODO: rework this to be more efficient
def x_filter(json_data, x_min=0, x_max=float('inf'), y_start=0, y_end=float('inf')):
    new_data = {}
    for key, value in json_data.items():
        if x_min <= value <= x_max and key != '':  # exclude empty, ie. no genre
            new_data[key] = value
    new_data = dict(sorted(new_data.items(), key=lambda item: item[1], reverse=True))
    if y_start > 0 or y_end < float('inf'):
        limit_data = {}
        count = 1
        for key, value in new_data.items():
            if y_end >= count >= y_start:
                limit_data[key] = value
            count += 1
        new_data = limit_data
    if y_start > 0:
        limit_data = {}
    return new_data


def bar_chart_gen(json_data, x_stat_type, y_stat_type, horiz_true=False):
    data_keys = list(json_data.keys())
    data_values = list(json_data.values())
    title_object = chart_title_gen(x_stat_type, y_stat_type)
    plt.style.use('pitayasmoothie-dark.mplstyle')  # third-party dark background theme; not included
    # plt.style.use('seaborn-v0_8-darkgrid')  # built-in light theme
    x_tick_interval = 2
    x_chart_dimension = 18  # dimensions are reversed in horizontal
    y_chart_dimension = 8
    title_size = 16
    label_size = 12

    if not horiz_true:
        plt.figure(figsize=(x_chart_dimension, y_chart_dimension))
        plt.xticks(rotation=90, ha='center')
        plt.yticks(np.arange(0, max(data_values) + 1, x_tick_interval))  # y tick interval
        plt.title(title_object['chart_title'], fontsize=title_size)
        plt.xlabel(title_object['xaxis_title'], fontsize=label_size)
        plt.ylabel(title_object['yaxis_title'], fontsize=label_size)
        plt.bar(data_keys, data_values, width=0.8)
    elif horiz_true:
        plt.figure(figsize=(y_chart_dimension, x_chart_dimension))  # inverted in horizonal
        plt.title(title_object['chart_title'], fontsize=title_size, fontweight='bold')
        plt.xlabel(title_object['yaxis_title'], fontsize=label_size)  # titles are reversed in horizontal
        plt.ylabel(title_object['xaxis_title'], fontsize=label_size)
        plt.xticks(np.arange(0, max(data_values) + 1, x_tick_interval))
        data_keys = list(reversed(data_keys))  # reversed for descending order
        data_values = list(reversed(data_values))
        plt.barh(data_keys, data_values)

    plt.savefig(f'charts/bar.png', dpi=300, bbox_inches='tight')  # tight fixes padding and margin
    plt.show()
    return
