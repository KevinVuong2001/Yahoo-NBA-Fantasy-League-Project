"""
A flask fantasy nba app where the user could see their fantasy nba league that includes draft board, free agents, and waivers
"""
import flask
from flask.views import MethodView
from index import Index
from draft import Draft
from free_agent import Free_Agent
from search import Search
import secrets

app = flask.Flask(__name__) #Our Flask app
secret_key = secrets.token_hex(16)
app.secret_key = secret_key

app.add_url_rule('/', view_func=Index.as_view('index'), methods=["GET"])
app.add_url_rule('/draft', view_func=Draft.as_view('draft'), methods=["GET", "POST"])
app.add_url_rule('/free_agent', view_func=Free_Agent.as_view('free_agent'), methods=["GET", "POST"])
app.add_url_rule('/search', view_func=Search.as_view('search'), methods=["GET", "POST"])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
