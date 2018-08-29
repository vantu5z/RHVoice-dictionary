#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Скрипт предварительной обработки текста для
# синтезатора речи RHVoice Ольги Яковлевой
# By Capricorn2001 & vantu5z

from re import sub, finditer

from .templates import (presamples, samples, patterns,
                        units, zh_units,
                        forms,
                        pre_acc,
                        i_mu, i_sr, i_zh, i_mn,
                        r_ca, r_mn, r_mu, r_sr, r_zh,
                        d_ca, d_mn, d_mu, d_sr, d_zh,
                        v_ca, v_zh,
                        t_ca, t_mn, t_mu, t_sr, t_zh,
                        p_ca, p_mn, p_mu, p_sr, p_zh,
                        adj_pad, mn_pad, mu_pad, sr_pad, zh_pad,
                        greekletters, letternames)
from .functions import (condition, cardinal, ordinal, roman2arabic,
                        substant, feminin, daynight, fraction)
from .words_forms import Words, M_GENDER, Z_GENDER, S_GENDER

# Для определения атрибутов слов
words = Words()


def text_prepare(text):
    """
    =================================
    Основная функция обработки текста
    =================================
    """

    # предварительная обработка текста
    for sample in presamples:
        text = sub(sample[0], sample[1], text)

    # =================
    # Единицы измерения
    # =================

    # Винительный падеж
    # например: "диаметром в 2 см -> диаметром в 2 сантиметра"
    mask = (r'\b([А-Яа-яё]{3,})'
            r'( (ориентировочно |примерно |приблизительно |)в )'
            r'((\d+,|)(\d+) - |)(\d+,|)(\d+)_' + units)
    for m in finditer(mask, text):
        if m.group(1).lower() in pre_acc:
            if m.group(4):
                if m.group(5):
                    number = fraction(m.group(5)[:-1], m.group(6), 5)
                else:
                    if condition(m.group(6)) and m.group(9) in zh_units:
                        number = feminin(m.group(6))[:-1] + 'у'
                    else:
                        number = m.group(6)
                number = number + ' - '
            else:
                number = ''
            if m.group(7):
                number += fraction(m.group(7)[:-1], m.group(8), 5) + ' '
                number += forms[m.group(9)][2]
            else:
                number += m.group(8) + ' ' + substant(m.group(8), m.group(9), 5)
            new = m.group(1) + m.group(2) + number
            text = text.replace(m.group(), new, 1)

    # Родительный падеж
    # пример: "С 5 см до -> С пяти сантиметров до"
    mask = (r'\b([Сс] (почти |примерно |приблизительно |плюс |минус |))'
            r'(\d+,|)(\d+)_' + units + ' до ')
    for m in finditer(mask, text):
        new = m.group(1)
        if m.group(3):
            new += fraction(m.group(3)[:-1], m.group(4), 1)
            new += ' ' + forms[m.group(5)][2]
        else:
            new += m.group(4)
            new += ' ' + substant(m.group(4), m.group(5), 1)
        text = text.replace(m.group(), new + ' до ', 1)

    # пример: "от 1 до 4 км -> от одного до четырёх километров"
    for m in finditer(r'\b([Оо]т |[Сс]о? )(\d+,|)(\d+)( до (\d+,|)\d+_)' + units, text):
        if m.group(2):
            number = fraction(m.group(2)[:-1], m.group(3), 1)
        else:
            number = cardinal(m.group(3), r_ca)
            if m.group(6) in zh_units:
                number = number[:-2] + 'й'
        new = m.group(1) + number + m.group(4) + m.group(6)
        text = text.replace(m.group(), new, 1)

    mask = (r'\b('
            r'[Бб]олее|[Мм]енее|[Бб]ольше|[Мм]еньше|[Вв]ыше|[Нн]иже|[Оо]коло|'
            r'[Сс]выше|[Дд]ля|[Дд]о|[Ии]з|[Оо]т|[Вв]место|[Вв] размере|'
            r'[Вв] течение|[Нн]ач[инаетсялоь]{2,7} с|'
            r'[Вв]ладел[аеимухцыь]{2,5}|[Дд]остиг[авеийлнотшщюуья]{,5}|'
            r'[Пп]ротив|[Пп]орядка|[Пп]осле'
            r')'
            r'( плюс | минус | )((\d+,|)(\d+)( - | или | и )'
            r'(плюс |минус |)|)(\d+,|)(\d+)_' + units)
    for m in finditer(mask, text):
        if m.group(3):
            if m.group(4):
                prenum = fraction(m.group(4)[:-1], m.group(5), 1)
            else:
                prenum = cardinal(m.group(5), r_ca)
                if condition(m.group(5)) and m.group(10) in zh_units:
                    prenum = prenum[:-2] + 'й'
            prenum += m.group(6) + m.group(7)
        else:
            prenum = ''
        if m.group(8):
            number = fraction(m.group(8)[:-1], m.group(9), 1) + ' ' + forms[m.group(10)][2]
        else:
            number = m.group(9) + ' ' + substant(m.group(9), m.group(10), 1)
        new = m.group(1) + m.group(2) + prenum  + number
        text = text.replace(m.group(), new, 1)

    # Дательный падеж
    mask = (r'\b('
            r'([Кк]|рав[нагеийлмоcуюыхья]{2,6})'
            r'( всего | почти | примерно | приблизительно | плюс | минус | )'
            r')'
            r'(\d+,|)(\d+)_' + units)
    for m in finditer(mask, text):
        if m.group(4):
            number = fraction(m.group(4)[:-1], m.group(5), 2) + ' ' + forms[m.group(6)][2]
        else:
            number = m.group(5) + ' ' + substant(m.group(5), m.group(6), 2)
        text = text.replace(m.group(), m.group(1) + number, 1)
    # С предлогом "по" при указании количества
    for m in finditer(r'\b([Пп]о (\d*1(000){0,3}))_' + units, text):
        new = m.group(1) + ' ' + substant(m.group(2), m.group(4), 2)
        text = text.replace(m.group(), new, 1)

    # Творительный падеж

    mask = (r'\b(([Мм]ежду|[Пп]о сравнению с|[Вв]ладе[авеийлмтюшщья]{1,7}) '
            r'(почти |приблизительно |примерно |плюс |минус |))'
            r'((\d+,|)(\d+)'
            r'( [-и] (почти |приблизительно |примерно |плюс |минус |))|)'
            r'(\d+,|)(\d+)_' + units)
    for m in finditer(mask, text):
        new = m.group(1)
        a = m.group(4) and not m.group(5)
        if a and condition(m.group(6)) and m.group(11) in zh_units:
            new += cardinal(m.group(6), t_ca)[:-2] + 'ой' + m.group(7)
        else:
            new += m.group(4)
        if m.group(9):
            new += fraction(m.group(9)[:-1], m.group(10), 3) + ' '
            new += forms[m.group(11)][2]
        else:
            new += m.group(10) + ' ' + substant(m.group(10), m.group(11), 3)
        text = text.replace(m.group(), new, 1)

    # Предложный падеж
    mask = (r'\b([Вв]|[Оо]б?|[Пп]ри)'
            r'(( плюс | минус | )(\d+,|)(\d+)( [-и] | или )| )'
            r'(почти |примерно |приблизительно |плюс |минус |)'
            r'(\d+,|)(\d+)_' + units)
    for m in finditer(mask, text):
        if m.group(2) == ' ':
            pre = ' '
        else:
            if m.group(4):
                pre = fraction(m.group(4)[:-1], m.group(5), 4) + ' ' + forms[m.group(10)][2]
            else:
                pre = m.group(5)
            pre = m.group(3) + pre + m.group(6)
        number = m.group(7)
        if m.group(8):
            number += fraction(m.group(8)[:-1], m.group(9), 4) + ' ' + forms[m.group(10)][2]
        else:
            number += m.group(9) + ' ' + substant(m.group(9), m.group(10), 4)
        text = text.replace(m.group(), m.group(1) + pre + number, 1)

    # Предлог "по" при указании количества
    for m in finditer(r'\b([Пп]о )(\d*[02-9]1|1)_' + units, text):
        new = m.group(1) + m.group(2) + ' ' + substant(m.group(2), m.group(3), 2)
        text = text.replace(m.group(), new, 1)

    # Именительный
    for m in finditer(r'\b(\d+,\d+)_' + units, text):
        new = m.group(1) + ' ' + forms[m.group(2)][2]
        text = text.replace(m.group(), new, 1)
    for m in finditer(r'\b(\d+)_' + units, text):
        new = m.group(1) + ' ' + substant(m.group(1), m.group(2))
        text = text.replace(m.group(), new, 1)

    mask = (r'('
            r'тысяч[аимх]{,3}|'
            r'(миллион|миллиард|триллион)(|ами|а[мх]?|ов)'
            r') ' + units)
    for m in finditer(mask, text):
        new = m.group(1) + ' ' + forms[m.group(4)][1]
        text = text.replace(m.group(), new, 1)

    # Время в формате (h)h ч (m)m мин
    for m in finditer(r'\b(\d{1,2}) ?ч ?(\d{1,2}) ?мин\b', text):
        if condition(m.group(1)): hours = ' час '
        elif m.group(1)[-1] in ('2', '3', '4'): hours = ' часа '
        else: hours = ' часов '
        if condition(m.group(2)): minutes = ' минута'
        elif m.group(2)[-1] in ('2', '3', '4'): minutes = ' минуты'
        else: minutes = ' минут'
        new = m.group(1) + hours + feminin(m.group(2)) + minutes
        text = text.replace(m.group(), new, 1)

    # Время в формате (ч)ч:мм/(ч)ч.мм

    for m in finditer(r'\b(([Вв]|[Нн]а) \d{1,2})[:.](\d\d)\b', text):
        minutes = feminin(m.group(3))
        if minutes[-2:] == 'на':
            minutes = minutes[:-1] + 'у'
        text = text.replace(m.group(), m.group(1) + ' ' + minutes, 1)

    for m in finditer(r'\b([Кк] )(\d{1,2})[:.](\d\d)\b', text):
        hours = cardinal(m.group(2), d_ca)
        minutes = cardinal(m.group(3), d_ca)
        if minutes[-2:] == 'му':
            minutes = minutes[:-2] + 'й'
        if m.group(3) == '00':
            minutes = '00'
        elif m.group(3)[0] == '0':
            minutes = '0_' + minutes
        text = text.replace(m.group(), m.group(1) + hours + ' ' + minutes, 1)

    mask = (r'\b([Дд]о |[Пп]осле |[Оо]коло |[Сс] )'
            r'(\d{1,2})[:.](\d\d)\b')
    for m in finditer(mask, text):
        hours = cardinal(m.group(2), r_ca)
        minutes = cardinal(m.group(3), r_ca)
        if minutes[-2:] == 'го':
            minutes = minutes[:-2] + 'й'
        if m.group(3) == '00':
            minutes = '00'
        elif m.group(3)[0] == '0':
            minutes = '0_' + minutes
        text = text.replace(m.group(), m.group(1) + hours + ' ' + minutes, 1)

    # =======================
    # Порядковые числительные
    # =======================

    # Чтение римских цифр в датах

    mask = (r'\b(([IVX]+)( (-|или|и|по)( в (конце |начале |середине |)| ))|)'
            r'([IVX]+)( в?в\.)')
    for m in finditer(mask, text):
        if m.group(1):
            pre = roman2arabic(m.group(2)) + m.group(3)
        else: pre = ''
        new = pre + roman2arabic(m.group(7)) + m.group(8)
        text = text.replace(m.group(), new, 1)

    mask = (r'\b([IVX]+)( [-и] )([IVX]+)'
            r'( век(ами?|ах?|ов)| (тысяче|сто)лети(ями?|ях?|й))\b')
    for m in finditer(mask, text):
        ending = m.group(4)[-1]
        if ending == 'а':
            num1 = ordinal(roman2arabic(m.group(1)), i_mu)
            num2 = ordinal(roman2arabic(m.group(3)), i_mu)
        elif ending == 'я':
            num1 = ordinal(roman2arabic(m.group(1)), i_sr)
            num2 = ordinal(roman2arabic(m.group(3)), i_sr)
        elif ending == 'в' or ending == 'й':
            num1 = ordinal(roman2arabic(m.group(1)), r_mu)
            num2 = ordinal(roman2arabic(m.group(3)), r_mu)
        elif ending == 'м':
            num1 = ordinal(roman2arabic(m.group(1)), d_mu)
            num2 = ordinal(roman2arabic(m.group(3)), d_mu)
        elif ending == 'и':
            num1 = ordinal(roman2arabic(m.group(1)), t_mu)
            num2 = ordinal(roman2arabic(m.group(3)), t_mu)
        else:
            num1 = ordinal(roman2arabic(m.group(1)), p_mu)
            num2 = ordinal(roman2arabic(m.group(3)), p_mu)
        text = text.replace(m.group(), num1 + m.group(2) + num2 + m.group(4), 1)

    # применение шаблонов
    for sample in samples:
        text = sub(sample[0], sample[1], text)

    # например: "во 2 окне -> во втором окне"
    mask = (r'\b([Вв]о?|[Оо]б?|[Пп]ри) '
            r'(\d*[02-9]|\d*1\d) ([а-яё]+)\b')
    for m in finditer(mask, text):
        attr = words.get_attr(m.group(3))
        number = ''
        if attr.have([S_GENDER, M_GENDER], False, [5]):
            number = ordinal(m.group(2), p_mu)
        elif attr.have([Z_GENDER], False, [2, 5]):
            number = ordinal(m.group(2), p_zh)
        if number:
            new = m.group(1) + number + ' ' + m.group(3)
            text = text.replace(m.group(), new, 1)

    # например: "со 2 примером -> со вторым примером"
    mask = (r'\b([Сс]о? )(\d*1\d|\d*[02-9]?[02-9]) ([а-яё]+)\b')
    for m in finditer(mask, text):
        number = ''
        attr = words.get_attr(m.group(3))
        if attr.have([M_GENDER, S_GENDER], False, [4]):
            number = ordinal(m.group(2), t_mu)
        elif attr.have([Z_GENDER], False, [2, 4, 5]):
            number = ordinal(m.group(2), t_zh)
        if number:
            new = m.group(1) + number + ' ' + m.group(3)
            text = text.replace(m.group(), new, 1)

    # например: "на 8-м этаже -> на восьмом этаже"
    for m in finditer(r'(\d+)-(м|й) ([а-яё]+)\b', text):
        number = ''
        attr = words.get_attr(m.group(3))
        if m.group(2) == 'м':
            if attr.have([M_GENDER, S_GENDER], None, [4]):
                number = ordinal(m.group(1), t_mu)
            elif attr.have([M_GENDER, S_GENDER], None, [5]):
                number = ordinal(m.group(1), p_mu)
        elif m.group(2) == 'й':
            if attr.have([Z_GENDER], False, [2, 4, 5]):
                number = ordinal(m.group(1), t_zh)
        if number:
            text = text.replace(m.group(), number + ' ' + m.group(3), 1)

    for m in finditer(r'(\d+)-е (([а-яё]+[ео]е ){,2}([а-яё]+[ео]))\b', text):
        if words.have(m.group(4), [S_GENDER], False, [0, 3]):
            new = ordinal(m.group(1), i_sr) + ' ' + m.group(2)
            text = text.replace(m.group(), new, 1)

    for m in finditer(r'\b(\d*11|\d*[05-9]) ([а-яё]+)\b', text):
        attr = words.get_attr(m.group(2))
        if attr.have([M_GENDER], False, [3]) and not attr.have(case=[0]):
            new = ordinal(m.group(1), r_mu) + ' ' + m.group(2)
            text = text.replace(m.group(), new, 1)

    for m in finditer(r'\b(\d*11|\d*[02-9]) ([а-яё]+)\b', text):
        if words.have(m.group(2), [Z_GENDER], False, [3]):
            new = ordinal(m.group(1), r_mu)[:-3] + 'ую ' + m.group(2)
            text = text.replace(m.group(), new, 1)

