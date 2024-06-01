from flask import render_template, redirect, url_for, redirect
from flask.views import MethodView
from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa 
import gbmodel

class Draft(MethodView):
    def get(self):
        model = gbmodel.get_model()
        # Connect to Yahoo API
        sc = OAuth2(None, None, from_file='oauth2.json')
        gm = yfa.Game(sc, 'nba')
        # Get league ID
        leagues = gm.league_ids()
        lg = gm.to_league(leagues[0])
        collection_name = leagues[0] + '-Draft'
        draft_res = lg.draft_results()

        entries = model.select_draft(collection_name, len(draft_res))

        return render_template('draft.html', draft_board=entries)
    
    def post(self):
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

        model = gbmodel.get_model()
        collection_name = leagues[0] + '-Draft'
        expected_count = 13;

        if not model.if_draft_exist(collection_name, expected_count):
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
            for round_number, picks in picks_by_round.items():
                print(f"Round: {round_number}")
                model.insert_draft(collection_name, round_number, picks)
        return redirect(url_for('draft'))

