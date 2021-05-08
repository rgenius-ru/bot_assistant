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

    if message.content == 'что ты умеешь?':
        quotes = [
            'Пока что ничего.',
            'Ничего!',
            '... ничего. Научи меня.'
        ]
        response = random.choice(quotes)
        await message.channel.send(response)

    elif is_similar_to(message.content, 'копия с гитхаб'):
        # quotes = [
        #    '',
        #    ''
        # ]
        # response = random.choice(quotes)
        response = 'Чтобы сделать копию с гитхаб надо ...'
        await message.channel.send(response)

    elif message.content == 'raise-exception':
        raise discord.DiscordException

client.run(TOKEN)


