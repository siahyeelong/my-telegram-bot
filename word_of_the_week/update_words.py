from mongodb_backend import Database


if __name__ == "__main__":
    DB = Database()
    # ------ Inserting a new word template -------
    # new_word = {
    #     "word": "xxx",
    #     "definition": "xxx",
    #     "sentence1": "xxx",
    #     "sentence2": "xxx",
    #     "sentence3": "xxx",
    #     "used": False,
    # }
    # DB.collection.insert_one(new_word)

    # ------ Loading csv words into db -------
    import pandas

    words = pandas.read_csv("./words.csv")
    data = []
    for word in words.iterrows():
        line = {
            "word": word[1]["word"],
            "definition": word[1]["definition"],
            "sentence1": word[1]["example use in a sentence 1"],
            "sentence2": word[1]["example use in a sentence 2"],
            "sentence3": word[1]["example use in a sentence 3"],
            "used": word[1]["used"] == "yes",
        }
        data.append(line)

    DB.words.insert_many(data)
