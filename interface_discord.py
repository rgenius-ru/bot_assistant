# bot.py
import os
from sys import exit
import random

import discord
from dotenv import load_dotenv

import nltk

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
if not TOKEN:
    exit('TOKEN = None')

client = discord.Client()


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
    distance = nltk.edit_distance(text1, text2)
    difference = distance / len(text1)
    # print(distance, difference)

    if difference < percent:
        return True
    return False


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
    if message.author == client.user:
        return

    if message.author.bot:  # message.member.roles.has(BOT_ROLE)
        return

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


def get_intent(replica):
    intent = None
    for string in intents_list:
        if string.startswith('##'):
            index_separator = string.index(':')
            intent = string[index_separator + 1:]
            # print(intent)
        if is_similar_to(replica, string.lower()):
            return intent

    return None


def failure_phrases():
    phrases = [
        'как-то непонятно',
        'Нет данных',
        'Я не понял, скажи нормально',
        'Не понимаю о чем ты',
        'Черт его знает, спроси чего полегче',
        'чего?',
        'а?',
        'Что ты сказал?',
        'выражайтесь так, как принято в культурном обществе]'
    ]
    return random.choice(phrases)


def get_answer_from_intent(intent, replica):
    """
    Сообщение боту: Чем знаменит Борис Ельцин?
    Ответ бота: Он бывший президент России

    Сообщение боту: где живут пингвины?
    Ответ бота: на Антарктиде
    """
    response = []

    # answer = random.choice(response)
    if intent == 'wiki':
        if is_similar_to('Чем знаменит Борис Ельцин?', replica):
            answer = 'Он бывший президент России'
        elif is_similar_to('где живут пингвины?', replica):
            answer = 'на Антарктиде'
    else:
        answer = 'Насколько я понял, твоё намерение: ' + intent
    return answer


def start_dialogue(replica):
    # NLU (Natural Language Understanding):
    # + Предварительная обработка реплики (очистка, регистр букв и т.п.)
    # + Относим реплику к какому-либо классу намерений
    # - Извлекаем параметры реплики (извлечение сущностей и объектов)

    # NLG (Natural Language Generation):
    # + Выдать заготовленный ответ основываясь на намерении
    # - Если заготовленного ответа нет, то сгенерировать ответ автоматически и выдать его
    # + Если не удалось сгенерировать ответ, то выдать фразу: "Я непонял"; "Перефразируй" и т.п.

    answer = ''
    #  Предварительная обработка реплики (очистка, регистр букв и т.п.)
    replica = clear_phrases(replica)

    #  Относим реплику к какому-либо классу намерений
    intent = get_intent(replica)
    print(intent)

    #  Выдать заготовленный ответ основываясь на намерении
    if intent:
        answer = get_answer_from_intent(intent, replica)

    #  Если не удалось сгенерировать ответ, то выдать фразу: "Я непонял"; "Перефразируй" и т.п.
    if not answer:
        answer = failure_phrases()

    return answer


def load_intents_old():  # Загрузить намерения из файла в память
    file = open('Intents/intents_old.txt', 'r')  # Отрытие файла в режиме чтения
    text = file.read()  # Чтение данных из файла
    file.close()  # Закрытие файла

    text = text.split('\n')  # Разделение текста и преобразование его в список строк

    intents_list = [
        # ['hello', [], []],
        # ['goodbye', [], []],
    ]

    mode = 'intent'  # examples, responses, end_string, default_string
    end_paragraph = 'default_string'  # end_string
    index = -1
    for string in text:
        if string == '[intent]':
            index += 1
            mode = 'intent'
            continue
        elif string == '[examples]':
            mode = 'examples'
            continue
        elif string == '[responses]':
            mode = 'responses'
            continue
        elif string == '':
            end_paragraph = 'end_string'
        else:
            end_paragraph = 'default_string'

        if mode == 'intent' and end_paragraph == 'default_string':
            intents_list.append([string, [], []])
        elif mode == 'examples' and end_paragraph == 'default_string':
            intents_list[index][1].append(string)
        elif mode == 'responses' and end_paragraph == 'default_string':
            intents_list[index][2].append(string)

    for intent in intents_list:
        print(intent)


def load_intents():  # Загрузить намерения из файла в память
    file = open('Intents/intents.txt', 'r', encoding='utf-8')  # Отрытие файла в режиме чтения
    text = file.read()  # Чтение данных из файла
    file.close()  # Закрытие файла

    text = text.split('\n')  # Разделение текста и преобразование его в список строк

    return text


# intents_list = [
    # ['hello', [], []],
    # ['goodbye', [], []],
# ]

# load_intents_old()

# intents - list strings from raw file intents.txt
intents_list = load_intents()

client.run(TOKEN)
