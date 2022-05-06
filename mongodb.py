from pymongo import MongoClient
import os
from dotenv import load_dotenv


def connect(db_name):
    load_dotenv()
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


def print_collections(db):
    if db is None:
        db = connect('python_help')

    print()
    # print(python_help_db.list_collection_names())
    print('', 'Список коллекций:', *db.list_collection_names(), sep='\n')


def get_intents(limit=None):
    python_help_db = connect('python_help')
    intents_collection = python_help_db['intents']

    if limit:
        intents = intents_collection.find().limit(limit)
    else:
        intents = intents_collection.find()

    return intents


def load_intents_from_file():
    file = open('Intents/intents.txt', 'r', encoding='utf-8')  # Отрытие файла в режиме чтения
    text = file.read()  # Чтение данных из файла
    file.close()  # Закрытие файла

    text = text.split('\n')  # Разделение текста и преобразование его в список строк

    intents = {}
    replica = []
    intent = ''
    start_flag = False
    for string in text:
        if string.startswith('## intent:'):
            if not start_flag:
                replica = []
                index_separator = string.index(':')
                intent = string[index_separator + 1:]
                intents.setdefault(intent)
                start_flag = True
                continue
            else:
                intents.update({intent: replica})
                start_flag = False

        if start_flag and string != '' and not string.startswith('# '):
            replica.append(string)

    return intents


def __save_intent(intent_name, replicas):
    data = {'intent': intent_name, 'questions': replicas}
    print(data)

    python_help_db = connect('python_help')
    intents_collection = python_help_db['intents']

    documents = intents_collection.insert_one(data)

    print()
    print('id: ', documents.inserted_id)


def __save_intents_from_file():
    intents = load_intents_from_file()
    # print(intents)
    # print(len(intents))

    data = []
    for intent_name, replica in intents.items():
        data.append({'intent': intent_name, 'replica': replica})

    # print(data[:2])
    # print(len(data))

    python_help_db = connect('python_help')
    intents_collection = python_help_db['intents']
    # documents = intents_collection.insert_many(data)
    #
    # print()
    # print('ids: ', *documents.inserted_ids, sep='\n')
    # print('Количество записанных документов: ', len(documents.inserted_ids))

    print_collections(python_help_db)


if __name__ == '__main__':
    # print(load_failure_phrases())
    # __save_intents_from_file()

    __save_intent(intent_name='test_delete_3', replicas=[1, 2, 3])

    print()
    print('Намерения:')
    some_intents = get_intents()
    print(*some_intents, sep='\n')
