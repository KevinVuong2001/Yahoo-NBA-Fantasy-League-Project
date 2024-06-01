from .Model import Model
from google.cloud import firestore
from collections import OrderedDict

class model(Model):
    def __init__(self):
        self.client = firestore.Client()

    def select_draft(self, collection_name, total_draft):
        rounds = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"]
        draft_board = {}
        for round in rounds:
            doc_ref = self.client.collection(collection_name).document(round)
            doc_snapshot = doc_ref.get()
            data = doc_snapshot.to_dict()
            order_data = {i: data[i] for i in sorted(data, key=lambda x: int(x))}
            draft_board[int(round)] = order_data
        return draft_board

    def insert_draft(self, collection_name, round, picks):
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

    def if_draft_exist (self, collection_name, expected_count):
        collection_ref = self.client.collection(collection_name)
        docs = collection_ref.stream()
        document_count = sum (1 for _ in docs)
        if document_count == expected_count:
            return True
        else:
            return False  
