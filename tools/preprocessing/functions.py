#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Модуль со вспомогательными функциями.

from re import sub
from .templates import *


def condition(value):
    """
    Оканчивается ли число на "1", но не на "11"?
    (value - число в формате строки)
    """
    if value == '1':
        return True
    if len(value) > 1 and value[-2] != '1' and value[-1] == '1':
        return True

    return False


def cardinal(num, casus):
    """
    Склонение количественного числительного.
    (num - число, casus - падеж)
    """
    rem = len(num) % 3
    if rem != 0:
        num = '0' * (3 - rem) + num
    c_num = ''
    triple = len(num) // 3
    for t in range(triple):
        number = num[:3]
        num = num[3:]

        t_num = ''
        if number[2] != '0':
            if number[1] == '1':
                t_num = casus[int(number[2])][1]
            else:
                t_num = casus[int(number[2])][0]
                if number[1] != '0':
                    t_num = casus[0][int(number[1])] + ' ' + t_num
            if number[0] != '0':
                t_num = casus[0][0][int(number[0])] + ' ' + t_num
        else:
            if number[1] != '0':
                t_num = casus[0][int(number[1])]
            if number[0] != '0':
                if t_num == '':
                    t_num = casus[0][0][int(number[0])]
                else:
                    t_num = casus[0][0][int(number[0])] + ' ' + t_num

        if c_num and t_num:
            c_num += ' ' + t_num
        else:
            c_num += t_num
        if t_num and len(num) != 0:
            if number[2] == '1' and number[1] != '1':
                n = 0
            else:
                n = 1
            c_num = c_num + ' ' + casus[0][0][0][triple - t - 1][n]

    c_num = sub(r'одн(им|ого|ому|ом) тысяч(ей|е|и)', r'одной тысяч\2', c_num)
    if c_num == '':
        c_num = casus[0][0][0][0]
    if casus[0][0][0][0] == 'ноль':
        c_num = sub((r'(два|три|четыре) '
                     r'(миллион|миллиард|триллион|квадриллион|квинтиллион|'
                     r'секстиллион|септиллион|октиллион)ов'), r'\1 \2а', c_num)
        c_num = sub('один тысячу', 'одну тысячу', c_num)
        c_num = sub('два тысяч', 'две тысячи', c_num)
        c_num = sub(r'((три|четыре) тысяч)', r'\1и', c_num)

    return c_num


def ordinal(num, casus):
    """
    Склонение порядковых числительных.
    (num - число, casus - падеж)
    """
    if num[-1] == '0':
        try:
            if num[-2] == '0':
                if num[-3] == '0':
                    prenum = ''
                    number = casus[0][0][0][int(num[-4])]
                else:
                    if len(num) == 3:
                        prenum = ''
                    else:
                        prenum = num[:-3]
                        if int(prenum) != 0:
                            prenum += '000_'
                    number = casus[0][0][int(num[-3])]
            else:
                if len(num) == 2:
                    prenum = ''
                else:
                    prenum = num[:-2]
                    if int(prenum) != 0:
                        prenum += '00_'
                number = casus[0][int(num[-2])]
        except:
            prenum = ''
            number = casus[0][0][0][0]
    else:
        if len(num) == 1:
            prenum = ''
            dec = 0
        else:
            if num[-2] == '1':
                dec = 1
                if len(num) == 2:
                    prenum = ''
                else:
                    prenum = num[:-2]
                    if int(prenum) != 0:
                        prenum += '00_'
            else:
                prenum = num[:-1]
                if int(prenum) != 0:
                    prenum += '0_'
                else:
                    prenum += '_'
                dec = 0
        number = casus[int(num[-1])][dec]
    return prenum + number


values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
def roman2arabic(value):
    """
    Преобразование римских цифр в арабские.
    Код заимствован (с изменениями) у Jeff Wheeler.
    """
    total = 0
    prevValue = 0
    value = value[::-1]
    for char in value:
        if values[char] >= prevValue:
            total += values[char]
        else:
            total -= values[char]
        prevValue = values[char]
    total = str(total)
    return total


def substant(num, key, cas=0):
    """
    Чтение единиц измерения
    num - число, key - обозначение единицы измерения,
    cas - падеж (0 - именительный, 1 - родительный, 2 - дательный,
                 3 - творительный, 4 - предложный, 5 - винительный)
    """
    if len(num) > 3 and num[-3:] == '000':
        form = forms[key][1]
    else:
        if cas == 0:
            if len(num) > 1 and num[-2] == '1':
                form = forms[key][1]
            else:
                if num[-1] == '1':
                    form = forms[key][0]
                elif 1 < int(num[-1]) < 5:
                    form = forms[key][10]
                else:
                    form = forms[key][1]
        elif cas == 5:
            if key in zh_units:
                if condition(num):
                    form = {'т': 'тонну',
                            'а.е.': 'астрономическую единицу',
                            'л.с.': 'лошадиную силу',
                            'сек': 'секунду',
                            "'": 'минуту',
                            'ед.': 'единицу',
                            'тыс.': 'тысячу',
                            'шт.': 'штуку'}[key]
                elif num in '234' or (len(num) > 1 and num[-2] != '1' and num[-1] in '234'):
                    form = forms[key][10]
                else:
                    form = forms[key][1]
            else:
                if (len(num) > 1 and num[-2] != '1' and num[-1] in '234') or num in '234':
                    form = forms[key][10]
                elif (len(num) > 1 and num[-2] == '1') or num[-1] != '1':
                    form = forms[key][1]
                else:
                    form = forms[key][0]
        else:
            if (len(num) > 1 and num[-2] == '1') or num[-1] != '1':
                form = forms[key][2 * cas + 1]
            else:
                form = forms[key][2 * cas]
    return form


