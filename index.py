from flask import render_template
from flask.views import MethodView
from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa 

class Index(MethodView):
    def get(self):
        # Get player stats
        # Connect to Yahoo API
        sc = OAuth2(None, None, from_file='oauth2.json')
        gm = yfa.Game(sc, 'nba')
        # Get league ID
        leagues = gm.league_ids(2023)
        lg = gm.to_league(leagues[0])
        player_stats = lg.player_stats([5352], 'average_season')
        player_position = lg.player_details([5352])
        player_stats[0]["position_type"] = player_position[0]['primary_position']
        return render_template('index.html', player_stats=player_stats)
