"""
A flask fantasy nba app where the user could see their fantasy nba league that includes draft board, free agents, and waivers
"""
import flask
from flask.views import MethodView
from index import Index
from draft import Draft

app = flask.Flask(__name__) #Our Flask app

app.add_url_rule('/', view_func=Index.as_view('index'), methods=["GET"])
app.add_url_rule('/draft', view_func=Draft.as_view('draft'), methods=["GET", "POST"])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
