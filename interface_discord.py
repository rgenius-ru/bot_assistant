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


def is_similar_to(text1, text2):  # Похожая на ...
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
    print(distance, difference)

    if difference < 0.35:
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

    if message.content == 'raise-exception':
        raise discord.DiscordException

    response = start_dialogue(message.content)
    await message.channel.send(response)


def clear_phrases(replica):
    replica = replica.lower()
    alfabet_russ = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    alfabet_engl = 'abcdefghijklmnopqrstuvwxyz'
    some_symbols = ' -'

    replica_copy = ''
    for symbol in replica:
        if symbol in (alfabet_russ + alfabet_engl + some_symbols):
            replica_copy += symbol  # replica_copy = replica_copy + symbol

    replica = replica_copy
    return replica


def get_intent(replica):
    for example in BOT_CONFIG.get('intents'):
        print(example)

    intent = None
    return intent


def start_dialogue(replica):
    # NLU (Natural Language Understanding):
    #  Предварительная обработка реплики (очистка, регистр букв и т.п.)
    #  Относим реплику к какому-либо классу намерений
    #  Извлекаем параметры реплики (извлечение сущностей и объектов)

    # NLG (Natural Language Generation):
    #  Выдать заготовленный ответ основываясь на намерении
    #  Если заготовленного ответа нет, то сгенерировать ответ автоматически и выдать его
    #  Если не удалось сгенерировать ответ, то выдать фразу: "Я непонял"; "Перефразируй" и т.п.

    # NLU (Natural Language Understanding):
    #  Предварительная обработка реплики (очистка, регистр букв и т.п.)
    replica = clear_phrases(replica)

    #  Относим реплику к какому-либо классу намерений
    intent = get_intent(replica)

    answer = replica
    return answer


BOT_CONFIG = {
    'intents': {
        'hello': {
            'examples': [
                'qq', 'hi', 'привет', 'welcome to the club body', 'boy next door'
            ],
            'responses': [
                'здоров', 'барев зес', 'здоров', 'Дадова', 'НУ ЗДАРОВА', 'хэлоу май фрэндс', 'здравствуйте'
            ]
        },
        'goodbye': {
            'examples': [
                'бб', 'gg', 'прощай дружок', 'goodbye'
            ],
            'responses': [
                'goodbye', 'изыди', 'до свидания'
            ]
        }
    },
    'failure_phrases': [
        "Я непонял",
        "Перефразируй"
    ]
}

client.run(TOKEN)
