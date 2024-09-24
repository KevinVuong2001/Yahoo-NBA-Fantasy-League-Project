"""
This part of the code handles the authorization
"""
from yahoo_oauth import OAuth2
import os

# Retrieve OAuth2 credentials from environment variables
consumer_key = os.environ.get('YAHOO_CONSUMER_KEY')
consumer_secret = os.environ.get('YAHOO_CONSUMER_SECRET')

# Initialize OAuth2 with consumer key, consumer secret, and redirect URI
sc = OAuth2(consumer_key, consumer_secret, access_token=None, refresh_token=None)
