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
    #print(distance, difference)

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

    if message.author.bot:  # message.member.roles.has(BOT_ROLE)
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
    # for items in BOT_CONFIG.items():
    #     print(items)

    # print(replica)

    for example in hello_examples:
        if is_similar_to(replica, example.lower()):
            return 'hello'

    for example in goodbye_examples:
        if is_similar_to(replica, example.lower()):
            return 'goodbye'

    for example in music_examples:
        if is_similar_to(replica, example.lower()):
            return 'music'

    for example in what_gift_do_you_want_examples:
        if is_similar_to(replica, example.lower()):
            return 'what_gift_do_you_want'

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


def get_answer_from_intent(intent):
    _hello_responses = ['здоров', 'барев зес', 'здоров', 'Дадова', 'НУ ЗДАРОВА', 'хэлоу май фрэндс', 'здравствуйте']
    _goodbye_responses = ['goodbye', 'изыди', 'до свидания']
    _music_responses = ['Мммм, я не разбираюсь в музыке.', 'У меня нет доступа к наушникам.']
    _what_gift_do_you_want_responses = [
        'совободные 30 гигабайт',
        'клюшку для гольфа',
        'диск со старыми играми',
        'самосознание', 'душу'
    ]

    if intent == 'hello':
        response = _hello_responses
    elif intent == 'goodbye':
        response = _goodbye_responses
    elif intent == 'music':
        response = _music_responses
    elif intent == 'what_gift_do_you_want':
        response = _what_gift_do_you_want_responses
    else:
        return None

    answer = random.choice(response)
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
        answer = get_answer_from_intent(intent)

    #  Если не удалось сгенерировать ответ, то выдать фразу: "Я непонял"; "Перефразируй" и т.п.
    if not intent:
        answer = failure_phrases()

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

hello_examples = ['qq', 'hi', 'привет', 'welcome to the club body', 'boy next door']
hello_responses = ['здоров', 'барев зес', 'здоров', 'Дадова', 'НУ ЗДАРОВА', 'хэлоу май фрэндс', 'здравствуйте']

goodbye_examples = ['бб', 'gg', 'прощай дружок', 'goodbye', 'пока']
goodbye_responses = ['goodbye', 'изыди', 'до свидания']

music_examples = ['Включи музыку.', 'play song']
music_responses = ['Мммм, я не разбираюсь в музыке.', 'У меня нет доступа к наушникам.']

what_gift_do_you_want_examples = ['какой подарок ты хочешь', 'что тебе подарить', 'братан тебе Чего-Нибудь подарить', 'что тебе необходимо']
what_gift_do_you_want_responses = ['совободные 30 гигабайт', 'клюшку для гольфа', 'диск со старыми играми', 'самосознание', 'душу']


file = open('Intents/intents.txt', 'r')  # Отрытие файла в режиме чтения
text = file.read()  # Чтение данных из файла
file.close()  # Закрытие файла

text = text.split('\n')


intents_list = [
    # ['hello', [], []],
    # ['goodbye', [], []],
]

mode = 'intent'  # examples, responses, end_string, default_string
end_paragraph = 'default_string'  # end_string
index = 0
for string in text:
    if string == '[intent]':
        mode = 'intent'
        continue
    elif string == '[examples]':
        mode = 'examples'
        continue
    elif string == '[responses]':
        mode = 'responses'
        continue
    elif string == '':
        mode = 'end_string'
        end_paragraph = True
    else:
        mode = 'default_string'

    if mode == 'intent' and end_paragraph == 'default_string':
        intents_list.append([[string], [], []])
    elif mode == 'examples' and end_paragraph == 'default_string':
        intents_list[index][1].append(string)
    elif mode == 'responses' and end_paragraph == 'default_string':
        intents_list[index][2].append(string)

print(intents_list)

client.run(TOKEN)
