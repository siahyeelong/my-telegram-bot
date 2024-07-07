import mysql.connector
from keys import SQL_DATABASE_PASSWORD, SQL_DATABASE_NAME, SQL_TABLE_NAME

from logger import setup_logger
logger = setup_logger()

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
        # create the columns: chat_id, chat_count, max_count, TODO: create thread_id column
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {SQL_TABLE_NAME} (
                                chat_id BIGINT NOT NULL PRIMARY KEY,
                                username VARCHAR(255) NOT NULL
                            );""")
        
    def insert_new_chat_id(self, id: int, username: str) -> None:
        '''
        This function checks if the chat id is already in the table. If yes, simply return and do nothing.
        If chat id doesn't exist yet, insert a new record
        '''
        try:
            # Check if the chat_id already exists
            query_check = f"SELECT 1 FROM {SQL_TABLE_NAME} WHERE chat_id = %s"
            self.cursor.execute(query_check, (id,))
            exists = self.cursor.fetchone()

            if exists:
                logger.info(f"chat_id {id} already exists. Skipping insert.")
                return

            # If the chat_id does not exist, insert it
            query_insert = f"INSERT INTO {SQL_TABLE_NAME} (chat_id, username) VALUES (%s, %s)"
            
            values = (id, username)
            self.cursor.execute(query_insert, values)
            
            self.db.commit()
            logger.info(f"Inserted chat_id {id}, username {username}.")
            
        except mysql.connector.Error as err:
            logger.error(f"Error: {err}")
            self.db.rollback()
            
    def get_all_records(self) -> list:
        # Define the query to fetch all records from the table
        query = f"SELECT chat_id, username FROM {SQL_TABLE_NAME}"
        
        # Execute the query
        self.cursor.execute(query)
        
        # Fetch all results
        return self.cursor.fetchall()
    
    def delete_record(self, id: int) -> None:
        '''
        This function deletes a record based on the chat id.
        '''
        try:
            query_delete = f"DELETE FROM {SQL_TABLE_NAME} WHERE chat_id = %s"
            self.cursor.execute(query_delete, (id,))
            self.db.commit()
            logger.info(f"Deleted chat_id {id}.")
        except mysql.connector.Error as err:
            logger.error(f"Error: {err}")
            self.db.rollback()
    
    def close(self):
        '''Close the cursor and the database connection.'''
        if self.cursor:
            self.cursor.close()
        if self.db:
            self.db.close()
    
    def __enter__(self):
        '''Enter the runtime context related to this object.'''
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        '''Exit the runtime context related to this object.'''
        self.close()
    
    def __del__(self):
        '''Destructor to ensure resources are released when the instance is deleted.'''
        self.close()