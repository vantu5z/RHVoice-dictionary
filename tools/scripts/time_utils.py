#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Работа со временем.

import string
import datetime


def get_time():
    """
    Получение текущего времени.
    В формате: "HH часов YY минут"
    """
    now_time = datetime.datetime.now()               # текущая дата со временем
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
