import json
import random

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

# Бесконечный цикл
while 1:
    question = input()

    if question == 'помощь' or question == 'п':
        print('---------------------------------------------------')
        print('новый (коротко: н) - запись в базу нового вопроса и ответа.')
        print('все вопросы (коротко: все) - вывод всех вопросов и ответов.')
        print('выход (коротко: в) - обновление базы и выход из программы.')
        print('---------------------------------------------------')
        print()
        continue

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
        continue

    if question == 'все вопросы' or question == 'все':
        print()
        for question_answer in main_list:
            print(question_answer)
            print(main_list[question_answer])
            print()
        continue

    if question == 'выход' or question == 'в':
        print('записываем в блокнотик и..')

        with open('datafile', 'w') as f:
            f.truncate(0)
            json.dump(main_list, f, sort_keys=True, indent=4,
                      ensure_ascii=False)
            print('уходим')
            f.close()

        break

    if question == 'рандом' or question == 'р':
        for x in range(5):
            question, answer = random.choice(list(main_list.items()))
            print(question, ':', answer)
        continue

    if question in main_list:
        print(main_list[question])
        print()
    else:
        print(random.choice(notUnderstandList))
        print()