#    for m in finditer(r'(\d+)-ю ([а-яё]+)\b', text):
#        if words.have(m.group(2), [Z_GENDER], False, [3]):
#            new = ordinal(m.group(1), v_zh) + ' ' + m.group(2)
#            text = text.replace(m.group(), new)

    for pattern in patterns:
        for m in finditer(pattern[0], text):
            text = text.replace(m.group(), eval(pattern[1]), 1)

    # Прилагательные, в состав которых входят числительные (3-кратный и т.п.)
    mask = (r'\b((\d+) - |)(\d+)-'
            r'((долларов|рубл[её]в|часов|градусн|мерн|сильн|ствольн|'
            r'тонн|канальн|страничн|тысячн|миллионн|миллиардн|'
            r'процентн|секундн|минутн|месячн|недельн|дневн|дюймов|кратн|'
            r'местн|мильн|этажн|лет[ин]|микронн|(кило|милли|)граммов|'
            r'(кило|милли|санти|)метров)'
            r'([еиюя]|[иы]([ейх]|ми?)|[ая]я|[ую]ю|[ео]([ей]|го|му?)))\b')
    for m in finditer(mask, text):
        if m.group(1) == '': pre = ''
        else:
            if m.group(2)[-3:] == '000':
                pre = cardinal(m.group(2)[:-3], r_ca) + 'тысяче - '
            else: pre = cardinal(m.group(2), r_ca) + ' - '
        if m.group(3)[-3:] == '000':
            num = cardinal(m.group(3)[:-3], r_ca) + 'тысяче'
        else: num = cardinal(m.group(3), r_ca)
        num = pre + num
        num = sub('ста', 'сто', num)
        num = sub(r'(одной тысячи|одноготысяче)', 'тысяче', num)
        num = sub(r'\bодного', 'одно', num)
        text = text.replace(m.group(), num + '-' + m.group(4), 1)

    # Количественные числительные

    # Родительный падеж
    mask = (r'\b([Оо]т|[Сс])'
            r'( почти | примерно | приблизительно | плюс | минус | )'
            r'((\d+,|)(\d+)( [-и] | или )|)(\d+,|)(\d+)'
            r'('
            r' до( почти | примерно | приблизительно | плюс | минус | )'
            r'((\d+,|)\d+( [-и] | или )|)(\d+,|)\d+'
            r'( ([а-яё]+([иы]х|[ео]й|[ео]го) |и более |и менее |)([а-яё]+)|)'
            r')\b')
    for m in finditer(mask, text):
        if m.group(3):
            if m.group(4):
                pre = fraction(m.group(4)[:-1], m.group(5), 1)
            else:
                pre = cardinal(m.group(5), r_ca)
                if pre[-6:] == 'одного' and m.group(18) is not None:
                    if words.have(m.group(18), [Z_GENDER], None, [1]):
                        pre = pre[:-2] + 'й'
                    elif m.group(18) == 'суток':
                        pre = pre[:-3] + 'их'
            pre += m.group(6)
        else:
            pre = ''
        if m.group(7):
            number = fraction(m.group(7)[:-1], m.group(8), 1)
        else:
            number = cardinal(m.group(8), r_ca)
        if number[-6:] == 'одного' and m.group(18) is not None:
            if words.have(m.group(18), [Z_GENDER], None, [1]):
                number = number[:-2] + 'й'
            elif m.group(18) == 'суток':
                number = number[:-3] + 'их'
        new = m.group(1) + m.group(2) + pre + number + m.group(9)
        text = text.replace(m.group(), new, 1)

    mask = (r'\b('
            r'[Бб]олее|[Мм]енее|[Бб]ольше|[Мм]еньше|[Вв]ыше|[Нн]иже|[Дд]ороже|'
            r'[Дд]ешевле|[Оо]коло|[Сс]выше|[Сс]реди|[Дд]ля|[Дд]о|[Ии]з|[Оо]т|'
            r'[Бб]ез|[Уу]|[Вв]место|[Вв] возрасте|[Вв] размере|'
            r'[Вв] пределах|[Вв] течение|[Нн]а протяжении|'
            r'[Нн]ач[инаетялсьо]{2,7} с|[Пп]орядка|[Пп]осле|[Пп]ротив|'
            r'[Дд]остиг[авеийлнотшщюуья]{,5}|[Вв]ладел[аеимухцыь]{2,5}|'
            r'[Сс]тарше|[Мм]оложе|не превы[шаеситьло]{3,4}'
            r')'
            r'( следующих | примерно | приблизительно '
            r'| почти | плюс | минус | )'
            r'((\d+,|)(\d+)( - | или )|)(\d+,|)(\d+)'
            r'( ([а-яё]+([иы]х|[ео]й|[ео]го) |и более |и менее |)'
            r'([а-яё]{3,})|)\b')
    for m in finditer(mask, text):
        if m.group(3):
            if m.group(4):
                pre = fraction(m.group(4)[:-1], m.group(5), 1)
            else:
                pre = cardinal(m.group(5), r_ca)
            if condition(m.group(5)) and m.group(12) is not None:
                attr = words.get_attr(m.group(12))
                if m.group(9) and attr.have([Z_GENDER], None, [1]):
                    pre = pre[:-2] + 'й'
                elif m.group(12) == 'суток':
                    pre = pre[:-3] + 'их'
            pre += m.group(6)
        else:
            pre = ''
        if m.group(7):
            number = fraction(m.group(7)[:-1], m.group(8), 1)
        else:
            number = cardinal(m.group(8), r_ca)
            if m.group(12):
                attr = words.get_attr(m.group(12))
                if condition(m.group(8)) and attr.have(Z_GENDER, False, [1]):
                    number = number[:-2] + 'й'
                elif (m.group(9) and (attr.have(None, True, [1])
                      or m.group(12) == 'суток')):
                        number = cardinal(m.group(8), r_ca)
                        if m.group(12) == 'суток' and number[-6:] == 'одного':
                            number = number[:-3] + 'их'
        new = m.group(1) + m.group(2) + pre + number + m.group(9)
        text = text.replace(m.group(), new, 1)

    mask = (r'(\s|\A|\(| )((\d+) - |)(1|\d*[02-9]1)'
            r'(( [а-яё]+[ео](й|го) | )([а-яё]+))\b')
    for m in finditer(mask, text):
        attr = words.get_attr(m.group(8))
        if attr.have(None, False, [1]):
            number = cardinal(m.group(4), r_ca)
            if attr.have(gender=Z_GENDER):
                number = number[:-2] + 'й'
            if m.group(2) == '':
                pre = ''
            else:
                pre = cardinal(m.group(3), r_ca)
                if attr.have(gender=Z_GENDER) and number[-2:] == 'го':
                    pre = pre[:-2] + 'й'
                pre += ' - '
            new = m.group(1) + pre + number + m.group(5)
            text = text.replace(m.group(), new, 1)

    mask = (r'(\s|\A|\(| )((\d+)( [-и] | или )|)(\d*[02-9][234]|[234])'
            r'(( [а-яё]+[иы]х | )([а-яё]+))\b(.)')
    for m in finditer(mask, text):
        attr = words.get_attr(m.group(8))
        if attr.have(None, True, [1]):
            if m.group(2) == '':
                number = ''
            else:
                number = cardinal(m.group(3), r_ca) + m.group(4)
                if attr.have(gender=Z_GENDER) and number[-2:] == 'го':
                    number = number[:-2] + 'й'
            new = (m.group(1) + number + cardinal(m.group(5), r_ca) +
                   m.group(6) + m.group(9))
            text = text.replace(m.group(), new, 1)

    # Предлог "с" + родительный падеж множественного числа
    mask = (r'\b([Сс] )(\d+) ([а-яё]+)\b')
    for m in finditer(mask, text):
        attr = words.get_attr(m.group(3))
        if attr.have(None, True, [1]):
            new = m.group(1) + cardinal(m.group(2), r_ca) + ' ' + m.group(3)
            text = text.replace(m.group(), new, 1)

    # Творительный падеж
    # Исключение
    mask = (r'\b((состав(ил[аио]?|[ия]т|ля[ею]т)|потеря(л[аио]?|[ею]т)) \d+) '
            r'(погибшими|ранеными|убитыми)'
            r'(( и \d+) (погибшими|ранеными|убитыми)|)\b')
    for m in finditer(mask, text):
        if m.group(6):
            new = m.group(7) + '_' + m.group(8)
        else:
            new = ''
        new = m.group(1) + '_' + m.group(5) + new
        text = text.replace(m.group(), new, 1)

    mask = (r'(?<!\d,)\b('
            r'(\d+)'
            r'( - | или | и (почти |приблизительно |примерно |плюс |минус |))|'
            r')'
            r'(\d+) '
            r'([а-яё]+([аиыья]ми|[ео]м|[еиоы]й|ью))\b')
    for m in finditer(mask, text):
        if m.group(1):
            pre = cardinal(m.group(2), t_ca)
            if condition(m.group(2)):
                a = words.have(m.group(6), [Z_GENDER], False, [4])
                b = words.have(m.group(6)[:-2], [Z_GENDER], False, [0])
                c = words.have(m.group(6)[:-3] + 'ь', [Z_GENDER], False, [0])
                if a or b or c:
                    pre = pre[:-2] + 'ой'
            pre += m.group(3)
        else:
            pre = ''
        number = ''
        if condition(m.group(5)):
            attr = words.get_attr(m.group(6))
            if attr.have([M_GENDER, S_GENDER], False, [4]):
                number = cardinal(m.group(5), t_ca)
            elif attr.have([Z_GENDER], False, [4]):
                number = cardinal(m.group(5), t_ca)[:-2] + 'ой'
            elif m.group(6) == 'сутками':
                number = cardinal(m.group(5), t_ca) + 'и'
        elif m.group(6)[-2:] == 'ми':
            number = cardinal(m.group(5), t_ca)
        if number:
            new = pre + number + ' ' + m.group(6)
            text = text.replace(m.group(), new, 1)

    # Предлоги творительного падежа

    mask = (r'\b(([Мм]ежду|[Нн]ад|[Пп]еред|[Пп]о сравнению с) '
            r'(почти |приблизительно |примерно |плюс |минус |))'
            r'((\d+,|)(\d+)'
            r'( [-и] | или )'
            r'(почти |приблизительно |примерно |плюс |минус |)|)'
            r'(\d+,|)(\d+)\b')
    for m in finditer(mask, text):
        pre = m.group(1)
        if m.group(4):
            if m.group(5):
                pre += fraction(m.group(5)[:-1], m.group(6), 3)
            else:
                pre += cardinal(m.group(6), t_ca)
            pre = pre + m.group(7) + m.group(8)
        if m.group(9):
            number = fraction(m.group(9)[:-1], m.group(10), 3)
        else:
            number = cardinal(m.group(10), t_ca)
        text = text.replace(m.group(), pre + number, 1)

    # Предложный падеж
    mask = (r'\b([Вв]|[Нн]а|[Оо]б?|[Пп]ри)'
            r'('
            r'( почти | примерно | приблизительно | плюс | минус | )'
            r'(\d+)( [-и] | или )| '
            r')'
            r'(почти |примерно |приблизительно |плюс |минус |)(\d+)'
            r'( ([а-яё]+([иы]х|[ео]м) |)([а-яё]+([ая]х|е|и|у)))\b')
    for m in finditer(mask, text):
        if m.group(2) == ' ':
            pre = ' '
        else:
            pre = m.group(3) + cardinal(m.group(4), p_ca)
            a = words.have(m.group(11), None, False, [2, 5])
            b = words.have(m.group(11)[:-1] + 'м', [Z_GENDER], True, [2])
            if condition(m.group(4)) and (a or b):
                pre = pre[:-1] + 'й'
            elif m.group(11) == 'сутках':
                pre = pre[:-2] + 'их'
            pre += m.group(5)
        number = ''
        if m.group(12) == 'ах' or m.group(12) == 'ях':
            number = cardinal(m.group(7), p_ca)
        if condition(m.group(7)):
            attr = words.get_attr(m.group(11))
            if attr.have([M_GENDER, S_GENDER], False, [5]):
                number = cardinal(m.group(7), p_ca)
            elif attr.have([Z_GENDER], False, [2, 5]):
                number = cardinal(m.group(7), p_ca)[:-1] + 'й'
            elif m.group(11) == 'сутках':
                number = cardinal(m.group(7), p_ca)[:-2] + 'их'
        elif m.group(12) == 'ах' or m.group(12) == 'ях':
            number = cardinal(m.group(7), p_ca)
        if number:
            new = m.group(1) + pre + m.group(6) + number + m.group(8)
            text = text.replace(m.group(), new, 1)

    for m in finditer(r'\b(\d+) ([а-яё]+)\b', text):
        attr = words.get_attr(m.group(2))
        a = attr.have(None, True, [5])
        b = condition(m.group(1))
        c = attr.have([M_GENDER, S_GENDER], False, [5])
        if a or (b and c):
            new = cardinal(m.group(1), p_ca) + ' ' + m.group(2)
            text = text.replace(m.group(), new, 1)

    # Предлоги предложного падежа
    mask = (r'\b([Оо]б?|[Пп]ри)'
            r'( (\d+)( [-и] | или )| )(\d+)\b')
    for m in finditer(mask, text):
        number = ' '
        if m.group(2) != ' ':
            number += cardinal(m.group(3), p_ca) + m.group(4)
        new = m.group(1) + number + cardinal(m.group(5), p_ca)
        text = text.replace(m.group(), new, 1)

    # Женский род (иминетельный/винительный падежи)
    mask = (r'(\s|\A|\(| )(((\d+)( - | или | и ))|)(\d+)'
            r'(( [а-яё]+([ая]я|[иы][ех])|) ([а-яё]+))')
    for m in finditer(mask, text):
        attr = words.get_attr(m.group(10))
        a = attr.have([Z_GENDER], None, [1])
        b = attr.have([Z_GENDER], False, [0])
        if (a or b):
            if m.group(2) == '':
                pre = ''
            else:
                pre = feminin(m.group(4)) + m.group(5)
            new = m.group(1) + pre + feminin(m.group(6)) + m.group(7)
            text = text.replace(m.group(), new, 1)

    # Винительный падеж
    mask = (r'\b([Зз]а |[Пп]ро |[Чч]ерез |состав[аеилотя]{2,4} )'
            r'(\d+)'
            r'(( [а-яё]+([ая]я|[ую]ю|[ео]е|[иы][йх]) | )([а-яё]+))\b')
    for m in finditer(mask, text):
        number = cardinal(m.group(2), v_ca)
        if number[-3:] == 'дин':
            attr = words.get_attr(m.group(6))
            if attr.have([Z_GENDER], False, [3]):
                number = number[:-2] + 'ну'
            elif attr.have([S_GENDER], False, [0, 3]):
                number = number[:-2] + 'но'
        text = text.replace(m.group(), m.group(1) + number + m.group(3), 1)

    for m in finditer(r'\b([Нн]а )(\d+) ([а-яё]+)\b', text):
        if words.have(m.group(3), None, True, [1]):
            new = m.group(1) + cardinal(m.group(2), v_ca) + ' ' + m.group(3)
            text = text.replace(m.group(), new, 1)

