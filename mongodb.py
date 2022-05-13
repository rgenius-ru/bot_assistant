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


def del_all_intents():
    python_help_db = connect('python_help')
    intents_collection = python_help_db['intents']

    documents = intents_collection.delete_many({})  # Удаление всех документов

    return documents


def get_intents(limit=None):
    python_help_db = connect('python_help')
    intents_collection = python_help_db['intents']

    if limit:
        intents = intents_collection.find().limit(limit)
    else:
        intents = intents_collection.find()

    return intents


def get_intent(title):
    python_help_db = connect('python_help')
    intents_collection = python_help_db['intents']

    query = {"title": {"$eq": title}}
    intent = intents_collection.find_one(query)

    return intent


def load_intents_from_file():
    file = open('Intents/intents.txt', 'r', encoding='utf-8')  # Отрытие файла в режиме чтения
    text = file.read()  # Чтение данных из файла
    file.close()  # Закрытие файла

    text = text.split('\n')  # Разделение текста и преобразование его в список строк

    intents = {}
    replicas = []
    intent = ''
    for string in text:
        if string.startswith('## intent:'):
            if intent:
                intents.update({intent: replicas})

            replicas = []
            index_separator = string.index(':')
            intent = string[index_separator + 1:]
            intents.setdefault(intent)

        elif string != '' and not string.startswith('# '):
            replicas.append(string)

    intents.update({intent: replicas})

    return intents


def add_replica(replica, _answer=None, title='помощь_в_python'):
    python_help_db = connect('python_help')
    intents_collection = python_help_db['intents']

    intent = get_intent(title)
    replicas = intent.get('replicas')
    _answers = intent.get('answers')

    replicas.append(replica)
    _answers.append(_answer)

    query = {'title': title}  # Запрос - Что нужно заменить
    new_values = {'$set': {'replicas': replicas, 'answers': _answers}}  # Новое значение - Чем нужно заменить
    result = intents_collection.update_one(query, new_values)  # Заменить один документ

    print('Добавлено документов в количестве:', result.matched_count)

    if result.matched_count == 0:
        return False

    return True


def update_answer(replica, _answer, title='помощь_в_python'):
    python_help_db = connect('python_help')
    intents_collection = python_help_db['intents']

    intent = get_intent(title)
    replicas = intent.get('replicas')
    _answers = intent.get('answers')

    # Поиск реплики и замена вопроса
    if replica not in replicas:
        print('Реплика не найдена!')
        return False

    index = replicas.index(replica)
    _answers[index] = _answer

    query = {'title': title}  # Запрос - Что нужно заменить
    new_values = {'$set': {'answers': _answers}}  # Новое значение - Чем нужно заменить
    result = intents_collection.update_one(query, new_values)  # Заменить один документ

    print('Заменено документов в количестве:', result.matched_count)

    if result.matched_count == 0:
        return False

    return True


def delete_question(replica, title='помощь_в_python'):
    python_help_db = connect('python_help')
    intents_collection = python_help_db['intents']

    intent = get_intent(title)
    replicas = intent.get('replicas')
    _answers = intent.get('answers')

    # Поиск реплики
    if replica not in replicas:
        print(f'Реплика "{replica}" не найдена!')
        return

    index = replicas.index(replica)

    replicas.remove(replica)

    _answer = _answers[index]
    _answers.remove(_answer)

    # print(replicas)
    # print(_answers)

    query = {'title': title}  # Запрос - Что нужно заменить

    new_values = {'$set': {'replicas': replicas, 'answers': _answers}}  # Новое значение - Чем нужно заменить
    result = intents_collection.update_one(query, new_values)  # Заменить один документ

    print('Удалено документов в количестве:', result.matched_count)

    if result.matched_count == 0:
        return False

    return True


def get_all_question(title='помощь_в_python'):
    intent = get_intent(title)
    _questions = intent.get('replicas')

    return _questions


def __save_intent(title, replicas, _answers=None):
    if not _answers:
        _answers = [None] * len(replicas)

    data = {'title': title, 'replicas': replicas, 'answers': _answers}
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
    for title, replicas in intents.items():
        answers = [None] * len(replicas)
        data.append({'title': title, 'replicas': replicas, 'answers': answers})

    # print(data[:2])
    # print(len(data))

    python_help_db = connect('python_help')
    intents_collection = python_help_db['intents']
    documents = intents_collection.insert_many(data)

    print()
    print('ids: ', *documents.inserted_ids, sep='\n')
    print('Количество записанных документов: ', len(documents.inserted_ids))

    print_collections(python_help_db)


if __name__ == '__main__':
    # print(load_failure_phrases())

    # print('Удалено документов в количестве:', del_all_intents().deleted_count)

    # __save_intents_from_file()
    # __save_intent(title='test_ghfghfgh', replicas=['sdfsdf', 'dddd', 'eee'])

    # add_replica('как найти слово в предложении?', 'index_int = text_str.find(word_str)')
    # update_answer('как вывести последний элемент списка?', 'print(list_name[:-1])')
    # delete_question('как найти слово в предложении?')
    # print(get_intent('помощь_в_python'))

    questions = get_intent('помощь_в_python').get('replicas')
    answers = get_intent('помощь_в_python').get('answers')

    for question, answer in zip(questions, answers):
        print(question)
        print(answer)
        print()

    # print()
    # print('Намерения:')
    # some_intents = get_intents(2)
    # print(*some_intents, sep='\n')
