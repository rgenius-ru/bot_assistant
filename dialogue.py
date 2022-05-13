import random
from nltk import edit_distance
import mongodb as mdb


def clear_phrases(replica):
    replica = replica.lower()
    alphabet_russ = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    alphabet_eng = 'abcdefghijklmnopqrstuvwxyz'
    some_symbols = ' -'

    replica_copy = ''
    for symbol in replica:
        if symbol in (alphabet_russ + alphabet_eng + some_symbols):
            replica_copy += symbol  # replica_copy = replica_copy + symbol

    replica = replica_copy
    return replica


def is_similar_to(text1, text2, percent=0.35):  # Похожая на ...
    # Добрый вечер
    # Дбрый вечер
    # Добрый вече

    # Добрый вечер

    # Добрый дечер
    # Добрый денер
    # Добрый деньр
    # Добрый день

    # Добрый день

    # Расстояние = 4
    # Изменение в проценнтах = 4/26 (= 0.15) Какой хороший Добрый день
    # Изменение в проценнтах = 4/26 (= 0.33) Добрый день
    distance = edit_distance(text1, text2)
    difference = distance / len(text1)
    # print(distance, difference)

    if difference < percent:
        return True
    return False


def get_intent(message):
    for intent_dict in all_intents:
        title = intent_dict.get('title')
        replicas = intent_dict.get('replicas')

        for replica in replicas:
            if is_similar_to(message, clear_phrases(replica)):
                return title

    return None


def random_failure_phrase():
    return random.choice(failure_phrases)


def get_answer_from_intent(intent, replica):
    """
    Сообщение боту: Чем знаменит Борис Ельцин?
    Ответ бота: Он бывший президент России

    Сообщение боту: где живут пингвины?
    Ответ бота: на Антарктиде
    """

    # answer = random.choice(response)
    answer = None
    if intent == 'wiki':
        if is_similar_to('Чем знаменит Борис Ельцин?', replica):
            answer = 'Он бывший президент России'
        elif is_similar_to('где живут пингвины?', replica):
            answer = 'на Антарктиде'
    elif intent == 'про_кошек':
        if is_similar_to('Как там мой кошак?', replica):
            answer = 'Сбежал куда-то вчера с пятого этажа'
        elif is_similar_to('Что известно о кошках?', replica):
            answer = 'что они усатые'

    elif intent == 'расскажи_прогноз_погоды':
        # days = ['сегодня', 'завтра', 'послезавтра', 'понедельниц', 'вторник', 'среда']
        # phenomenons = ['дождь', 'снег', 'облачность', 'гололедица']
        phrase = 'Завтра дождь будет?'
        # words = phrase.split()

        # какая погода будет в 14 часов 14 числа?

        # Цикл
        # day = 'завтра'
        # Цикл
        # phenomenon = 'дождь'

        if is_similar_to(phrase, replica):
            print('Спрашивает про сегодня')

    else:
        print('Насколько я понял, твоё намерение: ', intent)

    return answer


def load_intents():
    """
    # Загрузить намерения из БД  в память
    """

    mdb_intents = mdb.get_intents()

    _all_intents = []
    _intents_name = []
    for intent in mdb_intents:
        name = intent.get('title')
        _all_intents.append(intent)
        _intents_name.append(name)

    return _intents_name, _all_intents


def generate_answer(intent_title, message, difference_threshold=10):
    # сгенерировать ответ
    answer = None

    if intent_title == 'помощь_в_python':
        # Поиск самого близкого коэффициента похожести (дистанции Левенштейна)
        questions = []
        distances = []
        replicas = []
        answers = []

        for intent_dict in all_intents:
            title = intent_dict.get('title')
            if title == intent_title:
                replicas = intent_dict.get('replicas')
                answers = intent_dict.get('answers')
                break

        for replica in replicas:
            distance = edit_distance(replica, message)
            if distance < difference_threshold:
                questions.append(replica)
                distances.append(distance)
                print(distance, '\t', replica)

        print(distances)
        print(questions)

        index = distances.index(min(distances))
        question = questions[index]
        index_answer = replicas.index(question)

        if answers[index_answer] is None:
            return None

        answer = '**Похожий вопрос:** ' + question + '\n'
        answer += '**Ответ:** ' + answers[index_answer]

    return answer


def start_dialogue(replica):
    """
    # Общий план диалогов:

    # NLU (Natural Language Understanding):
    # + Предварительная обработка реплики (очистка, регистр букв и т.п.)
    # + Относим реплику к какому-либо классу намерений
    # + Извлекаем параметры реплики (извлечение сущностей и объектов)

    # NLG (Natural Language Generation):
    # + Выдать заготовленный ответ основываясь на намерении
    # + Если заготовленного ответа нет, то сгенерировать ответ автоматически и выдать его
    # + Если не удалось сгенерировать ответ, то выдать фразу: "Я непонял"; "Перефразируй" и т.п.

    :param replica:
    :return: answer
    """

    answer = ''
    #  Предварительная обработка реплики (очистка, регистр букв и т.п.)
    replica = clear_phrases(replica)

    #  Относим реплику к какому-либо классу намерений
    intent = get_intent(replica)
    print(intent)

    #  Выдать заготовленный ответ основываясь на намерении
    if intent:
        answer = get_answer_from_intent(intent, replica)

    # Если заготовленного ответа нет, то сгенерировать ответ автоматически и выдать его
    # print('-------', answer)
    if not answer:
        answer = generate_answer(intent, replica)

    #  Если не удалось сгенерировать ответ, то выдать фразу: "Я непонял"; "Перефразируй" и т.п.
    if not answer:
        answer = random_failure_phrase()

    return answer


# Описание сновного алгоритма находится в функции start_dialogue()

intents_name, all_intents = load_intents()
# print(intents_name)
# print(all_intents[0].get('title'))

failure_phrases = mdb.load_failure_phrases()
# print(failure_phrases)
