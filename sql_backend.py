import mysql.connector
from keys import SQL_DATABASE_PASSWORD, SQL_DATABASE_NAME, SQL_TABLE_NAME

class SQL_Database:
    def __init__(self) -> None:
        # connect to mysql server
        self.db = mysql.connector.connect(
            host='localhost', 
            user='root', 
            password=SQL_DATABASE_PASSWORD,
        )
        self.cursor = self.db.cursor()
        # create the database if it doesnt alr exist
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {SQL_DATABASE_NAME}")
        self.db.commit()
        # re-connect
        self.db = mysql.connector.connect(
            host='localhost', 
            user='root', 
            password=SQL_DATABASE_PASSWORD,
            database=SQL_DATABASE_NAME
        )
        self.cursor = self.db.cursor()
        # create the columns: chat_id, chat_count, max_count
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {SQL_TABLE_NAME} (
                                chat_id BIGINT NOT NULL PRIMARY KEY,  -- Assuming chat IDs are large integers
                                chat_count INT NOT NULL CHECK (chat_count <= 1024),
                                max_count INT NOT NULL DEFAULT 1024 CHECK (max_count <= 1024)
                            );""")
        
    def insert_new_chat_id(self, id: int) -> None:
        '''
        This function inserts a new id into the chat_id column and initializes the 
        chat_count to 0 and max_count to 10
        '''
        try:
            query = f"INSERT IGNORE INTO {SQL_TABLE_NAME} (chat_id, chat_count, max_count) VALUES (%s, %s, %s)"
            values = (id, 0, 10)
            self.cursor.execute(query, values)
            self.db.commit()
        except mysql.connector.Error as err:
            print(f"Maybe not Error: {err}\nOr user id could have already existed")
            self.db.rollback()

    def increment_chat_count(self, id: int) -> None:
        '''
        This function increments the chat_count by 1 for the corresponding chat_id
        '''
        try:
            query = f"UPDATE {SQL_TABLE_NAME} SET chat_count = chat_count + 1 WHERE chat_id = %s"
            values = (id,)
            self.cursor.execute(query, values)
            self.db.commit()
            print(f"Incremented chat_count for chat_id {id}.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.db.rollback()

    def get_chat_count(self, id: int) -> int:
        '''
        This function returns the chat_count for the corresponding chat_id
        '''
        try:
            query = f"SELECT chat_count FROM {SQL_TABLE_NAME} WHERE chat_id = %s"
            values = (id,)
            self.cursor.execute(query, values)
            result = self.cursor.fetchone()
            if result:
                return result[0]
            else:
                print(f"No entry found for chat_id {id}.")
                return 0
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return 0
        
    def get_chat_and_max_count(self, id: int) -> tuple:
        '''
        This function returns both chat_count and max_count for the corresponding chat_id
        '''
        try:
            query = f"SELECT chat_count, max_count FROM {SQL_TABLE_NAME} WHERE chat_id = %s"
            values = (id,)
            self.cursor.execute(query, values)
            result = self.cursor.fetchone()
            if result:
                return result
            else:
                print(f"No entry found for chat_id {id}.")
                return (0, 0)
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return (0, 0)