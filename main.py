import os
from sys import exit
from dotenv import load_dotenv
import discord
import dialogue as dlg
import commands as comm


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

    if message.content == '':
        return

    response = comm.on_command(message.content)

    if not response:
        response = dlg.start_dialogue(message.content)

    await message.channel.send(response)


if __name__ == '__main__':
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    # print(TOKEN)
    if not TOKEN:
        exit('TOKEN = None')

    client.run(TOKEN)
