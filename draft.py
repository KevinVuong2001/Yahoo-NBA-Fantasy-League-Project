from flask import render_template
from flask.views import MethodView
from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa 

class Draft:
    def get(self):
        # Get player stats
        # Connect to Yahoo API
        sc = OAuth2(None, None, from_file='oauth2.json')
        gm = yfa.Game(sc, 'nba')
        # Get league ID
        leagues = gm.league_ids()
        lg = gm.to_league(leagues[0])

        # Create a dictionary where each key will be the rounds
        picks_by_round = {}
        tms = lg.teams()
        draft_res = lg.draft_results()
        for item in draft_res:
            if item['round'] not in picks_by_round:
                picks_by_round[item['round']] = []
                info = lg.percent_owned([item['player_id']])
                picks_by_round[item['round']].append({
                    'pick': item['pick'],
                    'player': info[0]["name"],
                    'team': tms[item['team_key']]["name"],
                    'percent_own': info[0]["percent_owned"]
                })
        return render_template('draft.html', draft_board=picks_by_round)
