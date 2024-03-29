import os
from sys import exit
from dotenv import load_dotenv
import discord
import dialogue as dlg
import commands as comm


# UPD 18.02.2023
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


# client = discord.Client()


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

    if ignore(message):
        return

    response = comm.on_command(message.content)  # Проверка на команду, и ответ на неё

    if not response:  # Если ответа нет
        response = dlg.start_dialogue(message.content)  # Запуск диалога

    await message.channel.send(response)  # Отправка ответа в чат


def ignore(message):
    if message.author == client.user:  # Если автор сообщения этот бот
        return True

    # if message.member.roles.has(BOT_ROLE):
    if message.author.bot:  # Если автор сообщения любой бот
        return True

    # name = message.author.name
    # discriminator = message.author.discriminator
    # if name + '#' + discriminator != 'rgenius#1118':  # Если автор сообщения не мой никнейм
    #     return True

    if message.content == '':  # Если сообщение пустое
        return True

    if message.content == 'raise-exception':  # Если произошла ошибка
        raise discord.DiscordException

    return False


if __name__ == '__main__':
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    # print(TOKEN)
    if not TOKEN:
        exit('TOKEN = None')

    client.run(TOKEN)