def feminin(num, cas=0):
    """
    Форма женского рода количественного числительного
    num - число, cas - падеж
    """
    ending = num[-2:]
    number = num
    if cas == 0:
        try:
            if num[-2] != '1':
                pre = num[:-1]
                if int(pre) != 0:
                    pre = num[:-1] + '0'
                if num[-1] == '1':
                    number = pre + '_одна'
                elif num[-1] == '2':
                    number = pre + '_две'
        except:
            if num == '1':
                number = 'одна'
            elif num == '2':
                number = 'две'
    elif cas == 5:
        try:
            if num[-2] != '1':
                pre = num[:-1]
                if int(pre) != 0:
                    pre = num[:-1] + '0'
                if num[-1] == '1':
                    number = pre + '_одну'
                elif num[-1] == '2':
                    number = pre + '_две'
        except:
            if num == '1':
                number = 'одну'
            elif num == '2':
                number = 'две'
    else:
        if ending == 'го' or ending == 'му':
            number = num[:-2] + 'й'
        elif ending == 'им' or ending == 'ом':
            number = num[:-2] + 'ой'
    return number


def daynight(num, nom):
    """
    Счёт суток.
    (num - число, nom - существительное)
    """
    number = num
    if nom == 'сутки':
        if number == '1':
            number = 'одни'
        elif len(num) > 1 and num[-2] != '1' and num[-1] == '1':
            number = num[:-1] + '0_одни'
    else:
        if num == '2':
            number = 'двое'
        elif num == '3':
            number = 'трое'
        elif num == '4':
            number = 'четверо'
        elif len(num) > 1 and num[-2] != '1':
            if 5 > int(num[-1]) > 0:
                number = cardinal(num, r_ca)
                if number[-6:] == 'одного':
                    number = number[:-3] + 'их'
    return number


def fraction(full, frac, cas=0):
    """
    Чтение десятичных дробей до миллионных включительно.
    (full - целая часть, frac - дробная часть, cas - падеж)
    """
    try:
        dec = ' ' + ('десят', 'сот', 'тысячн', 'десятитысячн',
                     'стотысячн', 'миллионн')[len(frac) - 1]
    except:
        dec = ' запятая'
        for t in range(len(frac)):
            dec += ', ' + frac[t]
        return full + dec
    f_part = feminin(full)
    if f_part[-1] == 'а':
        fp = 'ая'
    else:
        fp = 'ых'
    d_part = feminin(frac)
    if d_part[-1] == 'а':
        dp = 'ая'
    else:
        dp = 'ых'
    if cas == 1:
        f_part = cardinal(full, r_ca)
        if condition(full):
            f_part = f_part[:-2] + 'й'
            fp = 'ой'
        else:
            fp = 'ых'
        d_part = cardinal(frac, r_ca)
        if condition(frac):
            d_part = d_part[:-2] + 'й'
            dp = 'ой'
        else:
            dp = 'ых'
    if cas == 2:
        f_part = cardinal(full, d_ca)
        if condition(full):
            f_part = f_part[:-2] + 'й'
            fp = 'ой'
        elif f_part == 'нолю':
            fp = 'ых'
        else:
            fp = 'ым'
        d_part = cardinal(frac, d_ca)
        if condition(frac):
            d_part = d_part[:-2] + 'й'
            dp = 'ой'
        elif d_part == 'нолю':
            dp = 'ых'
        else:
            dp = 'ым'
    if cas == 3:
        f_part = cardinal(full, t_ca)
        if condition(full):
            f_part = f_part[:-2] + 'ой'
            fp = 'ой'
        elif f_part == 'нолём':
            fp = 'ых'
        else:
            fp = 'ыми'
        d_part = cardinal(frac, t_ca)
        if condition(frac):
            d_part = d_part[:-2] + 'ой'
            dp = 'ой'
        elif d_part == 'нолём':
            dp = 'ых'
        else:
            dp = 'ыми'
    if cas == 4:
        f_part = cardinal(full, p_ca)
        if condition(full):
            f_part = f_part[:-1] + 'й'
            fp = 'ой'
        elif f_part == 'ноле':
            fp = 'ых'
        else:
            fp = 'ых'
        d_part = cardinal(frac, p_ca)
        if condition(frac):
            d_part = d_part[:-1] + 'й'
            dp = 'ой'
        else:
            dp = 'ых'
    if cas == 5:
        if f_part[-1] == 'а':
            f_part = f_part[:-1] + 'у'
            fp = 'ую'
        else:
            fp = 'ых'
        if d_part[-1] == 'а':
            d_part = d_part[:-1] + 'у'
            dp = 'ую'
        else:
            dp = 'ых'
    return f_part + ' цел' + fp + ' ' + d_part + dec + dp

