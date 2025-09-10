from keys import (
    MONGODB_URI,
    MONGODB_DATABASE,
    MONGODB_WOTW_USERS_COLLECTION,
    MONGODB_WORDS_COLLECTION,
)
from pymongo import MongoClient


class Database:
    def __init__(self):
        self.db = self.get_database()
        self.users = self.db[MONGODB_WOTW_USERS_COLLECTION]
        self.words = self.db[MONGODB_WORDS_COLLECTION]

        # Upon initialisation, get the latest word
        self.wotw = self.words.find_one({"used": True}, sort=[("_id", -1)])

    def get_database(self):

        # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
        client = MongoClient(MONGODB_URI)

        # Create the database for our example (we will use the same database throughout the tutorial
        return client[MONGODB_DATABASE]

    def get_word(self):
        # Get a word, then update 'used' parameter to true
        self.wotw = self.words.find_one_and_update(
            {"used": False}, {"$set": {"used": True}}
        )
        # Return word
        return self.wotw

    def add_user(self, username, chatID):
        # Check if user exists. If exists, input chat id
        if (
            self.users.find_one_and_update(
                {"username": username}, {"$set": {"chatid": chatID}}
            )
            is None
        ):
            # Otherwise, add a user
            self.users.insert_one({"username": username, "chatid": chatID})
        # Return this week's word
        return self.wotw

    def remove_user(self, chatID):
        # Find and remove user
        self.users.find_one_and_update({"chatid": chatID}, {"$set": {"chatid": ""}})
        return


# Test
if __name__ == "__main__":
    db = Database()
    print(db.users.find_one({"username": "yeelong"}))
