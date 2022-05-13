import os
from sys import exit
from dotenv import load_dotenv
import discord
import mongodb as mdb
import dialogue as dlg


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

    response = on_command(message.content)

    if not response:
        response = dlg.start_dialogue(message.content)

    await message.channel.send(response)


def on_command(replica):
    start_symbol = '!'

    help_commands = [
        'все команды',
        'команды',
        'что ты умеешь',
        'справка',
        'help',
        'помощь'
    ]

    commands = {
        'добавь вопрос':    on_command_add_question,  # !добавь вопрос как возвести в квадрат? number ** 2
        '+вопрос':          on_command_add_question,
        'обнови вопрос':    on_command_update_question,  # !обнови вопрос как вычислить корень? math.sqrt(number)
        'удали вопрос':     on_command_delete_question,  # !удали вопрос как вычислить корень?
        '-вопрос':          on_command_delete_question,
        'все вопросы':      on_command_all_questions,
    }

    for command in help_commands:
        command = start_symbol + command
        if replica.startswith(command):
            return on_command_all_commands(commands.keys())

    founded = None
    for command, function in commands.items():
        command = start_symbol + command
        if replica.startswith(command):
            founded = command, function
            break

    if not founded:
        return None

    command, function = founded

    text = replica.replace(command, '').lstrip()
    if '?' in text:
        question_end = text.index('?') + 1
        question = text[:question_end]
    else:
        question = text

    answer = text.replace(question, '').lstrip()
    result = function(question, answer)

    return result


def on_command_all_commands(commands):
    text = '**Список команд:**\n'

    for command in commands:
        text += '!' + command + '\n'

    return text


def on_command_add_question(question, answer):
    if not mdb.add_replica(question, answer):
        return 'Ошибка. Не могу добавить вопрос и ответ.'

    dlg.intents_name, dlg.all_intents = dlg.load_intents()

    return 'Вопрос и ответ добавлены успешно.'


def on_command_update_question(question, answer):
    if not mdb.update_answer(question, answer):
        return 'Ошибка. Не могу изменить вопрос.'

    dlg.intents_name, dlg.all_intents = dlg.load_intents()

    return 'Вопрос изменён успешно.'


def on_command_delete_question(question, answer):
    if not mdb.delete_question(question):
        return 'Ошибка. Не могу удалить вопрос.'

    dlg.intents_name, dlg.all_intents = dlg.load_intents()

    return 'Вопрос удалён успешно.'


def on_command_all_questions(question, answer):
    questions = mdb.get_all_question()
    count = len(questions)

    questions = shorten_list(questions)

    text = ''
    index = 1
    for question in questions:
        if question == '...':
            number = ''
            index = count - 5
        else:
            number = str(index) + '\t'

        text += number + question + '\n'
        index += 1

    text = '**Вопросы которые у меня записаны:**\n' + text

    return text


def shorten_list(source_list):
    if len(source_list) > 10:
        return source_list[:5] + ['...'] + source_list[-5:]

    return source_list


# Описание сновного алгоритма находится в функции start_dialogue()

if __name__ == '__main__':
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    # print(TOKEN)
    if not TOKEN:
        exit('TOKEN = None')

    client.run(TOKEN)
