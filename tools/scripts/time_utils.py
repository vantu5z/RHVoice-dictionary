#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Работа со временем.

import string
from datetime import datetime


def get_time():
    """
    Получение текущего времени.
    В формате: "HH часов YY минут"
    """
    now_time = datetime.now()             # текущая дата со временем
    cur_hour = now_time.hour
    cur_minute = now_time.minute
    last_min = cur_minute % 10            # последняя минута (например 38 -> 8)

    # склоняем "час" и "минуту"
    lc_hour = inflect(cur_hour,'час','часа','часов')
    lc_minute = inflect(cur_minute,'минута','минуты','минут')

    # корректровка один и два - на одна, две
    if cur_minute == 1:
        say_time = "%d %s одна минута" % (cur_hour, lc_hour)
    elif last_min == 1 and cur_minute != 11:
        say_time = "%d %s %d одна минута" % (cur_hour, lc_hour, cur_minute-1)
    elif cur_minute == 2:
        say_time = "%d %s две минуты" % (cur_hour, lc_hour)
    elif last_min == 2 and cur_minute != 12:
        say_time = "%d %s %d две минуты" % (cur_hour, lc_hour, cur_minute-2)
    elif cur_minute == 0:
        say_time = "%d %s ровно" % (cur_hour, lc_hour)
    else:
        say_time = "%d %s %d %s" % (cur_hour, lc_hour, cur_minute, lc_minute)

    return say_time

def get_date():
    """
    Сегодняшняя дата без года.
    """
    month_dic = {1:  "января",
                 2:  "февраля",
                 3:  "марта",
                 4:  "апреля",
                 5:  "мая",
                 6:  "июня",
                 7:  "июля",
                 8:  "августа",
                 9:  "сентября",
                 10: "октября",
                 11: "ноября",
                 12: "декабря"
            }
    now_date = datetime.now()
    day = now_date.day
    month = now_date.month

    return "%d-е %s" % (day, month_dic.get(month))

def get_weekday():
    """
    Получение текущего дня недели.
    """
    day_names = {0: 'понедельник',
                 1: 'вторник',
                 2: 'среда',
                 3: 'четверг',
                 4: 'пятница',
                 5: 'суббота',
                 6: 'воскресенье'}

    return day_names.get(datetime.today().weekday())


def inflect(n, form1, form2, form5):
    """
    Приведение в соответствие слова в зависимости от числа.
    Например: inflect(18,'градус','градуса','градусов') -> 'градусов'
    """
    n = abs(n)          # убираем минус, если есть
    n  = n % 100        # две последних цифры
    n1 = n % 10         # последняя цифра

    if n>10 and n<20 : form=form5
    elif n1>1 and n1<5 : form=form2
    elif n1==1 : form=form1
    else: form=form5

    return form
