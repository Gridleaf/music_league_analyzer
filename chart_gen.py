import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)


def chart_title_gen(stat_type, comparison_type):
    # stat types: genre, track_popularity, track_duration_ms
    # value types: occurrences, ...
    title_object = {'note': ''}
    match stat_type:
        case 'genres':
            title_object['chart_title'] = "Artist Genres"
            title_object['xaxis_title'] = "Genre"
        case 'track_duration_ms':
            title_object['chart_title'] = "Track Duration"
            title_object["xaxis_title"] = "Duration (seconds)"
        case 'track_popularity':
            title_object['chart_title'] = "Track Popularity"
            title_object["xaxis_title"] = "Popularity"
        case 'album_year':
            title_object['chart_title'] = "Album Release Year*"
            title_object['xaxis_title'] = "Year"
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


def stat_year_aggregator(csv_data):
    new_data = {}
    year_list = []  # to search if added; can't search for strings
    for track in csv_data['album_year']:
        year_list.append(track)
    sorted_list = sorted(year_list)

    added_list = []
    for year in sorted_list:
        if year in added_list:
            new_data[str(year)] += 1  # convert to string for label compatibility
        else:
            new_data[str(year)] = 1
            added_list.append(year)
    return new_data


def csv_genre_aggregator(csv_data):
    genre_dict = {}
    for track in csv_data['genres']:
        list_convert = csv_list_convert(track)
        for genre in list_convert:
            if genre in genre_dict:
                genre_dict[genre] += 1
            else:
                genre_dict[genre] = 1
    return genre_dict


def stat_popularity_aggregator(csv_data):
    new_data = {}
    count = 0
    popularity_list = []
    for track in csv_data['track_popularity']:
        popularity_list.append(track)
    while count <= 100:
        if count in popularity_list:
            if count in new_data:
                new_data[count] += 1
            else:
                new_data[count] = 1
            popularity_list.remove(count)
        else:
            if count not in new_data:
                new_data[count] = 0
            count += 1
    return new_data


def stat_time_aggregator(csv_data):  # same as general aggregator, but divides by 1000 to convert ms to seconds
    new_data = {}
    for item in csv_data['track_duration_ms']:
        if item not in new_data:
            new_data[int(round(item/1000))] = 1
        if item in new_data:
            new_data[int(round(item/1000))] += 1
    return new_data


def x_interval_gen(stat_json, interval, single_end=False):
    sorted_data = dict(sorted(stat_json.items()))
    keys = []
    values = []
    for key, value in sorted_data.items():
        keys.append(key)  # easier to work with lists, and uses max(keys) for while loop
        values.append(value)

    new_data = {}
    interval_end = interval - 1
    interval_start = 0
    current_sum = 0
    count = 0
    while interval_end <= max(keys):
        if keys[count] <= interval_end:
            current_sum += values[count]
            count += 1
        else:  # if greater than current interval, add sum to dict, increase interval, reset sum
            new_data[f'{interval_start} - {interval_end}'] = current_sum
            interval_start += interval
            interval_end += interval
            current_sum = 0
    # catch any remaining
    current_sum += values[count]
    if single_end:  # if you don't want it to end in a range (ex. 0-100 popularity)
        new_data[f'{interval_start}'] = current_sum
    else:
        new_data[f'{interval_start} - {interval_end}'] = current_sum
    return new_data


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


def value_labels(x, y, vertical):
    if not vertical:
        for i in range(len(x)):
            print(i, y[i])
            # plt.text(1,1,"Hello")
            plt.text(i, y[i], y[i], ha='center')
    if vertical:
        for i in range(len(x))[::-1]:  # reverse for descending order
            plt.text(y[i], i, y[i], va='center')


# TODO: reformat repetitions
def bar_chart_gen(json_data, x_stat_type, y_stat_type, x_dimension, y_dimension, x_interval, y_footer, labels=True, vertical=False, reverse=False):
    data_keys = list(json_data.keys())
    data_values = list(json_data.values())
    title_object = chart_title_gen(x_stat_type, y_stat_type)
    plt.style.use('pitayasmoothie-dark.mplstyle')  # third-party dark background theme; not included
    # plt.style.use('seaborn-v0_8-darkgrid')  # built-in light theme
    x_tick_interval = x_interval
    x_chart_dimension = x_dimension  # dimensions are reversed in vertical
    y_chart_dimension = y_dimension
    title_size = 24
    label_size = 14
    y_footer = y_footer

    if reverse:
        data_keys = list(reversed(data_keys))  # reversed for descending order
        data_values = list(reversed(data_values))

    if not vertical:
        plt.figure(figsize=(x_chart_dimension, y_chart_dimension))
        plt.xticks(rotation=90, ha='center')
        plt.yticks(np.arange(0, max(data_values) + 1, x_tick_interval))  # y tick interval
        plt.title(title_object['chart_title'], fontsize=title_size, fontweight='bold')
        plt.xlabel(title_object['xaxis_title'], fontsize=label_size, fontweight='bold')
        plt.ylabel(title_object['yaxis_title'], fontsize=label_size, fontweight='bold')
        if labels:
            value_labels(data_keys, data_values, vertical)
        plt.annotate(f"Midhunters Music League Season 2", xy=(1, y_footer), xycoords='axes fraction', ha='right')
        plt.bar(data_keys, data_values, width=0.8)
    elif vertical:
        plt.figure(figsize=(y_chart_dimension, x_chart_dimension))  # inverted in vertical
        plt.title(title_object['chart_title'], fontsize=title_size, fontweight='bold', pad=0)
        plt.xlabel(title_object['yaxis_title'], fontsize=label_size, fontweight='bold')  # titles are reversed in vertical
        plt.ylabel(title_object['xaxis_title'], fontsize=label_size, fontweight='bold')
        plt.xticks(np.arange(0, max(data_values) + 1, x_tick_interval))
        if labels:
            value_labels(data_keys, data_values, vertical)
        plt.annotate(f"Midhunters Music League Season 2", xy=(1, y_footer), xycoords='axes fraction', ha='right')
        plt.barh(data_keys, data_values)

    plt.savefig(f'charts/bar.png', dpi=300, bbox_inches='tight')  # tight fixes padding and margin
    plt.show()
    return
