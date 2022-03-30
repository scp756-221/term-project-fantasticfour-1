"""
Integration test of the CMPT 756 sample applicaton.

Result of test in program return code:
0: Test succeeded
1: Test failed
"""

# Standard library modules
import argparse
import os
import sys

# Installed packages
import pytest

# Local modules
import create_tables
import music
import user
import playlist

# The services check only that we pass an authorization,
# not whether it's valid
DUMMY_AUTH = 'Bearer A'


@pytest.fixture
def song(request):
    # Recorded 1956
    return ('Elvis Presley', 'Hound Dog')


def parse_args():
    """Parse the command-line arguments.

    Returns
    -------
    namespace
        A namespace of all the arguments, augmented with names
        'user_url', 'music_url' and 'playlist_url'.
    """
    argp = argparse.ArgumentParser(
        'ci_test',
        description='Integration test of CMPT 756 sample application'
        )
    argp.add_argument(
        'user_address',
        help="DNS name or IP address of user service."
        )
    argp.add_argument(
        'user_port',
        type=int,
        help="Port number of user service."
        )
    argp.add_argument(
        'music_address',
        help="DNS name or IP address of music service."
        )
    argp.add_argument(
        'music_port',
        type=int,
        help="Port number of music service."
        )
    argp.add_argument(
        'playlist_address',
        help="DNS name or IP address of playlist service."
        )
    argp.add_argument(
        'playlist_port',
        type=int,
        help="Port number of playlist service."
        )
    argp.add_argument(
        'table_suffix',
        help="Suffix to add to table names (not including leading "
             "'-').  If suffix is 'scp756-2022', the music table "
             "will be 'Music-scp756-2022'."
    )
    args = argp.parse_args()
    args.user_url = "http://{}:{}/api/v1/user/".format(
        args.user_address, args.user_port)
    args.music_url = "http://{}:{}/api/v1/music/".format(
        args.music_address, args.music_port)
    args.playlist_url = "http://{}:{}/api/v1/playlist/".format(
        args.playlist_address, args.playlist_port)
    return args


def get_env_vars(args):
    """Augment the arguments with environment variable values.

    Parameters
    ----------
    args: namespace
        The command-line argument values.

    Environment variables
    ---------------------
    AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY,
        SVC_LOADER_TOKEN, DYNAMODB_URL: string
        Environment variables specifying these AWS access parameters.

    Modifies
    -------
    args
        The args namespace augmented with the following names:
        dynamodb_region, access_key_id, secret_access_key, loader_token,
        dynamodb_url

        These names contain the string values passed in the corresponding
        environment variables.

    Returns
    -------
    Nothing
    """
    # These are required to be present
    args.dynamodb_region = os.getenv('AWS_REGION')
    args.access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    args.secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    args.loader_token = os.getenv('SVC_LOADER_TOKEN')
    args.dynamodb_url = os.getenv('DYNAMODB_URL')


def setup(args):
    """Create the DynamoDB tables.

    Parameters
    ----------
    args: namespace
        The arguments specifying the tables. Uses dynamodb_url,
        dynamodb_region, access_key_id, secret_access_key, table_suffix.
    """
    create_tables.create_tables(
        args.dynamodb_url,
        args.dynamodb_region,
        args.access_key_id,
        args.secret_access_key,
        'Music-' + args.table_suffix,
        'User-' + args.table_suffix,
        'PlayList-' + args.table_suffix
    )


def run_test(args):
    """Run the tests.

    Parameters
    ----------
    args: namespace
        The arguments for the test.

    Prerequisites
    -------------
    The DyamoDB tables must already exist.

    Returns
    -------
    number
        An HTTP status code representing the test result.
        Some "pseudo-HTTP" codes are defined in the 600 range
        to indicate conditions that are not included in the HTTP
        specification.

    Notes
    -----
    This test is highly incomplete and needs substantial extension.
    """
    mserv = music.Music(args.music_url, DUMMY_AUTH)
    artist, song = ('Mary Chapin Carpenter', 'John Doe No. 24')
    trc, m_id = mserv.create_song(artist, song)
    assert trc == 200
    trc, ra, rs = mserv.read_song(m_id)
    assert (trc == 200 and artist == ra and song == rs)
    trc = mserv.delete_song(m_id)
    assert trc == 200

    userv = user.User(args.user_url, DUMMY_AUTH)
    fname, lname, email = ('Mohamadreza', 'Dokhah', 'mda85@sfu.ca')
    trc, u_id = userv.create_user(fname, lname, email)
    assert trc == 200
    trc, rf, rl, re = userv.get_user(u_id)
    assert (trc == 200 and fname == rf and lname == rl and email == re)
    fname, lname, email = ('Mohammadreza', 'Dorkhah', 'mda84@sfu.ca')
    trc = userv.update_user(u_id, fname, lname, email)
    assert (trc == 200)
    trc, rf, rl, re = userv.get_user(u_id)
    assert (trc == 200 and fname == rf and lname == rl and email == re)
    trc = userv.delete_user(u_id)
    assert trc == 200
    trc = userv.login(u_id)
    assert trc == 200
    trc = userv.logoff()
    assert trc == 200

    pserv = playlist.PlayList(args.playlist_url, DUMMY_AUTH)
    title = 'My Favourites'
    trc, p_id = pserv.create_playlist(title, u_id)
    assert trc == 200
    trc, rt, rs = pserv.get_playlist(p_id)
    assert (trc == 200 and title == rt and [] == rs)
    trc, m_id = mserv.create_song(artist, song)
    assert trc == 200
    trc = pserv.add_song_to_playlist(p_id, m_id)
    assert trc == 200
    trc, rt, rs = pserv.get_playlist(p_id)
    assert (trc == 200 and title == rt and [m_id] == rs)
    trc = pserv.remove_song_from_playlist(p_id, m_id)
    assert trc == 200
    trc = pserv.delete_playlist(p_id)
    assert trc == 200

    return trc


if __name__ == '__main__':
    args = parse_args()
    get_env_vars(args)
    setup(args)
    trc = run_test(args)
    if trc != 200:
        sys.exit(1)
