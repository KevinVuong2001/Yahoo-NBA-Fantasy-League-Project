class Model():
    def select_draft(self, collection_name, total_draft):
        """
        Get all entries from the database
        :return: Tuple containing all rows of database
        """
        pass

    def select_agent(self, collection_name, total_agent):
        """
        Get all free agent entries from the database
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

    def insert_agent (self, collection_name, position, players):
        """
        Insert player entry into the free agent database
        :return: none
        :raises: Database errors on connection and insertion
        """

    def if_draft_exist (self, collection_name, expected_count):
        """
        Check if the free agent database exists or not
        """

    def if_free_agent_exist (self, collection_name, requested):
        """
        Check if the free agent database exists
        """
