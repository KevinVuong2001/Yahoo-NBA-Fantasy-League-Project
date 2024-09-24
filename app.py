"""
A flask fantasy yahoo nba app where the user could see their fantasy nba league that includes draft board, free agents,
and have the ability to search for a player
"""
import flask
from flask.views import MethodView
from index import Index
from draft import Draft
from free_agent import Free_Agent
from yahoo_oauth import OAuth2
from search import Search
import secrets
import os
from oauth import get_oauth_client

app = flask.Flask(__name__) #Our Flask app
secret_key = secrets.token_hex(16)
app.secret_key = secret_key

oauth_client = get_oauth_client()

@app.route('/login')
def login():
    # Get the authorization URL from the OAuth2 client
    auth_url = oauth_client.authorization_url()

    # Redirect the user to the authorization URL
    return flask.redirect(auth_url)

@app.route('/oauth2callback')
def oauth2callback():
    # Extract the verifier from the callback URL
    verifier = flask.request.args.get('code')

    # Complete the OAuth2 authentication flow with the verifier
    oauth_client.get_access_token(verifier)

    # Redirect the user to the index page or any other page after authentication
    return flask.redirect(flask.url_for('index'))


app.add_url_rule('/', view_func=Index.as_view('index'), methods=["GET"])
app.add_url_rule('/draft', view_func=Draft.as_view('draft'), methods=["GET", "POST"])
app.add_url_rule('/free_agent', view_func=Free_Agent.as_view('free_agent'), methods=["GET", "POST"])
app.add_url_rule('/search', view_func=Search.as_view('search'), methods=["GET", "POST"])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

