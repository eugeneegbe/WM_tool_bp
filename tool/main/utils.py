import sys
import requests
import traceback
from tool import db
from requests_oauthlib import OAuth1

def is_commit_successfull():
    '''
    Test for the success of a database commit operation.

    '''
    try:
        db.session.commit()
        return True
    except Exception:
        # TODO: We could add a try catch here for the error
        print('Exception when committing to database.', file=sys.stderr)
        traceback.print_stack()
        traceback.print_exc()
        db.session.rollback()
        # for resetting non-commited .add()
        db.session.flush()
    return False


def generate_csrf_token(url, app_key, app_secret, user_key, user_secret):
    '''
    Generate CSRF token for edit request

    Keyword arguments:
    app_key -- The application api auth key
    app_secret -- The application api auth secret
    user_key -- User auth key generated at login
    user_secret -- User secret generated at login
    '''
    # We authenticate the user using the keys
    auth = OAuth1(app_key, app_secret, user_key, user_secret)

    # Get token
    token_request = requests.get(url, params={
        'action': 'query',
        'meta': 'tokens',
        'format': 'json',
    }, auth=auth)
    token_request.raise_for_status()

    # We get the CSRF token from the result to be used in editing
    CSRF_TOKEN = token_request.json()['query']['tokens']['csrftoken']
    return CSRF_TOKEN, auth
