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


@client.event
async def on_ready():
    print(f'{client.user.name} подключился к Discord!')


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, Приветствуем тебя на нашем сервере!'
    )


def is_similar_to():
    pass


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
    elif message.content == 'копия с гитхаб':
        quotes = [
            '',
            ''
        ]
        response = random.choice(quotes)
        await message.channel.send(response)
    elif message.content == 'raise-exception':
        raise discord.DiscordException

client.run(TOKEN)
