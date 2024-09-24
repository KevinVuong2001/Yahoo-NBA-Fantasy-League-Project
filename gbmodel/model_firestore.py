from .Model import Model
from google.cloud import firestore
from collections import OrderedDict

class model(Model):
    def __init__(self):
        self.client = firestore.Client()

    def select_draft(self, collection_name, total_draft):
        """
        Getting the draft information for all rounds
            - return: list of dictionary
        """
        rounds = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"]
        draft_board = {}
        for round in rounds:
            doc_ref = self.client.collection(collection_name).document(round)
            doc_snapshot = doc_ref.get()
            data = doc_snapshot.to_dict()
            order_data = {i: data[i] for i in sorted(data, key=lambda x: int(x))}
            draft_board[int(round)] = order_data
        return draft_board
    
    def select_agent(self, collection_name, requested):
        """
        Getting the free agents information for a certain position based on user request
            - return: list of dictionary
        """
        data_list = []
        for id in requested:
            agent_ref = self.client.collection(collection_name).document(id)
            doc_snapshot = agent_ref.get()
            data = doc_snapshot.to_dict()
            data_list.append(data)
        return data_list

    def insert_draft(self, collection_name, round, picks):
        """
        Insert an array of players that was selected by a certain round
        The document id is the round (1-13)
        It will insert draft info:
            - pick number
            - player
            - team that selected them
            - percent own
        """
        draft_ref = self.client.collection(collection_name).document(str(round))
        data = {}
        for pick in picks:
            pick_number = pick['pick']
            player = pick['player']
            team = pick['team']
            percent_own = pick['percent_own']
            data[str(pick_number)] = [player, team, percent_own]
            draft_ref.set(data)
        return True

    def insert_agent(self, collection_name, position, players):
        """
        Insert the agent in a document which its id will be the position (PG, SG, SF, PF, C)
        It will insert each player data:
            - name
            - percent own
            - positions (primary and eligible)
            - stats
        """
        agent_ref = self.client.collection(collection_name).document(position)
        player_data = []
        for player in players:
            player_name = player['name']
            primary_position = player['primary_position']
            eligible_position = player['eligible_position']
            points = player['PTS']
            rebound = player['REB']
            assist = player['AST']
            field_goal = player['FG']
            free_throw = player['FT']
            three_point = player['3PTM']
            steal = player['ST']
            block = player['BLK']
            turnover = player['TO']
            percent_own = player['percent_own']
            
            data = {
            'name': player_name,
            'primary_position': primary_position,
            'eligible_position': eligible_position,
            'PTS': points,
            'REB': rebound,
            'AST': assist,
            'FG': field_goal,
            'FT': free_throw,
            '3PTM': three_point,
            'ST': steal,
            'BLK': block,
            'TO': turnover,
            'percent_own': percent_own
            }   
            player_data.append(data)
        agent_ref.set({"players": player_data})
        return True

    def if_draft_exist (self, collection_name, expected_count):
        """
        Check if there's a certain amount of documents
            - used as an indicator if we need to write to Firestore Database or not
            - return True or False
        """
        collection_ref = self.client.collection(collection_name)
        docs = collection_ref.stream()
        document_count = sum (1 for _ in docs)
        if document_count == expected_count:
            return True
        else:
            return False

    def if_free_agent_exist(self, collection_name, requested):
        """
        Check if we have that certain document id (position)
            - Return what positions we need to write into the Firestore Database
        """
        need_data = []
        for id in requested:
            doc_ref = self.client.collection(collection_name).document(id)
            doc = doc_ref.get()
            if doc.exists:
                print ("Data Exist")
            else:
                need_data.append(id)
        return need_data

