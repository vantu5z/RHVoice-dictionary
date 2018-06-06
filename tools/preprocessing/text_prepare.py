#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Скрипт предварительной обработки текста для
# синтезатора речи RHVoice Ольги Яковлевой
# By Capricorn2001 & vantu5z

from re import sub, finditer

from .templates import *
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

    for sample in presamples:
        text = sub(sample[0], sample[1], text)

    # Единицы измерения

    # Винительный падеж
    for m in finditer(r'\b([Дд]иаметр[аеуом]{,2}|[Рр]азниц[аейуы]{1,2}|[Вв]ысот[аейоуы]{1,2}|[Гг]лубин[аейоуы]{1,2}|[Дд]альност[иью]{1,2}|[Дд]альност[иью]{1,2} стрельбы|[Дд]истанци[яюией]{1,2}|[Дд]лин[аейоуы]{1,2}|[Мм]асс[аейоуы]{1,2}|[Шш]ирин[аейоуы]{1,2}|[Вв]ес[аемоу]{,2}|[Мм]ощност[иью]{1,2}|[Пп]лощад[иью]{1,2}|[Сс]корост[иью]{1,2}|[Сс]тоимост[иью]{1,2}|[Рр]асстояни[еимхюя]{1,2}|[Дд]лительност[иью]{1,2}|[Пп]родолжительност[иью]{1,2}|оцени[авеийлмстшыья]{,6}|[Уу]далени[еимюя]{1,2}) в( (\d+,|)(\d+) - | )(\d+,|)(\d+)_' + units, text):
        if m.group(2) == ' ':
            number = ''
        else:
            if m.group(3):
                number = fraction(m.group(3)[:-1], m.group(4), 5)
            else:
                if condition(m.group(4)) and m.group(7) in zh_units:
                    number = feminin(m.group(4))[:-1] + 'у'
                else:
                    number = m.group(4)
            number = number + ' - '
        if m.group(5):
            number += fraction(m.group(5)[:-1], m.group(6), 5) + ' ' + forms[m.group(7)][2]
        else:
            number += m.group(6) + ' ' + substant(m.group(6), m.group(7), 5)
        text = text.replace(m.group(), m.group(1) + ' в ' + number, 1)

    # Родительный падеж
    for m in finditer(r'\b([Сс] (почти |примерно |приблизительно |плюс |минус |))(\d+)_' + units + ' до ', text):
        text = text.replace(m.group(), m.group(1) + m.group(3) + ' ' + substant(m.group(3), m.group(4), 1) + ' до ', 1)
    for m in finditer(r'\b([Оо]т |[Сс]о? )(\d+,|)(\d+)( до (\d+,|)\d+_)' + units, text):
        if m.group(2) != '':
            number = fraction(m.group(2)[:-1], m.group(3), 1)
        else:
            number = cardinal(m.group(3), r_ca)
            if m.group(6) in zh_units:
                number = number[:-2] + 'й'
        text = text.replace(m.group(), m.group(1) + number + m.group(4) + m.group(6), 1)
    for m in finditer(r'\b([Бб]олее|[Мм]енее|[Бб]ольше|[Мм]еньше|[Вв]ыше|[Нн]иже|[Оо]коло|[Сс]выше|[Дд]ля|[Дд]о|[Ии]з|[Оо]т|[Вв]место|[Вв] размере|[Вв] течение|[Нн]ач[инаетсялоь]{2,7} с|[Вв]ладел[аеимухцыь]{2,5}|[Дд]остиг[авеийлнотшщюуья]{,5}|[Пп]ротив|[Пп]орядка|[Пп]осле)( плюс | минус | )((\d+,|)(\d+)( - | или | и )(плюс |минус |)|)(\d+,|)(\d+)_' + units, text):
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
        text = text.replace(m.group(), m.group(1) + m.group(2) + prenum  + number, 1)

    # Дательный падеж
    for m in finditer(r'\b(([Кк]|рав[нагеийлмоcуюыхья]{2,6})( почти | примерно | приблизительно | плюс | минус | ))(\d+,|)(\d+)_' + units, text):
        if m.group(4):
            number = fraction(m.group(4)[:-1], m.group(5), 2) + ' ' + forms[m.group(6)][2]
        else:
            number = m.group(5) + ' ' + substant(m.group(5), m.group(6), 2)
        text = text.replace(m.group(), m.group(1) + number, 1)

    # Творительный падеж
    for m in finditer(r'\b(([Сс]|[Вв]ладе[авеийлмтюшщья]{1,7})( почти | приблизительно | примерно | плюс | минус | ))(\d+,|)(\d+)_' + units, text):
        if m.group(4):
            number = fraction(m.group(4)[:-1], m.group(5), 3) + ' ' + forms[m.group(6)][2]
        else:
            number = m.group(5) + ' ' + substant(m.group(5), m.group(6), 3)
        text = text.replace(m.group(), m.group(1) + number, 1)
    for m in finditer(r'([Мм]ежду( почти | приблизительно | примерно | плюс | минус | ))(\d+,|)(\d+)( и( почти | приблизительно | примерно | плюс | минус | ))(\d+,|)(\d+)_' + units, text):
        if m.group(3):
            prenum = fraction(m.group(3)[:-1], m.group(4), 3)
        else:
            prenum = cardinal(m.group(4), t_ca)
            if condition(m.group(4)) and m.group(9) in zh_units:
                prenum = prenum[:-2] + 'ой'
        if m.group(7):
            number = fraction(m.group(7)[:-1], m.group(8), 3) + ' ' + forms[m.group(9)][2]
        else:
            number = m.group(8) + ' ' + substant(m.group(8), m.group(9), 3)
        text = text.replace(m.group(), m.group(1) + prenum + m.group(5) + number, 1)

    # Предложный падеж
    for m in finditer(r'\b([Вв]|[Оо]б?|[Пп]ри)(( плюс | минус | )(\d+,|)(\d+)( [-и] | или )| )(почти |примерно |приблизительно |плюс |минус |)(\d+,|)(\d+)_' + units, text):
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

    for m in finditer(r'(тысяч[аимх]{,3}|(миллион|миллиард|триллион)(|ам?|ами|ов)) ' + units, text):
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

    for m in finditer(r'\b([Дд]о |[Пп]осле |[Оо]коло |[Сс] )(\d{1,2})[:.](\d\d)\b', text):
        hours = cardinal(m.group(2), r_ca)
        minutes = cardinal(m.group(3), r_ca)
        if minutes[-2:] == 'го':
            minutes = minutes[:-2] + 'й'
        if m.group(3) == '00':
            minutes = '00'
        elif m.group(3)[0] == '0':
            minutes = '0_' + minutes
        text = text.replace(m.group(), m.group(1) + hours + ' ' + minutes, 1)

    # Порядковые числительные

    for m in finditer(r'\b(([IVXCDLM]+)( ?- ?(начале |середине |конце )| (и|или)( | в ))|)([IVXCDLM]+) ([в]?в\.|век[аеуовмих]{,3}\b|(сто|тысяче)лети[ейяюмих]{1,3}\b|[Сс]ъезд[аеуовмих]{,3}\b|квартал[аеуыовмих]{,3}\b)', text):
        if m.group(1) == '':
            part1 = ''
        else:
            part1 = roman2arabic(m.group(2)) + m.group(3)
        new = part1 + roman2arabic(m.group(7)) + ' ' + m.group(8)
        text = text.replace(m.group(), new, 1)

    for sample in samples:
        text = sub(sample[0], sample[1], text)

    # например: "во 2 окне -> во втором окне"
    for m in finditer(r'\b([Вв]о? |[Оо]б? |[Пп]ри )(\d*[02-9]|\d*1\d) ([а-яё]+)\b', text):
        attr = words.get_attr(m.group(3))
        number = ''
        if attr.have([S_GENDER, M_GENDER], False, [5]):
            number = ordinal(m.group(2), p_mu)
        elif attr.have([Z_GENDER], False, [2, 5]):
            number = ordinal(m.group(2), p_zh)
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
            text = text.replace(m.group(), new)

    for m in finditer(r'\b(\d*11|\d*[02-9]) ([а-яё]+)\b', text):
        if words.have(m.group(2), [Z_GENDER], False, [3]):
            new = ordinal(m.group(1), r_mu)[:-3] + 'ую ' + m.group(2)
            text = text.replace(m.group(), new)

