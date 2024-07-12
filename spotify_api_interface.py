from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Types": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token


token = get_token()


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


def get_playlist(token, playlist_id):
    url = "https://api.spotify.com/v1/playlists/"
    headers = get_auth_header(token)
    query = f"{playlist_id}?&fields=name,tracks.items(track(name, id, popularity, track_number, duration_ms, album(release_date, id), artists(name, id, genres)))"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)
    return json_result


def get_artists(token, artist_ids):
    ids_param = ','.join(artist_ids)
    url = f"https://api.spotify.com/v1/artists?ids="
    headers = get_auth_header(token)

    query_url = url + ids_param
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)
    return json_result


def get_tracks(token, track_ids):
    ids_param = ','.join(track_ids)
    url = "https://api.spotify.com/v1/tracks?ids="
    headers = get_auth_header(token)
    query = f"{ids_param}"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)
    return json_result
