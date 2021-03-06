"""
SFU CMPT 756
Sample application---playlist service.
"""

# Standard library modules
import logging
# import os
import sys

# Installed packages
from flask import Blueprint
from flask import Flask
from flask import request
from flask import Response

from prometheus_flask_exporter import PrometheusMetrics

import requests

import simplejson as json

# The application

app = Flask(__name__)

metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Playlist process')

db = {
    "name": "http://cmpt756db:30002/api/v1/datastore",
    "endpoint": [
        "read",
        "write",
        "delete",
        "update"
    ]
}
bp = Blueprint('app', __name__)


@bp.route('/health')
@metrics.do_not_track()
def health():
    return Response("", status=200, mimetype="application/json")


@bp.route('/readiness')
@metrics.do_not_track()
def readiness():
    return Response("", status=200, mimetype="application/json")


@bp.route('/', methods=['POST'])
def create_playlist():
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')
    try:
        content = request.get_json()
        PlaylistTitle = content['title']
        user_id = content['user_id']
        songs = content['songs'] if 'songs' in content else []
    except Exception:
        return json.dumps({"message": "error reading arguments"})

    url = db['name'] + '/' + db['endpoint'][1]
    response = requests.post(
        url,
        json={"objtype": "playlist", "title": PlaylistTitle, "songs": songs},
        headers={'Authorization': headers['Authorization']})

    if response.status_code != 200:
        print("Non-successful status code:", response.status_code)
        return json.dumps({"message": "request not successful"})

    content = response.json()
    playlist_id = content['playlist_id']
    url = db['name'] + '/' + db['endpoint'][0]
    payload = {"objtype": "user", "objkey": user_id}
    response_get = requests.get(
        url,
        payload,
        headers={'Authorization': headers['Authorization']}
    )

    if response_get.status_code != 200:
        print("Non-successful status code:", response_get.status_code)
        return json.dumps({"message": "request not successful"})

    content = response_get.json()
    # print(content)
    playlist = content['Items'][0]['playlist']
    fname = content['Items'][0]['fname']
    lname = content['Items'][0]['lname']
    email = content['Items'][0]['email']
    playlist.append(playlist_id)
    url = db['name'] + '/' + db['endpoint'][3]
    requests.put(
        url,
        params={"objtype": "user", "objkey": user_id},
        json={"lname": lname,
              "email": email,
              "fname": fname,
              "playlist": playlist}
    )

    return (response.json())


@bp.route('/<playlist_id>', methods=['PUT'])
def add_song_to_playlist(playlist_id):
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}), status=401,
                        mimetype='application/json')

    try:
        content = request.get_json()
        title = content['title']
        music_id = content['music_id']
    except Exception:
        return json.dumps({"message": "error reading arguments"})

    payload = {"objtype": "playlist", "objkey": playlist_id}
    url = db['name'] + '/' + db['endpoint'][0]
    response = requests.get(
        url,
        params=payload,
        headers={'Authorization': headers['Authorization']})
    try:
        content = response.json()
        songs = content['Items'][0]['songs']
    except Exception:
        return json.dumps({"message": "error in getting existing song list"})

    songs = list(songs)
    songs.append(music_id)
    url = db['name'] + '/' + db['endpoint'][3]
    response = requests.put(
        url,
        params={"objtype": "playlist", "objkey": playlist_id},
        json={"title": title, "songs": songs})
    return (response.json())


@bp.route('/<playlist_id>/<music_id>', methods=['PUT'])
def remove_song_from_playlist(playlist_id, music_id):
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}), status=401,
                        mimetype='application/json')
    try:
        content = request.get_json()
        title = content['title']
        # music_id = content['music_id']
    except Exception:
        return json.dumps({"message": "error reading arguments"})

    payload = {"objtype": "playlist", "objkey": playlist_id}
    url = db['name'] + '/' + db['endpoint'][0]
    response = requests.get(
        url,
        params=payload,
        headers={'Authorization': headers['Authorization']})
    try:
        content = response.json()
        songs = content['Items'][0]['songs']
    except Exception:
        return json.dumps({"message": "error in getting existing song list"})

    songs = list(songs)
    songs.remove(music_id)
    url = db['name'] + '/' + db['endpoint'][3]
    response = requests.put(
        url,
        params={"objtype": "playlist", "objkey": playlist_id},
        json={"title": title, "songs": songs})
    return (response.json())


@bp.route('/<playlist_id>', methods=['GET'])
def get_playlist(playlist_id):
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')
    payload = {"objtype": "playlist", "objkey": playlist_id}
    url = db['name'] + '/' + db['endpoint'][0]
    response = requests.get(
        url,
        params=payload,
        headers={'Authorization': headers['Authorization']})
    return (response.json())


@bp.route('/<playlist_id>', methods=['DELETE'])
def delete_playlist(playlist_id):
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')
    content = request.get_json()
    user_id = content['user_id']

    url = db['name'] + '/' + db['endpoint'][2]
    response = requests.delete(
        url,
        params={"objtype": "playlist", "objkey": playlist_id},
        headers={'Authorization': headers['Authorization']})

    if response.status_code != 200:
        print("Non-successful status code:", response.status_code)
        return json.dumps({"message": "request not successful"})

    url = db['name'] + '/' + db['endpoint'][0]
    payload = {"objtype": "user", "objkey": user_id}
    response_get = requests.get(
        url,
        payload,
        headers={'Authorization': headers['Authorization']}
    )

    if response_get.status_code != 200:
        print("Non-successful status code:", response_get.status_code)
        return json.dumps({"message": "request not successful"})

    content = response_get.json()
    playlist = content['Items'][0]['playlist']
    fname = content['Items'][0]['fname']
    lname = content['Items'][0]['lname']
    email = content['Items'][0]['email']
    playlist.remove(playlist_id)
    url = db['name'] + '/' + db['endpoint'][3]
    requests.put(
        url,
        params={"objtype": "user", "objkey": user_id},
        json={"lname": lname,
              "email": email,
              "fname": fname,
              "playlist": playlist}
    )

    return (response.json())


# All database calls will have this prefix.  Prometheus metric
# calls will not---they will have route '/metrics'.  This is
# the conventional organization.
app.register_blueprint(bp, url_prefix='/api/v1/playlist/')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        logging.error("missing port arg 1")
        sys.exit(-1)

    # app.logger.error("Unique code: {}".format(ucode))
    p = int(sys.argv[1])
    # Do not set debug=True---that will disable the Prometheus metrics
    app.run(host='0.0.0.0', port=p, threaded=True)
