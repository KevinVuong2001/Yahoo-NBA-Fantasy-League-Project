from flask import render_template, redirect, url_for, redirect, request, session
from flask.views import MethodView
import gbmodel
from fantasy_data import lg, agent_collection_name, positions

class Free_Agent(MethodView):
    def get(self):
        requested_position = session.get('requested_position')
        model = gbmodel.get_model()
        entries = []
        if type(requested_position) == list:
            entries = model.select_agent(agent_collection_name, requested_position)
        player_entries = {}
        for entry in entries:
            if entry is not None:
                player_entries = entry['players']
        sorted_player_entries = sorted(player_entries, key=lambda x: x['percent_own'], reverse=True)    
        return render_template('free_agent.html', positions=positions, player_entries=sorted_player_entries, requested=requested_position)
    
    def post(self):
        requested_position = request.form.getlist('position[]')
        model = gbmodel.get_model()
        list_agents = {}
        position_agents_info = {}
        need_data = model.if_free_agent_exist(agent_collection_name, requested_position)
        if len(need_data) > 0: #If there's data that's need to be added to database
            for position in need_data:
                list_agents[position] = lg.free_agents(position) #Get the list of free agents based on position
            # Go through list of free agents each position
            for pos in list_agents:
                for player in list_agents[pos]: # Go through each agent 
                    flag = 1 #success if we can get player's info
                    player_id = player['player_id']
                    try:
                        player_stats = lg.player_stats([player_id], 'average_season')
                    except:
                        continue
                        flag = 0
                    if flag == 1:
                        player_position = lg.player_details([player_id])
                        if position not in position_agents_info:
                            position_agents_info[position] = []
                        position_agents_info[position].append({
                            'name': player_stats[0]['name'],
                            'primary_position': player_position[0]['primary_position'],
                            'eligible_position': player['eligible_positions'],
                            'PTS': player_stats[0]['PTS'],
                            'REB': player_stats[0]['REB'],
                            'AST': player_stats[0]['AST'],
                            'FG': player_stats[0]['FG%'],
                            'FT': player_stats[0]['FT%'],
                            '3PTM': player_stats[0]['3PTM'],
                            'ST': player_stats[0]['ST'],
                            'BLK': player_stats[0]['BLK'],
                            'TO': player_stats[0]['TO'],
                            'percent_own': player['percent_owned']
                        })
                for key, players in position_agents_info.items():
                    print ("Position: ", key)
                    model.insert_agent(agent_collection_name, key, players)
        session['requested_position'] = requested_position
        return redirect(url_for('free_agent'))
