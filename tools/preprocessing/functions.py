#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Модуль со вспомогательными функциями.

from re import sub
from .templates import *


def replace(text, new, length, start, end):
    delta = len(text) - length
    text = text[:start + delta] + new + text[end + delta:]
    return text

def condition(value):
    """
    Оканчивается ли число на "1", но не на "11"?
    (value - число в формате строки)
    """
    if value == '1' or (len(value) > 1 and value[-2] != '1'
                        and value[-1] == '1'):  
        return True
    else:
        return False


def cardinal(num, casus):
    """
    Склонение количественного числительного.
    Числа свыше 30 разрядов не обрабатываются.
    (num - число, casus - падеж)
    """
    if len(num) > 30:
        return num
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
    Корректно для чисел менее 1 000 000.
    (num - число, casus - падеж_род/мн.ч.)
    """

    nil = 0
    while num[0] == '0' and len(num) > 1:
        nil += 1
        num = num[1:]

    if len(num) == 1:
        number = ordinal_d[num]
    else:
        if num[-3:] == '000':
            number = cardinal(num[:-3], r_ca)
            if number == 'одного':
                number = ''
            elif number == 'ста':
                number = 'сто'
            number += 'тысячный'
        else:
            if num[-2:] == '00':
                prenum = num[:-3]
                if prenum != '':
                    prenum += '000_ '
                number = cardinal(num[-3], r_ca)
                if number == 'одного':
                    number = ''
                number = prenum + number + 'сотый'
            else:
                if num[-1] == '0' or num[-2] == '1':
                    number = num[:-2]
                    if number != '':
                        number += '00_ '
                    number += ordinal_d[num[-2:]]
                else:
                    number = num[:-1] + '0_ ' + ordinal_d[num[-1]]

    if casus == 'i_mu':
        pass
    elif number[-2:] == 'ий':
        number = number[:-2] + ordinal_d[casus][0]
    else:
        number = number[:-2] + ordinal_d[casus][1]
    return '0 ' * nil + number


values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
def roman2arabic(value):
    """
    Преобразование римских цифр в арабские.
    Код заимствован (с изменениями) у Jeff Wheeler.
    """

    number = value.count('I')
    if (number > 3 or (number == 3 and 'III' not in value)
        or (number == 2 and 'II' not in value)):
        return value
    for char in 'VLD':
        if value.count(char) > 1:
            return value
    for char in 'XCM':
        number = value.count(char)
        if number > 4:
            return value
        elif number == 4:
            for sub in ('XXXX', 'CCCC', 'MMMM'):
                if sub in value:
                    return value
            for sub in ('XX', 'CC', 'MM'):
                if value.count(sub) == 2:
                    return value
    for sub in ('IL', 'IC', 'ID', 'IM', 'VX', 'VL', 'VC', 'VD', 'VM', 'XD',
                'LC', 'LD', 'LM', 'DM','IIV', 'IIX', 'XXL', 'XXC', 'XXM', 'CCM',
                'IXX', 'IXL', 'IXC', 'IXM', 'XLX', 'XCX', 'XCL', 'XCC', 'XCD',
                'XCM', 'CDC', 'CDM', 'CMC', 'CMD', 'CMM'):
        if sub in value:
            return value

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
                            'шт.': 'штуку',
                            'атм': 'атмосферу'}[key]
                elif num in '234' or (len(num) > 1 and num[-2] != '1'
                                      and num[-1] in '234'):
                    form = forms[key][10]
                else:
                    form = forms[key][1]
            else:
                if num in '234' or (len(num) > 1 and num[-2] != '1'
                                    and num[-1] in '234'):
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
                    number = pre + '_ одна'
                elif num[-1] == '2':
                    number = pre + '_ две'
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
                    number = pre + '_ одну'
                elif num[-1] == '2':
                    number = pre + '_ две'
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


def decimal(full, frac, cas=0):
    """
    Чтение десятичных дробей до миллионных включительно.
    (full - целая часть, frac - дробная часть, cas - падеж)
    """
    try:
        dec = '_ ' + ('десят', 'сот', 'тысячн', 'десятитысячн',
                      'стотысячн', 'миллионн')[len(frac) - 1]
    except:
        dec = ' запятая'
        for t in range(len(frac)):
            dec += ', ' + frac[t]
        return full + dec
    f_part = feminin(full)
    d_part = feminin(frac)

    if  d_part != '0' * len(d_part):    # Не читаем нули в начале
        while d_part[0] == '0':         # дробной части
            d_part = d_part[1:]
        if d_part[:2] == '_ ':
            d_part = d_part[2:]

    if cas == 0:
        if f_part[-1] == 'а':
            fp = 'ая'
        else:
            fp = 'ых'
        if d_part[-1] == 'а':
            dp = 'ая'
        else:
            dp = 'ых'
    elif cas == 1:
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
    elif cas == 2:
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
    elif cas == 3:
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
    elif cas == 4:
        f_part = cardinal(full, p_ca)
        if condition(full):
            f_part = f_part[:-1] + 'й'
            fp = 'ой'
        else:
            fp = 'ых'
        d_part = cardinal(frac, p_ca)
        if condition(frac):
            d_part = d_part[:-1] + 'й'
            dp = 'ой'
        else:
            dp = 'ых'
    else:
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
    return f_part + '_ цел' + fp + ' ' + d_part + dec + dp