#    for m in finditer(r'\b(\d*[02-9]1|1)(( [а-яё]+[ео]го | )([а-яё]+))\b', text):
#        if (words.have(m.group(4), [M_GENDER], False, [3])
#                and not words.have(m.group(4), [M_GENDER], False, [0])):
#            new = cardinal(m.group(1), v_ca)[:-2] + 'ного' + m.group(2)
#            text = text.replace(m.group(), new, 1)

    for m in finditer(r'\b(\d*[02-9]1|1)(( [а-яё]+[ую]ю | )([а-яё]+))', text):
        if words.have(m.group(4), [Z_GENDER], False, [3]):
            new = cardinal(m.group(1), v_ca)[:-2] + 'ну' + m.group(2)
            text = text.replace(m.group(), new, 1)

    mask = (r'\b(\d*[02-9][2-4]|[2-4])'
            r'(( [а-яё]+[иы]х | )([а-яё]+))')
    for m in finditer(mask, text):
        if words.have(m.group(4), [M_GENDER], True, [3]):
            number = cardinal(m.group(1), v_ca)
            if number[-3:] == 'два':
                number = number[:-1] + 'ух'
            else:
                number = number[:-1] + 'ёх'
            text = text.replace(m.group(), number + m.group(2), 1)

    for m in finditer(r'\b([Вв] )(\d+)( раз[а]?)\b', text):
        new = m.group(1) + cardinal(m.group(2), v_ca) + m.group(3)
        text = text.replace(m.group(), new, 1)

    mask = (r'([Сс]тои(т[ь]?|л[аио]?|вш[аеиймя]{2,3})) '
            r'(\d+) ([а-яё]+)\b')
    for m in finditer(mask, text):
        number = cardinal(m.group(3), v_ca)
        if number[-3:] == 'дин' and m.group(4) in ('копейку', 'гривну', 'драхму', 'марку'):
            number = number[:-2] + 'ну'
        elif number[-3:] == 'два' and m.group(4) in ('копейки', 'гривны', 'драхмы', 'марки'):
            number = number[:-1] + 'е'
        new = m.group(1) + ' ' + number + ' ' + m.group(4)
        text = text.replace(m.group(), new, 1)

    # Средний род (именительный/винительный падежи)
    for m in finditer(r'\b(\d*[02-9]1|1) (([а-яё]+[ео]е |)([а-яё]+[ео]))\b', text):
        if words.have(m.group(4), [S_GENDER], False, [0, 3]):
            if len(m.group(1)) > 1:
                if int(m.group(1)[:-1]) != 0:
                    number = m.group(1)[:-1] + '0_одно'
                else:
                    number = m.group(1)[:-1] + '_одно'
            else:
                number = m.group(1)[:-1] + 'одно'
            text = text.replace(m.group(), number + ' ' + m.group(2), 1)

    # Дательный падеж
    mask = (r'(?<!-)\b((\d+)( [-и] | или )|)(\d+)'
            r'(( [а-яё]+([иы]м|[ео]му) | )([а-яё]+([аиыя]м|у|ю|е)))\b')
    for m in finditer(mask, text):
        if m.group(1) == '':
            pre = ''
        else:
            pre = ' ' + cardinal(m.group(2), d_ca)
            attr = words.get_attr(m.group(8))
            a = attr.have([Z_GENDER], None, [2])
            b = attr.have([Z_GENDER], False, [5])
            if condition(m.group(2)) and (a or b):
                pre = pre[:-2] + 'й'
            elif m.group(8) == 'суткам':
                pre = pre[:-3] + 'им'
            pre += m.group(3)
        number = ''
        if condition(m.group(4)):
            if m.group(8)[-1] == 'у' or m.group(8)[-1] == 'ю':
                number = cardinal(m.group(4), d_ca)
            elif words.have(m.group(8), [Z_GENDER], False, [2, 5]):
                number = cardinal(m.group(4), d_ca)[:-2] + 'й'
            elif m.group(8) == 'суткам':
                number = cardinal(m.group(4), d_ca)[:-3] + 'им'
        elif m.group(9) == 'ам' or m.group(9) == 'ям':
            number = cardinal(m.group(4), d_ca)
        if number:
            text = text.replace(m.group(), pre + number + m.group(5), 1)

    # Предлоги дательного падежа
    mask = (r'\b([Кк]|рав[нагеийлмоcуюыхья]{2,6})'
            r'( (\d+)( [-и] | или )| )(\d+)\b')
    for m in finditer(mask, text):
        number = ' '
        if m.group(2) != ' ':
            number += cardinal(m.group(3), d_ca) + m.group(4)
        new = m.group(1) + number + cardinal(m.group(5), d_ca)
        text = text.replace(m.group(), new, 1)

    # Существует только во множественном числе
    for m in finditer(r'\b((\d+) - |)((\d+) (сутки|суток))', text):
        if m.group(1):
            pre = daynight(m.group(2), m.group(5)) + '-'
        else:
            pre = ''
        new = pre + daynight(m.group(4), m.group(5)) + ' ' + m.group(5)
        text = text.replace(m.group(), new, 1)

    # Предлог "по" при указании количества
    for m in finditer(r'\b([Пп]о )(\d*1(000){1,3})\b', text):
        new = m.group(1) + cardinal(m.group(2), d_ca)
        text = text.replace(m.group(), new, 1)

    # Десятичные дроби в именительном падеже
    for m in finditer(r'\b(\d+),(\d+)(\b|\Z)', text):
        new = fraction(m.group(1), m.group(2)) + m.group(3)
        text = text.replace(m.group(), new, 1)

    # Необязательная замена "_" (используется при обработке)
    text = sub('_', ' ', text)

    # Буквы греческого алфавита
    for j in greekletters:
        text = text.replace(j, letternames[greekletters.index(j)//2], 1)

    return text
