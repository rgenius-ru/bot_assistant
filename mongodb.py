from pymongo import MongoClient
import os


def load_failure_phrases():
    login = os.getenv('mongo_login')
    password = os.getenv('mongo_pass')
    # print(login, password)

    uri = f"mongodb+srv://{login}:{password}" \
          "@cluster0.2ootn.mongodb.net/" \
          "myFirstDatabase" \
          "?retryWrites=true" \
          "&w=majority"
    connection_mongo = MongoClient(uri)

    print('Список доступных баз данных:', *connection_mongo.list_database_names(), sep='\n')

    python_help_db = connection_mongo['python_help']
    failure_phrases_collection = python_help_db['failure_phrases']

    some_phrases = failure_phrases_collection.find_one()

    if isinstance(some_phrases, dict):
        return some_phrases.get('phrases')

    return None
