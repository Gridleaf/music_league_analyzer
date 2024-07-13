from spotify_api_interface import token, get_playlist, get_artists
from league_season_link_scraper import season_id_scraper
from math import floor


def playlist_track_data(playlist_id):
    playlist_json = get_playlist(token, playlist_id)
    playlist_name = playlist_json['name']

    playlist_data = [{'playlist_name': playlist_name}]  # first index is metadata

    total_track_counter = 0
    total_duration = 0

    for _ in playlist_json['tracks']['items']:
        track_name = playlist_json['tracks']['items'][total_track_counter]['track']['name']
        track_duration_ms = playlist_json['tracks']['items'][total_track_counter]['track']['duration_ms']
        total_duration += track_duration_ms
        track_popularity = playlist_json['tracks']['items'][total_track_counter]['track']['popularity']
        album_year = int(playlist_json['tracks']['items'][total_track_counter]['track']['album']['release_date'][0:4])  # only year

        playlist_artist_data = playlist_json['tracks']['items'][total_track_counter]['track']['artists']
        artist_ids = []  # artist data may be a list of multiple artists
        track_artists = []
        for artist in playlist_artist_data:  # must iterate over and scrape artist IDs for genre info
            artist_ids.append(artist['id'])
            track_artists.append(artist['name'])
        track_genres = []
        artists_data = get_artists(token, artist_ids)  # multiple artists in 1 request
        for artist in artists_data['artists']:
            for genre in artist['genres']:
                if genre not in track_genres:  # prevent duplicate genres
                    track_genres.append(genre)

        total_track_counter += 1
        track_data = {
            'track_number': total_track_counter,
            'track_name': track_name,
            'track_artists': track_artists,
            'track_duration_ms': track_duration_ms,
            'track_popularity': track_popularity,
            'album_year': album_year,
            'track_genres': track_genres
        }
        playlist_data.append(track_data)

    playlist_data[0]['track_count'] = total_track_counter  # update metadata
    playlist_data[0]['playlist_duration'] = total_duration

    return playlist_data  # return lists, first index is metadata


def multiplaylist_track_data(playlist_id_list):
    multiplaylist_data = []
    for playlist_id in playlist_id_list:
        playlist_data = playlist_track_data(playlist_id)
        multiplaylist_data.append(playlist_data)
    return multiplaylist_data
