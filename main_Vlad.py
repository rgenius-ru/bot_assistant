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

def money(question):
    if question == 'монета' or question == 'м':
        e = 1
        c = 0
        question = input('орел или решка?')
        if question == 'орел' or question == 'о':
            m = random.randint(e, c)
            print('подкидываем монетку...', )
            if m == 1:
                print('УРА ВАМ ВЫПАЛ : ОРЕЛ')
            if question == 'решка' or question == 'р':
                m = random.randint(e, c)
                print('подкидываем монетку...')
                if m == 0:
                 print('УРА ВАМ ВЫПАЛ : РЕШКА')


def command_r_number(question):
    if question == 'roll' or question == 'roll':
        r_n = random.randint(0, 10)
        r = random.randint(0, 100)

        question = input('Введите тип ролла')
        if question == 'rol-nolet' or question == 'r-n':
            print('производится ролл...', )
            print('УРА ВАМ ВЫПАЛО ЧИСЛО :',r_n)
            if question == 'roll-classic' or question == 'r-c':
                print('производится ролл...',r)
                print('УРА ВАМ ВЫПАЛО ЧИСЛО :', r)


# Бесконечный цикл
is_command_in_base = False
while 1:
    question = input()
    is_command_in_base = command_r_number(question)
    is_command_in_base = money(question)
    is_command_in_base = command_help()
    is_command_in_base = command_new()
    is_command_in_base = command_all()
    is_command_in_base = command_random(question)
    command_exit()

    question_answer()
