"""
SFU CMPT 756
Loader for sample database
"""

# Standard library modules
import csv
from json.encoder import py_encode_basestring
import os
import time

# Installed packages
import requests

# The application

loader_token = os.getenv('SVC_LOADER_TOKEN')

# Enough time for Envoy proxy to initialize
# This is only needed if the loader is run with
# Istio injection.  `cluster/loader-tpl.yaml`
# sets that value.
INITIAL_WAIT_SEC = 1

db = {
    "name": "http://cmpt756db:30002/api/v1/datastore",
}


def build_auth():
    """Return a loader Authorization header in Basic format"""
    global loader_token
    return requests.auth.HTTPBasicAuth('svc-loader', loader_token)


def create_user(user_id, email, fname, lname, playlist):
    """
    Create a user.
    If a record already exists with the same fname, lname, and email,
    the old UUID is replaced with this one.
    """
    url = db['name'] + '/load'
    response = requests.post(
        url,
        auth=build_auth(),
        json={"objtype": "user",
              "lname": lname,
              "email": email,
              "fname": fname,
              "uuid": user_id,
              "playlist": playlist})
    print(response)
    return (response.json())


def create_song(artist, title, uuid):
    """
    Create a song.
    If a record already exists with the same artist and title,
    the old UUID is replaced with this one.
    """
    url = db['name'] + '/load'
    response = requests.post(
        url,
        auth=build_auth(),
        json={"objtype": "music",
              "Artist": artist,
              "SongTitle": title,
              "uuid": uuid})
    return (response.json())


def create_playlist(playlist_id, songs, title):
    """
    Create a song.
    If a record already exists with the same artist and title,
    the old UUID is replaced with this one.
    """
    url = db['name'] + '/load'
    response = requests.post(
        url,
        auth=build_auth(),
        json={"objtype": "playlist",
              "uuid": playlist_id,
              "songs": songs,
              "title": title})
    return (response.json())


def check_resp(resp, key):
    if 'http_status_code' in resp:
        return None
    else:
        return resp[key]


if __name__ == '__main__':
    # Give Istio proxy time to initialize
    time.sleep(INITIAL_WAIT_SEC)

    resource_dir = '/data'

    with open('{}/users/users.csv'.format(resource_dir), 'r') as inp:
        rdr = csv.reader(inp)
        next(rdr)  # Skip header
        for user_id, email, fname, lname, playlist in rdr:
            resp = create_user(user_id.strip(),
                               email.strip(),
                               fname.strip(),
                               lname.strip(),
                               playlist.strip())
            resp = check_resp(resp, 'user_id')
            if resp is None or resp != user_id:
                print('Error creating user {} {} ({}), {}, {}'.format(user_id,
                                                                  email,
                                                                  fname,
                                                                  lname,
                                                                  playlist))

    with open('{}/music/music.csv'.format(resource_dir), 'r') as inp:
        rdr = csv.reader(inp)
        next(rdr)  # Skip header
        for uuid, artist, title, in rdr:
            resp = create_song(artist.strip(),
                               title.strip(),
                               uuid.strip())
                               
            resp = check_resp(resp, 'music_id')
            if resp is None or resp != uuid:
                print('Error creating song {} {}, {}'.format(artist,
                                                             title,
                                                             uuid))

    with open('{}/playlist/playlist.csv'.format(resource_dir), 'r') as inp:
        rdr = csv.reader(inp)
        next(rdr)  # Skip header
        for uuid, songs, title in rdr:
            resp = create_playlist(uuid.strip(),
                                   songs.strip(),
                                   title.strip())
            resp = check_resp(resp, 'playlist_id')
            if resp is None or resp != uuid:
                print('Error creating playlist {} {}, {}'.format(playlist_id,
                                                                songs,
                                                                title))
