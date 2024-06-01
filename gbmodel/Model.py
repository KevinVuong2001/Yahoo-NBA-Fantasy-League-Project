class Model():
    def select_draft(self, collection_name, total_draft):
        """
        Get all entries from the database
        :return: Tuple containing all rows of database
        """
        pass

    def insert_draft (self, collection_name, round, picks):
        """
        Inserts entry into the database
        :return: none
        :raises: Database errors on connection and insertion
        """
        pass

    def if_draft_exist (self, collection_name):
        """
        Check if the database exists or not
        """
