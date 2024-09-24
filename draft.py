"""
This part of the code handles the draft endpoint
It will consist of displaying the draft board for the league
In addition, it will return information like rounds, picks, players, team selected and percent own
"""

from flask import render_template, redirect, url_for, redirect
from flask.views import MethodView
import gbmodel
from fantasy_data import lg, draft_collection_name, draft_res


class Draft(MethodView):
    def get(self):
        model = gbmodel.get_model()
        entries = model.select_draft(draft_collection_name, len(draft_res))
        return render_template('draft.html', draft_board=entries)
    
    def post(self):
        # Create a dictionary where each key will be the rounds
        picks_by_round = {}
        tms = lg.teams()
        model = gbmodel.get_model()
        expected_count = 13;

        if not model.if_draft_exist(draft_collection_name, expected_count):
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
                model.insert_draft(draft_collection_name, round_number, picks)
        return redirect(url_for('draft'))


