"""
Purpose of this file is to connect to the league
and providing variables for certain web pages
"""

from oauth import sc
import yahoo_fantasy_api as yfa 

# Set it to NBA fantasy league
gm = yfa.Game(sc, 'nba')

# Get league ID
leagues = gm.league_ids()
lg = gm.to_league(leagues[0])

"""
Draft Page Variables
    - Set collection name so we can store the info/data to firestore (draft_collection_name)
    - The draft results (draft_res)
"""
draft_collection_name = leagues[0] + '-Draft'
draft_res = lg.draft_results()

"""
Free Agent Page Variables
    - Set collection name so we can store the info/data to firestore (draft_collection_name)
    - The draft results (draft_res)
"""
agent_collection_name = leagues[0] + '-Free_Agent'
positions = ['PG', 'SG', 'SF', 'PF', 'C']

"""
Search Page Variables:
    - Record all players that are taken (taken_players)
    - Record all players id (taken_players_id)
"""
taken_players = lg.taken_players()
taken_players_id = []
for i in taken_players:
    taken_players_id.append(i['player_id'])
