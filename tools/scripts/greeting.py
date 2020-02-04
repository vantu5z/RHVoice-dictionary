from datetime import datetime
import random


def get_greeting():
    """
    Получение приветствия.
    """
    # приветствия
    morning =   ['Доброе утро', 'С добрым утром', 'Бодрого утречка',
                 'Рад Вас видеть этим прекраным утром']
    day =       ['Добрый день', 'Бонжур']
    evning =    ['Добрый вечер', 'Вечер добрый']
    night =     ['Доброй ночи', 'Приветствую Вас в этот поздний час']
    universal = ['Привет', 'Салют', 'Доброе время суток', 'Приветствую Ваc',
                 'Добро пожаловать', 'Рад Вас видеть']
    
    hour = datetime.now().hour
    
    # выбор списка с приветствиями в зависимости от времени
    if hour > 5 and hour<12:
        greeting = morning
    elif hour > 11 and hour<17:
        greeting = day
    elif hour > 16 and hour<24:
        greeting = evning
    elif hour > 24 and hour<4:
        greeting = night
    else:
        greeting = universal

    # иногда подключаем универсальное приветствие
    if random.randint(0, 5) == 5:
        greeting = universal
    
    num = random.randint(0, len(greeting)-1)

    return greeting[num]
