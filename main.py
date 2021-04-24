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
    vopros = input()

    if vopros == 'помощь' or vopros == 'п':
        print('---------------------------------------------------')
        print('новый (коротко: н) - запись в базу нового вопроса и ответа.')
        print('все вопросы (коротко: все) - вывод всех вопросов и ответов.')
        print('выход (коротко: в) - обновление базы и выход из программы.')
        print('---------------------------------------------------')
        print()
        continue

    if vopros == 'новый' or vopros == 'н':
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

    if vopros == 'все вопросы' or vopros == 'все':
        print()
        for vopros_otvet in main_list:
            print(vopros_otvet)
            print(main_list[vopros_otvet])
            print()
        continue

    if vopros == 'выход' or vopros == 'в':
        print('записываем в блокнотик и..')

        with open('datafile', 'w') as f:
            f.truncate(0)
            json.dump(main_list, f, sort_keys=True, indent=4,
                      ensure_ascii=False)
            print('уходим')
            f.close()

        break

    if vopros == 'рандом' or vopros == 'р':
        for x in range(5):
            vopros, otvet = random.choice(list(main_list.items()))
            print(vopros, ':', otvet)
        continue

    if vopros in main_list:
        print(main_list[vopros])
        print()
    else:
        print(random.choice(notUnderstandList))
        print()