#    for m in finditer(r'(\d+)-ю ([а-яё]+)\b', text):
#        if words.have(m.group(2), [Z_GENDER], False, [3]):
#            new = ordinal(m.group(1), v_zh) + ' ' + m.group(2)
#            text = text.replace(m.group(), new)

    for pattern in patterns:
        for m in finditer(pattern[0], text):
            text = text.replace(m.group(), eval(pattern[1]), 1)

    # Количественные числительные
    for m in finditer(r'\b((\d+) - |)(\d+)-(часов[агеиймоухыюя]{2,3}|(градус|силь|стволь|тон|каналь|странич|тысяч|миллион|миллиард|процент|секунд|минут|месяч|недель|днев|крат|мест|миль|этаж)н[агеиймоухыюя]{2,3}|лет[геиймноухюя]{2,4}|(|кило|милли|санти)(граммов|метров)[агеиймоухыюя]{2,3})\b', text):
        if m.group(1) == '':
            pre = ''
        else:
            if m.group(2)[-3:] == '000':
                pre = cardinal(m.group(2)[:-3], r_ca) + 'тысяче - '
            else:
                pre = cardinal(m.group(2), r_ca) + ' - '
        if m.group(3)[-3:] == '000':
            num = cardinal(m.group(3)[:-3], r_ca) + 'тысяче'
        else:
            num = cardinal(m.group(3), r_ca)
        num = pre + num
        num = sub(r'ста', 'сто', num)
        num = sub(r'(одной тысячи|одноготысяче)', 'тысяче', num)
        num = sub(r'\bодного', 'одно', num)
        text = text.replace(m.group(), num + '-' + m.group(4), 1)

    # Творительный падеж
    for m in finditer(r'((\d+)( - | или | и )|)(плюс |минус |)(\d+) ([а-яё]+([аиыья]ми|[ео]м|[еиоы]й|ью))\b', text):
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
            new = pre + m.group(4) + number + ' ' + m.group(6)
            text = text.replace(m.group(), new, 1)

    # Предлоги творительного падежа
    for m in finditer(r'\b([Нн]ад|[Пп]еред|[Пп]о сравнению с)( (\d+)( [-и] | или )| )(\d+)\b', text):
        number = ' '
        if m.group(2) != ' ':
            number += cardinal(m.group(3), t_ca) + m.group(4)
        new = m.group(1) + number + cardinal(m.group(5), t_ca)
        text = text.replace(m.group(), new, 1)

    # Родительный падеж
    for m in finditer(r'\b([Оо]т|[Сс])( почти | примерно | приблизительно | плюс | минус | )((\d+,|)(\d+)( [-и] | или )|)(\d+,|)(\d+)( до( почти | примерно | приблизительно | плюс | минус | )((\d+,|)\d+( [-и] | или )|)(\d+,|)\d+( ([а-яё]+([иы]х|[ео]й|[ео]го) |и более |и менее |)([а-яё]+)|))\b', text):
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

    for m in finditer(r'\b([Бб]олее|[Мм]енее|[Бб]ольше|[Мм]еньше|[Вв]ыше|[Нн]иже|[Дд]ороже|[Дд]ешевле|[Оо]коло|[Сс]выше|[Сс]реди|[Дд]ля|[Дд]о|[Ии]з|[Оо]т|[Бб]ез|[Сс]|[Уу]|[Вв]место|[Вв] возрасте|[Вв] размере|[Вв] пределах|[Вв] течение|[Нн]а протяжении|[Нн]ач[инаетялсьо]{2,7} с|[Пп]орядка|[Пп]осле|[Пп]ротив|[Дд]остиг[авеийлнотшщюуья]{,5}|[Вв]ладел[аеимухцыь]{2,5}|[Сс]тарше|[Мм]оложе|не превы[шаеситьло]{3,4})( примерно | приблизительно | почти | плюс | минус | )((\d+,|)(\d+)( - | или )|)(\d+,|)(\d+)( ([а-яё]+([иы]х|[ео]й|[ео]го) |и более |и менее |)([а-яё]+)|)\b', text):
        if m.group(2)[1:-1] not in ("них", "которых"):
            if m.group(3) == '':
                pre = ''
            else:
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
            if m.group(7):
                number = fraction(m.group(7)[:-1], m.group(8), 1)
            else:
                number = cardinal(m.group(8), r_ca)
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

    for m in finditer(r'(\s|\A|\(| )((\d+) - |)(1|\d*[02-9]1)(( [а-яё]+[ео](й|го) | )([а-яё]+))\b', text):
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

    for m in finditer(r'(\s|\A|\(| )((\d+)( [-и] | или )|)(\d*[02-9][234]|[234])(( [а-яё]+[иы]х | )([а-яё]+))\b(.)', text):
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

    # Предложный падеж
    for m in finditer(r'\b([Вв]|[Нн]а|[Оо]б?|[Пп]ри)(( почти | примерно | приблизительно | плюс | минус | )(\d+)( [-и] | или )| )(почти |примерно |приблизительноплюс |минус |)(\d+)( ([а-яё]+([иы]х|[ео]м) |)([а-яё]+([ая]х|е|и|у)))\b', text):
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

    # Предлоги предложного падежа
    for m in finditer(r'\b([Оо]б?|[Пп]ри)( (\d+)( [-и] | или )| )(\d+)\b', text):
        number = ' '
        if m.group(2) != ' ':
            number += cardinal(m.group(3), p_ca) + m.group(4)
        new = m.group(1) + number + cardinal(m.group(5), p_ca)
        text = text.replace(m.group(), new, 1)

    # Женский род (иминетельный/винительный падежи)
    for m in finditer(r'(\s|\A|\(| )(((\d+)( - | или | и ))|)(\d+)(( [а-яё]+([ая]я|[иы][ех])|) ([а-яё]+))', text):
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
    for m in finditer(r'\b([Зз]а |[Пп]ро |[Чч]ерез |состав[аеилотя]{2,4} )(\d+)(( [а-яё]+([ая]я|[ую]ю|[ео]е|[иы][йх]) | )([а-яё]+))\b', text):
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

    for m in finditer(r'\b(\d*[02-9]1|1)(( [а-яё]+[ео]го | )([а-яё]+))\b', text):
        if words.have(m.group(4), [M_GENDER], False, [3]):
            new = cardinal(m.group(1), v_ca)[:-2] + 'ного' + m.group(2)
            text = text.replace(m.group(), new, 1)

    for m in finditer(r'\b(\d*[02-9]1|1)(( [а-яё]+[ую]ю | )([а-яё]+))', text):
        if words.have(m.group(4), [Z_GENDER], False, [3]):
            new = cardinal(m.group(1), v_ca)[:-2] + 'ну' + m.group(2)
            text = text.replace(m.group(), new, 1)

    for m in finditer(r'\b(\d*[02-9][2-4]|[2-4])(( [а-яё]+[иы]х | )([а-яё]+))', text):
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

    for m in finditer(r'([Сс]тои(т[ь]?|л[аио]?|вш[аеиймя]{2,3})) (\d+) ([а-яё]+)\b', text):
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
    for m in finditer(r'((\d+)( [-и] | или )|)(\d+)(( [а-яё]+([иы]м|[ео]му) | )([а-яё]+([аиыя]м|у|ю|е)))\b', text):
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
    for m in finditer(r'\b([Кк]|рав[нагеийлмоcуюыхья]{2,6})( (\d+)( [-и] | или )| )(\d+)\b', text):
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
