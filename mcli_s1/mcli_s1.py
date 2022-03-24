"""
Simple command-line interface to user service
"""

# Standard library modules
import argparse
import cmd
import re

# Installed packages
import requests

# The services check only that we pass an authorization,
# not whether it's valid
DEFAULT_AUTH = 'Bearer A'


def parse_args():
    argp = argparse.ArgumentParser(
        'mcli',
        description='Command-line query interface to user service'
        )
    argp.add_argument(
        'name',
        help="DNS name or IP address of user server"
        )
    argp.add_argument(
        'port',
        type=int,
        help="Port number of user server"
        )
    return argp.parse_args()


def get_url(name, port):
    return "http://{}:{}/api/v1/user/".format(name, port)


class Mcli(cmd.Cmd):
    def __init__(self, args):
        self.name = args.name
        self.port = args.port
        cmd.Cmd.__init__(self)
        self.prompt = 'mql: '
        self.intro = """
Command-line interface to music service.
Enter 'help' for command list.
'Tab' character autocompletes commands.
"""

    def do_createUser(self, arg):
        """
        Add a user to the database.

        Parameters
        ----------
        Last Name - lname : string
        email: string
        First Name - fname : string

        Examples
        --------
        createUser Wright john1977@yahoo.com john
        """
        url = get_url(self.name, self.port)
        args = arg.strip().split(' ')
        payload = {
            'lname': args[0],
            'email': args[1],
            'fname': args[2]
        }
        r = requests.post(
            url,
            json=payload,
            headers={'Authorization': DEFAULT_AUTH}
        )
        result = r.json()
        print("User ID : {}".format(result['user_id']))

    def do_updateUser(self, arg):
        """
        Update the user detials in the database.

        Parameters
        ----------
        userid - uid : string
        Last Name - lname : string
        email: string
        First Name - fname : string

        Examples
        --------
        updateUser 6ecfafd0-8a35-4af6-a9e2-cbd79b3abeea Wright john1977@yahoo.com john
        """
        url = get_url(self.name, self.port)
        args = arg.strip().split(' ')
        payload = {
            'lname': args[1],
            'email': args[2],
            'fname': args[3]
        }
        r = requests.put(
            url+args[0],
            json=payload,
            headers={'Authorization': DEFAULT_AUTH}
            )
        if r.status_code != 200:
            print("Non-successful status code:", r.status_code)
        else:
            print('User information updated')

    def do_deleteUser(self, arg):
        """
        Delete a user.

        Parameters
        ----------
        user: user_id
            The user_id of the user to delete.

        Examples
        --------
        deleteUser 6ecfafd0-8a35-4af6-a9e2-cbd79b3abeea
        """
        url = get_url(self.name, self.port)
        r = requests.delete(
            url+arg.strip(),
            headers={'Authorization': DEFAULT_AUTH}
            )
        if r.status_code != 200:
            print("Non-successful status code:", r.status_code)

    def do_getUser(self, arg):
        """
        Read the user.

        Parameters
        ----------
        user:  user_id 
            The user_id of the user to read. 

        Examples
        --------
        getUser 6ecfafd0-8a35-4af6-a9e2-cbd79b3abeea
        """
 
        url = get_url(self.name, self.port)
        r = requests.get(
            url+arg.strip(),
            headers={'Authorization': DEFAULT_AUTH}
            )
        if r.status_code != 200:
            print("Non-successful status code:", r.status_code)
        items = r.json()
        if 'Count' not in items:
            print("0 items returned")
            return
        print("{} items returned".format(items['Count']))
        for i in items['Items']:
            print("{}  {:20.20s} {}".format(
                i['email'],
                i['fname'],
                i['lname']))

    def do_login(self, arg):
        """
        Login to user service

        Parameters
        ----------
        user:  user_id 
            The user_id of the user. 

        Examples
        --------
        login 6ecfafd0-8a35-4af6-a9e2-cbd79b3abeea
        """
        url = get_url(self.name, self.port)
        payload = {'uid' : arg.strip()}
        r = requests.put(
            url+'login',
            json=payload,
            headers={'Authorization': DEFAULT_AUTH}
            )
        print(r)
        #if r.status_code != 200:
        #    print("Non-successful status code: {}. Login Failed".format(r.status_code))
        #else:
        #    print('Login Successful')
    

    def do_logoff(self, arg):
        """
        Logoff from user service

        Parameters
        ----------
        None

        Examples
        --------
        logoff
        """
        url = get_url(self.name, self.port)
        payload = {'jwt' : 'logoff'}
        r = requests.get(
            url+'logoff',
            json=payload,
            headers={'Authorization': DEFAULT_AUTH}
            )
        if r.status_code != 200:
            print("Non-successful status code: {}. Logout Failed".format(r.status_code))
        else:
            print('Logout Succesful')
    
    def do_quit(self, arg):
        """
        Quit the program.
        """
        return True

if __name__ == '__main__':
    args = parse_args()
    Mcli(args).cmdloop()



#def parse_quoted_strings(arg):
#    """
#    Parse a line that includes words and '-, and "-quoted strings.
#    This is a simple parser that can be easily thrown off by odd
#    arguments, such as entries with mismatched quotes.  It's good
#    enough for simple use, parsing "-quoted names with apostrophes.
    """
    mre = re.compile(r'''(\w+)|'([^']*)'|"([^"]*)"''')
    args = mre.findall(arg)
    return [''.join(a) for a in args]
    """