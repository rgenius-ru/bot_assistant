import mongodb as mdb
import dialogue as dlg
import list_tools as lt


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
        'добавь вопрос':    add_question,  # !добавь вопрос как возвести в квадрат? number ** 2
        '+вопрос':          add_question,
        'обнови вопрос':    update_question,  # !обнови вопрос как вычислить корень? math.sqrt(number)
        'удали вопрос':     delete_question,  # !удали вопрос как вычислить корень?
        '-вопрос':          delete_question,
        'все вопросы':      all_questions,
    }

    for command in help_commands:
        command = start_symbol + command
        if replica.startswith(command):
            return all_commands(commands.keys())

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


def all_commands(commands):
    text = '**Список команд:**\n'

    for command in commands:
        text += '!' + command + '\n'

    return text


def add_question(question, answer):
    if not mdb.add_replica(question, answer):
        return 'Ошибка. Не могу добавить вопрос и ответ.'

    dlg.intents_name, dlg.all_intents = dlg.load_intents()

    return 'Вопрос и ответ добавлены успешно.'


def update_question(question, answer):
    if not mdb.update_answer(question, answer):
        return 'Ошибка. Не могу изменить вопрос.'

    dlg.intents_name, dlg.all_intents = dlg.load_intents()

    return 'Вопрос изменён успешно.'


def delete_question(question, answer):
    if not mdb.delete_question(question):
        return 'Ошибка. Не могу удалить вопрос.'

    dlg.intents_name, dlg.all_intents = dlg.load_intents()

    return 'Вопрос удалён успешно.'


def all_questions(question, answer):
    questions = mdb.get_all_question()
    count = len(questions)

    questions = lt.shorten_list(questions)

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
