"""
Python  API for the music service.
"""

# Standard library modules

# Installed packages
import requests
# import logging
# import pytest


# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger()


class Playlist():
    """Python API for the playlist service.

    Handles the details of formatting HTTP requests and decoding
    the results.

    Parameters
    ----------
    url: string
        The URL for accessing the playlist service. Often
        'http://cmpt756s3:30004/'. Note the trailing slash.
    auth: string
        Authorization code to pass to the playlist service. For many
        implementations, the code is required but its content is
        ignored.
    """

    def __init__(self, url, auth):
        self._url = url
        self._auth = auth

    def test_create_playlist(self, title, u_id):
        r = requests.post(
            self._url,
            json={'title': title,
                  'user_id': u_id,
                  'songs': []},
            headers={'Authorization': self._auth}
        )
        # print(r.json())
        return r.status_code, r.json()['playlist_id']

    def get_playlist(self, p_id):
        r = requests.get(
            self._url + p_id,
            headers={'Authorization': self._auth}
        )
        if r.status_code != 200:
            return r.status_code, None, None

        item = r.json()['Items'][0]
        return r.status_code, item['title'], item['songs']

    def delete_playlist(self, p_id, u_id):
        r = requests.delete(
            self._url + p_id,
            json={'user_id': u_id},
            headers={'Authorization': self._auth}
        )
        return r.status_code

    def add_song_to_playlist(self, p_id, m_id):
        r = requests.get(
            self._url + p_id,
            headers={'Authorization': self._auth}
        )
        if r.status_code != 200:
            return r.status_code

        item = r.json()['Items'][0]
        # logger.info("Song List: " + str(item['songs']))
        item['songs'].append(m_id)
        # logger.info("Song List: " + str(item['songs']))

        r = requests.put(
            self._url + p_id,
            json={'title': item['title'],
                  'music_id': item['songs']},
            headers={'Authorization': self._auth}
        )
        # logger.info("Response: " + str(r.json()))
        return r.status_code

    def remove_song_from_playlist(self, p_id, m_id):
        r = requests.get(
            self._url + p_id,
            headers={'Authorization': self._auth}
        )
        if r.status_code != 200:
            return r.status_code

        item = r.json()['Items'][0]
        # logger.info("Songs: " + str(item['songs']))
        item['songs'][0].remove(m_id)

        r = requests.put(
            self._url + p_id,
            json={'title': item['title'],
                  'songs': item['songs']},
            headers={'Authorization': self._auth}
        )
        return r.status_code
