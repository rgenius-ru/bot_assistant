from pymongo import MongoClient
import os


def connect(db_name):
    login = os.getenv('mongo_login')
    password = os.getenv('mongo_pass')
    # print(login, password)

    uri = f"mongodb+srv://{login}:{password}" \
          "@cluster0.2ootn.mongodb.net/" \
          "myFirstDatabase" \
          "?retryWrites=true" \
          "&w=majority"
    connection_mongo = MongoClient(uri)
    db = connection_mongo[db_name]

    return db


def load_failure_phrases():
    python_help_db = connect('python_help')
    # print('Список доступных баз данных:', *connection_mongo.list_database_names(), sep='\n')
    failure_phrases_collection = python_help_db['failure_phrases']
    some_phrases = failure_phrases_collection.find_one()

    if isinstance(some_phrases, dict):
        return some_phrases.get('phrases')

    return None


def save_intents():
    file = open('Intents/intents.txt', 'r', encoding='utf-8')  # Отрытие файла в режиме чтения
    text = file.read()  # Чтение данных из файла
    file.close()  # Закрытие файла

    text = text.split('\n')  # Разделение текста и преобразование его в список строк

