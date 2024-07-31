import csv, json
from pandas import read_csv
from datetime import datetime


def get_datestamp():
    time_now = datetime.now()
    return time_now.strftime("%Y-%m-%d")


def export_csv(playlist_data):
    datestamp = get_datestamp()
    playlist_counter = 1

    def write_playlist_csv(playlist_data, writer):

            track_index = 1  # skip metadata
            while track_index < len(playlist_data):
                row_data = [
                    playlist_data[track_index]['track_name'],
                    playlist_data[track_index]['track_artists'],
                    playlist_data[track_index]['track_duration_ms'],
                    playlist_data[track_index]['album_year'],
                    playlist_data[track_index]['track_genres'],
                    playlist_data[track_index]['track_popularity'],
                    playlist_data[0]['playlist_name']
                ]
                writer.writerow(row_data)
                track_index += 1

    with open(f'data/playlist-export_{datestamp}.csv', 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        fields = [
            "track_name",
            "artist_name",
            "track_duration_ms",
            "album_year",
            "genres",
            "track_popularity",
            "playlist_name"
        ]
        writer.writerow(fields)
        if 'playlist_name' in playlist_data[0]:
            write_playlist_csv(playlist_data, writer)
        if 'playlist_name' in playlist_data[0][0]:
            for playlist in playlist_data:
                write_playlist_csv(playlist, writer)
                playlist_counter += 1
    return


def export_json(playlist_data):
    datestamp = get_datestamp()
    with open(f'data/playlist-export_{datestamp}.json', 'w', encoding='utf-8') as json_file:
        json.dump(playlist_data, json_file, ensure_ascii=True, indent=4)
    return


def import_json(json_datestamp):
    with open(f'data/playlist-export_{json_datestamp}.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        return data


def import_csv(csv_datestamp):
    playlist_counter = 1
    csv_data = read_csv(f'data/playlist-export_{csv_datestamp}.csv', delimiter=';', encoding='utf-8')
    return csv_data
