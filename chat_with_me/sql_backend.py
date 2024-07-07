import mysql.connector
from keys import SQL_DATABASE_PASSWORD, SQL_DATABASE_NAME, SQL_TABLE_NAME
from chatgpt_assistant import GPT_assistant

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
                                chat_id BIGINT NOT NULL PRIMARY KEY,  -- Assuming chat IDs are large integers
                                chat_count INT NOT NULL CHECK (chat_count <= 1024),
                                max_count INT NOT NULL DEFAULT 1024 CHECK (max_count <= 1024),
                                thread_id VARCHAR(255) NOT NULL
                            );""")
        
    def insert_new_chat_id(self, id: int) -> None:
        '''
        This function checks if the chat id is already in the table. If yes, simply return and do nothing.
        If chat id doesn't exist yet, insert a new id into the chat_id column and initializes the 
        chat_count to 0 and max_count to 10, and thread_id to whatever that was generated.
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
            query_insert = f"INSERT INTO {SQL_TABLE_NAME} (chat_id, chat_count, max_count, thread_id) VALUES (%s, %s, %s, %s)"
            
            # Generate the threadID here
            assistant = GPT_assistant()
            threadID = assistant.create_new_thread()
            values = (id, 0, 10, threadID)
            self.cursor.execute(query_insert, values)
            
            self.db.commit()
            logger.info(f"Inserted chat_id {id} with chat_count 0, max_count 10, and thread_id {threadID}.")
        except mysql.connector.Error as err:
            logger.error(f"Error: {err}")
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
            logger.info(f"Incremented chat_count for chat_id {id}.")
        except mysql.connector.Error as err:
            logger.error(f"Error: {err}")
            self.db.rollback()

    def get_chat_count(self, id: int) -> int:
        '''
        [NOT USED]
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
                logger.debug(f"No entry found for chat_id {id}.")
                return 0
        except mysql.connector.Error as err:
            logger.error(f"Error: {err}")
            return 0
        
    def get_row(self, id: int) -> tuple:
        '''
        This function returns the row of data according to the chat_id
        '''
        try:
            query = f"SELECT chat_count, max_count, thread_id FROM {SQL_TABLE_NAME} WHERE chat_id = %s"
            values = (id,)
            self.cursor.execute(query, values)
            result = self.cursor.fetchone()
            if result:
                return result
            else:
                logger.debug(f"No entry found for chat_id {id}.")
                return (0, 0, 0)
        except mysql.connector.Error as err:
            logger.error(f"Error: {err}")
            return (0, 0, 0)
        
    def reset_chat_count(self, id: int) -> None:
        '''
        This function resets the chat_count and thread_ID for a specified chat_id
        '''
        try:
            query = f"UPDATE {SQL_TABLE_NAME} SET chat_count = 0, thread_id = %s WHERE chat_id = %s"
            assistant = GPT_assistant()
            values = (assistant.create_new_thread(),id)
            self.cursor.execute(query, values)
            self.db.commit()
            logger.info(f"Resetted chat_count for chat_id {id}.")
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