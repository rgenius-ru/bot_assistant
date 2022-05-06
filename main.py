import os
from sys import exit
import random
import discord
from dotenv import load_dotenv
from nltk import edit_distance
import mongodb as mdb


client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user.name} подключился к Discord!')


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, Приветствуем тебя на нашем сервере!'
    )


@client.event
async def on_message(message):
    print(message.author)

    if message.author == client.user:
        return

    if message.author.bot:  # message.member.roles.has(BOT_ROLE)
        return

    # if message.author.name != 'rgenius' and message.author.discriminator != '1118':
    #     return

    if message.content == 'raise-exception':
        raise discord.DiscordException

    response = start_dialogue(message.content)
    await message.channel.send(response)


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


def get_intent(replica):
    intent = None
    for string in intents_list:
        if string.startswith('##'):
            index_separator = string.index(':')
            intent = string[index_separator + 1:]
            # print(intent)
        if is_similar_to(replica, clear_phrases(string)):
            return intent

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
    # Загрузить намерения из файла в память
    """

    file = open('Intents/intents.txt', 'r', encoding='utf-8')  # Отрытие файла в режиме чтения
    text = file.read()  # Чтение данных из файла
    file.close()  # Закрытие файла

    text = text.split('\n')  # Разделение текста и преобразование его в список строк

    return text


def generate_answer(intent, replica, difference_threshold=10):
    # сгенерировать ответ
    answer = None

    if intent == 'помощь_в_python':
        # Вывести коэффициенты похожести (дистанции Левенштейна)
        questions = []
        distances = []
        start_flag = False
        for string in intents_list:
            if string == '## intent:помощь_в_python':
                start_flag = True
                continue
            if start_flag and string.startswith('## intent:'):
                break
            if start_flag and string != '':
                distance = edit_distance(string, replica)
                if distance < difference_threshold:
                    questions.append(string)
                    distances.append(distance)
                    print(distance, '\t', string)

        print(distances)
        print(questions)

        index = distances.index(min(distances))
        answer = questions[index]

        # if is_similar_to(replica, 'какие бывают типы данных'):
        #     answer = """
        #     int, float (числа)
        #     str (строки)
        #     list (списки)
        #     dict (словари)
        #     tuple (кортежи)
        #     set (множества)
        #     bool (логический тип данных)
        #     """

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
    # - Если заготовленного ответа нет, то сгенерировать ответ автоматически и выдать его
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

if __name__ == '__main__':
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    # print(TOKEN)
    if not TOKEN:
        exit('TOKEN = None')

    intents_list = load_intents()  # intents - list strings from raw file intents.txt
    # print(*intents_list[:50], sep='\n')

    failure_phrases = mdb.load_failure_phrases()
    print(failure_phrases)

    client.run(TOKEN)
