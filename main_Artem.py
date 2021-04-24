import json
import random
import sys

# Список случайных ответов, если бот не знает что ответить
notUnderstandList = [
    'моя твоя не понимат!!',
    'Чтобы узнать что я умею напиши: помощь или п',
    'I\'m from Russia'
]

# Приветственная фраза
print()
print('---------------------------------------------------')
print('Привет. Я Чатбот.')
print()
print('Напиши мне что-нибудь, и я отвечу')
print('Чтобы узнать что я умею напиши: помощь или п')
print('---------------------------------------------------')
print()

# Чтение файла с вопросами и ответами
with open('datafile') as f:
    main_list = json.load(f)
    f.close()


def command_help():
    if question == 'помощь' or question == 'п':
        print('---------------------------------------------------')
        print('новый (коротко: н) - запись в базу нового вопроса и ответа.')
        print('все вопросы (коротко: все) - вывод всех вопросов и ответов.')
        print('выход (коротко: в) - обновление базы и выход из программы.')
        print('---------------------------------------------------')
        print()
        return True
    return False

def Athor():
    if question == 'Автроры' or question == 'а':
        print('---------------------------------------------------')
        print('Сергей')
        print('Матвей')
        print('Артем')
        print('Саша Г.')
        print('Саша Р.')
        print('Степан')
        print('Лёша')
        print('---------------------------------------------------')
        print()
        return True
    return False


def command_new():
    if question == 'новый' or question == 'н':
        v1 = input('новый вопрос: ')
        v2 = input('      ответ : ')
        main_list[v1] = v2

        with open('datafile', 'w') as f:
            f.seek(0)
            f.truncate(0)
            json.dump(main_list, f, sort_keys=True, indent=4,
                      ensure_ascii=False)

        print()
        return True
    return False


def command_all():
    if question == 'все вопросы' or question == 'все':
        print()
        for question_answer in main_list:
            print(question_answer)
            print(main_list[question_answer])
            print()
        return True
    return False


def command_exit():
    if question == 'выход' or question == 'в':
        print('записываем в блокнотик и..')

        with open('datafile', 'w') as f:
            f.truncate(0)
            json.dump(main_list, f, sort_keys=True, indent=4,
                      ensure_ascii=False)
            print('уходим')
            f.close()

        sys.exit(0)


def command_random(_question):
    if _question == 'рандом' or _question == 'р':
        for x in range(5):
            _question, answer = random.choice(list(main_list.items()))
            print(_question, ':', answer)
        return True
    return False


def question_answer():
    if question in main_list:
        print(main_list[question])
        print()
        return True
    return False


def i_dont_know():
    if not is_command_in_base:
        print(random.choice(notUnderstandList))
        print()


# Бесконечный цикл
is_command_in_base = False
while 1:
    question = input()
    is_command_in_base = Athor()
    is_command_in_base = command_help()
    is_command_in_base = command_new()
    is_command_in_base = command_all()
    is_command_in_base = command_random(question)
    command_exit()

    question_answer()
