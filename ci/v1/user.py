"""
Python  API for the user service.
"""

# Standard library modules

# Installed packages
import requests


class User():
    """Python API for the user service.

    Handles the details of formatting HTTP requests and decoding
    the results.

    Parameters
    ----------
    url: string
        The URL for accessing the user service. Often
        'http://cmpt756s1:30000/'. Note the trailing slash.
    auth: string
        Authorization code to pass to the user service. For many
        implementations, the code is required but its content is
        ignored.
    """
    def __init__(self, url, auth):
        self._url = url
        self._auth = auth

    def update_user(self, u_id, fname, lname, email):
        r = requests.put(
            self._url + u_id,
            json={'fname': fname,
                  'lname': lname,
                  'email': email},
            headers={'Authorization': self._auth}
        )
        return r.status_code

    def create_user(self, fname, lname, email):
        """
        Create a user.
        If a record already exists with the same fname, lname, and email,
        the old UUID is replaced with a new one.
        """
        r = requests.post(
            self._url,
            json={'fname': fname,
                  'lname': lname,
                  'email': email},
            headers={'Authorization': self._auth}
        )
        return r.status_code, r.json()['user_id']

    def delete_user(self, u_id):
        r = requests.delete(
            self._url + u_id,
            headers={'Authorization': self._auth}
        )
        return r.status_code

    def get_user(self, u_id):
        r = requests.get(
            self._url + u_id,
            headers={'Authorization': self._auth}
            )
        if r.status_code != 200:
            return r.status_code, None, None, None

        item = r.json()['Items'][0]
        return r.status_code, item['fname'], item['lname'], item['email']

    def login(self, u_id):
        r = requests.get(
            self._url + u_id,
            headers={'Authorization': self._auth}
            )
        return r.status_code

    def logoff(self):
        return 200
