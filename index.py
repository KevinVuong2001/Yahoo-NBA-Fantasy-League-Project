"""
Homepage:
    - Displays the stats category that the league is using
    - Displays the standings
    - Displays the recent transactions
"""

from flask import render_template
from flask.views import MethodView
from fantasy_data import lg

class Index(MethodView):
    def get(self):
        # Getting the standings portion
        standings = lg.standings()
        team_standings = {}
        for s in standings:
            team_name = s['name']
            regular_rank = s['playoff_seed']
            final_rank = s['rank']
            wins = s['outcome_totals']['wins']
            losses = s['outcome_totals']['losses']
            ties = s['outcome_totals']['ties']
            win_percent = s['outcome_totals']['percentage']
            games_back = s['games_back']
            team_standings[team_name] = {
                'regular_rank': regular_rank,
                'final_rank': final_rank,
                'wins': wins,
                'losses': losses,
                'ties': ties,
                'win_percent': win_percent,
                'games_back': games_back
            }
        # Getting the 5 recent add/drops
        transaction = lg.transactions('add', 5)
        recent_five = []
        for t in transaction:
            player_name = t['players']['0']['player'][0][2]['name']['full']
            position = t['players']['0']['player'][0][4]['display_position']
            status = t['type']
            source = t['players']['0']['player'][1]['transaction_data']
            source_team = ""
            destination_team = ""
            if 'source_type' in source:
                source_team = source['source_team_name']
                destination_team = "Free Agents"
            else:
                source_team = "Free Agents"
                destination_team = source[0]['destination_team_name']
            recent_five.append({
                'name': player_name, 
                'position': position,
                'status': status, 
                'source': source_team, 
                'destination': destination_team})
        return render_template('index.html', standings=team_standings, recent_five=recent_five)

