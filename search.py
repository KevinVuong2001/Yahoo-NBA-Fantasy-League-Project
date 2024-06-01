from flask import render_template, redirect, url_for, redirect, request, session
from flask.views import MethodView
from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa 
import gbmodel

# Connect to Yahoo API
sc = OAuth2(None, None, from_file='oauth2.json')
gm = yfa.Game(sc, 'nba')
# Get league ID
leagues = gm.league_ids()
lg = gm.to_league(leagues[0])

class Search(MethodView):
    def get(self):
        requested_player = session.get('requested_player')
        results = lg.player_details(requested_player)
        search_result = {}
        for r in results:
            player_id = r['player_id']
            player_name = r['name']['full']
            team = r['editorial_team_abbr']
            primary_position = r['primary_position']
            eligible = r['eligible_positions']
            eligible_position = [pos['position'] for pos in eligible] # Get a list of eligible position
            image_url = r['headshot']['url']
            print (player_name, player_id)
            # Get their stats
            try:
                player_stats = lg.player_stats([player_id], 'average_season')
                points = player_stats[0]['PTS']
                rebounds = player_stats[0]['REB']
                assists = player_stats[0]['AST']
                fg = player_stats[0]['FG%']
                ft = player_stats[0]['FT%']
                threes_made = player_stats[0]['3PTM']
                steals = player_stats[0]['ST']
                blocks = player_stats[0]['BLK']
                turnovers = player_stats[0]['TO']
            except:
                continue
                points, rebounds, assists, fg, ft, threes_made, steals, blocks, turnovers = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
            
            search_result[player_name] = {
                'name': player_stats[0]['name'],
                    'primary_position': primary_position,
                    'eligible_position': eligible_position,
                    'PTS': points,
                    'REB': rebounds,
                    'AST': assists,
                    'FG': fg,
                    'FT': ft,
                    '3PTM': threes_made,
                    'ST': steals,
                    'BLK': blocks,
                    'TO': turnovers,
            }
            # Get percent owned and if player is taken
            try:
                percent_data = lg.percent_owned([player_id])
                percent_own = percent_data[0]['percent_owned']
            except:
                continue
                percent_owned = 0
            search_result[player_name]['percent_own'] = percent_own
        sorted_search_result = dict(sorted(search_result.items(), key=lambda item: item[1].get('percent_own', 0), reverse=True))
        return render_template('search.html', results=sorted_search_result)
    
    def post(self):
        requested_player = request.form['query']
        session['requested_player'] = requested_player
        return redirect(url_for('search'))
