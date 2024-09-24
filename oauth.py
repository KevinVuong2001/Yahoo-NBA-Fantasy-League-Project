"""
This part of the code handles the authorization
"""
from yahoo_oauth import OAuth2
import os

consumer_key = os.environ.get('YAHOO_CONSUMER_KEY')
consumer_secret = os.environ.get('YAHOO_CONSUMER_SECRET')

# Initialize OAuth2 with consumer key and consumer secret
sc = OAuth2(consumer_key, consumer_secret, access_token=None, refresh_token=None)

def get_oauth_client():
    global sc
    if sc is None or not sc.token_is_valid():
        sc = OAuth2(consumer_key, consumer_secret, os.path.join(os.getcwd(), "oauth2.json"))
        if not sc.token_is_valid():
            # If tokens couldn't be obtained or validated, handle error here
            raise ValueError("Failed to obtain valid OAuth tokens")
    return sc
