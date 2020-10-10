#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# В этом файле определены правила.

from re import finditer, sub

from .templates import (units, zh_units,
                        forms,
                        pre_acc,
                        i_mu, i_sr, i_zh, i_mn,
                        r_ca, r_mn, r_mu, r_sr, r_zh,
                        d_ca, d_mn, d_mu, d_sr, d_zh,
                        v_ca, v_zh,
                        t_ca, t_mn, t_mu, t_sr, t_zh,
                        p_ca, p_mn, p_mu, p_sr, p_zh,
                        adj_pad, mn_pad, mu_pad, sr_pad, zh_pad)
from .functions import (condition, cardinal, ordinal, roman2arabic, replace,
                        substant, feminin, daynight, decimal)
from .words_forms import Words, M_GENDER, Z_GENDER, S_GENDER

# Для определения атрибутов слов
words = Words()


class RuleBase():
    """
    Базовый класс.
    """
    def __init__(self):
        self.mask = ''       # регулярное выражение для поиска (маска)

    def run(self, text, debug=False):
        """
        Применение правила к тексту.
        """
        length = len(text)
        for m in finditer(self.mask, text):
            new = self.check(m)
            if new is not None:
                text = replace(text, new, length, m.start(), m.end())
                if debug:
                    print('Сработало правило: %s' % self.__class__.__name__)
                    print('     найдено: "%s"\n'
                          '    заменено: "%s"\n' % (m, new))
        return text

    def check(self, m):
        """
        Проверка и обработка найденных совпадений по маске.
        Должна возвращать строку для замены найденной или None.
        """
        pass


class QuasiRoman(RuleBase):
    """
    Описание: Часто вместо латиницы встречается кириллица.
    Пример:
    """
    def __init__(self):
        self.mask = (r'\b((([ІХ]+)( [-и] | или )|)([ІХ]+))'
                     r'( (в?в\.|век[аеу]?|веках|веками?|'
                     r'(сто|тысяче)лети(ем?|й|ю|ях?|ями?))|)\b')

    def check(self, m):
        new = m.group(1)
        if m.group(2) or m.group(6) or ('ХХ' or 'І' in m.group(1)):
            new = sub('І', 'I', new)
            new = sub('Х', 'X', new)
            return new + m.group(6)
        return None


class UnitRule_0(RuleBase):
    """
    Описание: Количественные числительные. Винительный падеж.
    Пример: "в 2 тыс. раз -> в 2 тысячи раз"
    """
    def __init__(self):
        self.mask = (r'\b([Вв] ((\d+,|)(\d+) - |)'
                     r'(\d+,|)(\d+)) (тыс\.|млн|млрд|трлн)( раз)\b')

    def check(self, m):
        new = m.group(1) +' '
        if m.group(5):
            new += forms[m.group(7)][2]
        else:
            new += substant(m.group(6), m.group(7), 5)
        return new + m.group(8)


class UnitRule_1(RuleBase):
    """
    Описание: Единицы измерения. Винительный падеж.
    Пример:
    """
    def __init__(self):
        self.mask = (
            r'\b(([Зз]а|[Нн]а|[Пп]ро|[Сс]пустя|[Чч]ерез|'
            r'состав[авеийлотшщьюя]{2,6}|превы[сш][авеийлотшщьюя]{2,5}) (бы |)'
            r'((\d+,|)(\d+) - |)(\d+,|)(\d+)) ' + units)

    def check(self, m):
        new = m.group(1) + ' '
        if m.group(7):
            new += forms[m.group(9)][2]
        else:
            new += substant(m.group(8), m.group(9), 5)
        return new


class UnitRule_2(RuleBase):
    """
    Описание: Единицы измерения. Винительный падеж.
    Пример: "диаметром в 2 см -> диаметром в 2 сантиметра"
    """
    def __init__(self):
        self.mask = (
            r'\b([А-Яа-яё]{3,})'
            r'( (всего |ориентировочно |примерно |приблизительно |более чем |'
            r'не более чем |стрельбы |заказчику |заказчикам |покупателю |'
            r'покупателям |)в '
            r'((\d+,|)(\d+) - |)(\d+,|)(\d+)) ' + units)

    def check(self, m):
        preacc = sub('ё', 'е', m.group(1).lower())
        if preacc not in pre_acc:
            return None
        new = m.group(1) + m.group(2) + ' '
        if m.group(7):
            new += forms[m.group(9)][2]
        else:
            new += substant(m.group(8), m.group(9), 5)
        return new


class UnitRule_3(RuleBase):
    """
    Описание: Единицы измерения. Родительный падеж.
    Пример: "от 1 до 4 км -> от 1 до 4 километров"
    """
    def __init__(self):
        self.mask = (r'\b([Оо]т |[Сс] )(((\d+,|)\d+ - |)(\d+,|)\d+ '
                     r'до ((\d+,|)\d+ - |)(\d+,|)(\d+) )' + units)

    def check(self, m):
        if m.group(8):
            new = forms[m.group(10)][2]
        else:
            new = substant(m.group(9), m.group(10), 1)
        return m.group(1) + m.group(2) + new


class UnitRule_4(RuleBase):
    """
    Описание: Единицы измерения. Родительный падеж.
    Пример:
    """
    def __init__(self):
        self.mask = (
            r'\b('
            r'[Бб]олее|[Мм]енее|[Бб]ольше|[Мм]еньше|[Вв]ыше|[Нн]иже|[Дд]альше|'
            r'[Оо]коло|[Сс]выше|[Дд]ля|[Дд]о|[Ии]з|[Оо]т|[Вв]место|[Дд]линнее|'
            r'[Вв] размере|[Бб]лиже|[Вв] течение|[Вв] количестве|'
            r'[Вв]ладел[аеимухцыь]{2,5}|[Дд]остиг[авеийлнотшщюуья]{,5}|'
            r'[Пп]ротив|[Пп]орядка|[Пп]осле|[Ээ]тих [а-яё]+[иы]х|[Ээ]тих|'
            r'[Нн]е превы[сш][аи][авеийолтшщюья]{1,4}'
            r')'
            r'( плюс | минус | более чем | менее чем | )'
            r'((\d+,|)(\d+)( - | или | и )'
            r'(плюс |минус |)|)(\d+,|)(\d+) ' + units)

    def check(self, m):
        if m.group(3):
            if m.group(4):
                prenum = decimal(m.group(4)[:-1], m.group(5), 1)
            else:
                prenum = cardinal(m.group(5), r_ca)
                if condition(m.group(5)) and m.group(10) in zh_units:
                    prenum = prenum[:-2] + 'й'
            prenum += m.group(6) + m.group(7)
        else:
            prenum = ''
        if m.group(8):
            number = decimal(m.group(8)[:-1], m.group(9), 1)
            number += ' ' + forms[m.group(10)][2]
        else:
            number = cardinal(m.group(9), r_ca)
            if condition(m.group(9)) and m.group(10) in zh_units:
                number = number[:-2] + 'й'
            number += ' ' + substant(m.group(9), m.group(10), 1)
        return m.group(1) + m.group(2) + prenum  + number


class UnitRule_5(RuleBase):
    """
    Описание: Единицы измерения. Родительный падеж.
    Пример: "С 10 кВт до 12 -> С десяти киловатт до двенадцати"
    """
    def __init__(self):
        self.mask = (
            r'\b(([Оо]т|[Сс]) '
            r'(почти |примерно |приблизительно |плюс |минус |'
            r'более чем |менее чем|))'
            r'((\d+,|)(\d+) - |)(\d+,|)(\d+) '
            r'([%°\℃ВКМ£₽\$\.²³_БВГМагдеклмнпрстцш\']+)'
            r'( (в час |в секунду |[а-яё]{3,} |)до '
            r'(почти |примерно |приблизительно |плюс |минус |'
            r'более чем |менее чем|))(((\d+,|)(\d+) - |)(\d+,|)(\d+)|)\b')

    def check(self, m):
        if m.group(9) in ('%', '°', "'", '℃', 'В', 'К', 'М', '£', '₽', '$',
                          'кГц', 'МГц', 'ГГц', 'Гц', 'кпк', 'Мпк', 'Гпк', 'пк',
                          'кг', 'мг', '_г', 'мкм', 'км', 'см', 'мм', 'м',
                          'км²', 'см²', 'мм²', 'м²', 'км³', 'см³', 'мм³', 'м³',
                          'кт', 'Мт', 'т', 'кВт', 'МВт', 'ГВт', 'Вт', 'га', 'л',
                          'дБ', 'сек', 'л.с.', 'а.е.', 'шт.', 'ед.', 'тыс.',
                          'млн', 'млрд', 'трлн', 'атм'):
            number1 = ''
            if m.group(4):
                if m.group(5):
                    number1 = decimal(m.group(5)[:-1], m.group(6), 1)
                else:
                    number1 = cardinal(m.group(6), r_ca)
                    if m.group(9) in zh_units and condition(m.group(6)):
                        number1 = number1[:-2] + 'й'
                number1 += ' - '
            else:
                number1 = ''
            if m.group(7):
                number1 += decimal(m.group(7)[:-1], m.group(8), 1)
                number1 += ' ' + forms[m.group(9)][2]
            else:
                number1 += cardinal(m.group(8), r_ca)
                if m.group(9) in zh_units and condition(m.group(8)):
                    number1 = number1[:-2] + 'й'
                number1 += ' ' + substant(m.group(8), m.group(9), 1)
            if m.group(13):
                if m.group(14):
                    if (not m.group(15) and m.group(9) in zh_units
                        and condition(m.group(16))):
                        number2 = cardinal(m.group(16), r_ca)[:-2] + 'й'
                        number2 += ' - '
                    else:
                        number2 = m.group(14)
                else:
                    number2 = ''
                if m.group(17):
                    number2 += decimal(m.group(17)[:-1], m.group(18), 1)
                else:
                    number2 += cardinal(m.group(18), r_ca)
                    if m.group(9) in zh_units and condition(m.group(18)):
                        number2 = number2[:-2] + 'й'
            else:
                number2 = ''
            return m.group(1) + number1 + m.group(10) + number2
        else:
            return None


class UnitRule_6(RuleBase):
    """
    Описание: Единицы измерения. Дательный падеж.
    Пример:
    """
    def __init__(self):
        self.mask = (
            r'\b(([Кк]|равна|равн[оы][ей]?|равен'
            r'|равняться|равнял[аио]сь|равнялся|равняется)'
            r'( всего | почти | примерно | приблизительно | плюс | минус | )'
            r')'
            r'(\d+,|)(\d+) ' + units)

    def check(self, m):
        if m.group(4):
            number = decimal(m.group(4)[:-1], m.group(5), 2)
            number += ' ' + forms[m.group(6)][2]
        else:
            number = m.group(5) + ' ' + substant(m.group(5), m.group(6), 2)
        return m.group(1) + number



class UnitRule_7(RuleBase):
    """
    Описание: Единицы измерения. Дательный падеж.
              С предлогом "по" при указании количества.
    Пример:
    """
    def __init__(self):
        self.mask = (r'\b([Пп]о (\d*[02-9]1|1(000){0,3})) ' + units)

    def check(self, m):
        return m.group(1) + ' ' + substant(m.group(2), m.group(4), 2)


class UnitRule_8(RuleBase):
    """
    Описание: Единицы измерения. Творительный падеж.
    Пример:
    """
    def __init__(self):
        self.mask = (
            r'\b(([Мм]ежду|[Нн]ад|[Сс]|[Вв]ладе[авеийлмтюшщья]{1,7}|'
            r'[Пп]о сравнению со?|[Вв] сравнении со?) '
            r'(более чем |почти |приблизительно |примерно |плюс |минус |))'
            r'((\d+,|)(\d+)'
            r'( [-и] (почти |приблизительно |примерно |плюс |минус |))|)'
            r'(\d+,|)(\d+) ' + units)

    def check(self, m):
        new = m.group(1)
        a = m.group(4) and not m.group(5)
        if a and condition(m.group(6)) and m.group(11) in zh_units:
            new += cardinal(m.group(6), t_ca)[:-2] + 'ой' + m.group(7)
        else:
            new += m.group(4)
        if m.group(9):
            new += decimal(m.group(9)[:-1], m.group(10), 3) + ' '
            new += forms[m.group(11)][2]
        else:
            new += m.group(10) + ' ' + substant(m.group(10), m.group(11), 3)
        return new


class UnitRule_9(RuleBase):
    """
    Описание: Единицы измерения. Предложный падеж.
    Пример:
    """
    def __init__(self):
        self.mask = (
            r'\b(([Вв]|[Оо]б?|[Пп]ри) '
            r'((около |почти |приблизительно |примерно |плюс |минус |)'
            r'(\d+,|)(\d+) ([-и]|или) |)'
            r'(около |почти |приблизительно |примерно |плюс |минус |)'
            r'(\d+,|)(\d+)) ' + units
            )

    def check(self, m):
        if m.group(9):
            pre = forms[m.group(11)][2]
        else:
            pre = substant(m.group(10), m.group(11), 4)
        return m.group(1) + ' ' + pre


class UnitRule_11(RuleBase):
    """
    Описание: Единицы измерения. Именительный падеж.
    Пример:
    """
    def __init__(self):
        self.mask = (r'\b(((\d+),|)(\d+)) ' + units)

    def check(self, m):
        if m.group(2):
            return m.group(1) + ' ' + forms[m.group(5)][2]
        else:
            return m.group(1) + ' ' + substant(m.group(4), m.group(5))


class UnitRule_12(RuleBase):
    """
    Описание: Единицы измерения. Именительный падеж.
    Пример:
    """
    def __init__(self):
        self.mask = (
            r'('
            r'-й степени|тысяч(|ами|а[мх]?|ей?|и|у)|'
            r'(миллион|миллиард|триллион)(|ами|а[мх]?|о[вм]|[еу])'
            r') ' + units)

    def check(self, m):
        return m.group(1) + ' ' + forms[m.group(5)][1]


class TimeRule_1(RuleBase):
    """
    Описание: Время в формате (h)h ч (m)m мин.
    Пример:
    """
    def __init__(self):
        self.mask = (r'\b([012]?\d) ?ч ?([0-5]?\d) ?мин\b')

    def check(self, m):
        if condition(m.group(1)):
            hours = ' час '
        elif m.group(1) in ('2', '3', '4', '02', '03', '04', '22', '23', '24'):
            hours = ' часа '
        else:
            hours = ' часов '
        if condition(m.group(2)):
            minutes = ' минута'
        elif m.group(2) in ('2', '3', '4', '02', '03', '04',
                            '22', '23', '24', '32', '33', '34',
                            '42', '43', '44', '52', '53', '54'):
            minutes = ' минуты'
        else:
            minutes = ' минут'
        return m.group(1) + hours + feminin(m.group(2)) + minutes


class TimeRule_2(RuleBase):
    """
    Описание: Время в формате (ч)ч:мм/(ч)ч.мм
    Пример:
    """
    def __init__(self):
        self.mask = (r'\b(([Вв]|[Нн]а) [012]?\d)[:.]([0-5]\d)(?!\.\d)')

    def check(self, m):
        return m.group(1) + ' ' + feminin(m.group(3), 5) + '_'


class TimeRule_3(RuleBase):
    """
    Описание: Время в формате (ч)ч:мм/(ч)ч.мм
    Пример:
    """
    def __init__(self):
        self.mask = (r'\b([Кк] )([012]?\d)[:.]([0-5]\d)(?!\.\d)')

    def check(self, m):
        hours = cardinal(m.group(2), d_ca)
        minutes = cardinal(m.group(3), d_ca)
        if m.group(3) == '00':
            minutes = '00'
        else:
            if m.group(3)[0] == '0':
                minutes = '0_ ' + minutes
            minutes = feminin(minutes, 2)
        return m.group(1) + hours + ' ' + minutes


class TimeRule_4(RuleBase):
    """
    Описание: Время в формате (ч)ч:мм/(ч)ч.мм
    Пример:
    """
    def __init__(self):
        self.mask = (
            r'\b([Дд]о |[Пп]осле |[Оо]коло |[Сс] )'
            r'([012]?\d)[:.]([0-5]\d)(?!\.\d)')

    def check(self, m):
        hours = cardinal(m.group(2), r_ca)
        minutes = cardinal(m.group(3), r_ca)
        if m.group(3) == '00':
            minutes = '00'
        else:
            if m.group(3)[0] == '0':
                minutes = '0_ ' + minutes
            minutes = feminin(minutes, 1)
        return m.group(1) + hours + ' ' + minutes


class RomanRule_1(RuleBase):
    """
    Описание: Римские цифры.
    Пример:
    """
    def __init__(self):
        self.mask = (
            r'\b(([IVX]+)( (-|или|и|по)( в (конце |начале |середине |)| ))|)'
            r'([IVX]+)( в?в\.)')

    def check(self, m):
        if m.group(1):
            pre = roman2arabic(m.group(2)) + m.group(3)
        else: pre = ''
        return pre + roman2arabic(m.group(7)) + m.group(8)


class RomanRule_2(RuleBase):
    """
    Описание: Римские цифры.
    Пример:
    """
    def __init__(self):
        self.mask = (
            r'\b([IVX]+)( [-и] )([IVX]+)( век(ами?|ах?|ов|е)'
            r'| (тысячелети|столети|поколени)(ями?|ях?|и|й))\b')

    def check(self, m):
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
        return num1 + m.group(2) + num2 + m.group(4)


class OrdinalRule_1(RuleBase):
    """
    Описание: Порядковые числительные.
    Пример: "во 2 окне -> во втором окне"
    """
    def __init__(self):
        self.mask = (
            r'\b([Вв]о?|[Нн]а|[Оо]б?|[Пп]ри) '
            r'(\d*[02-9]|\d*1\d) ([а-яё]+)\b')

    def check(self, m):
        attr = words.get_attr(m.group(3))
        number = ''
        if attr.have([S_GENDER, M_GENDER], False, [5]):
            number = ordinal(m.group(2), p_mu)
        elif attr.have([Z_GENDER], False, [2, 5]):
            if len(m.group(2)) == 1 or m.group(2)[-2] != '1':
                a = m.group(2)[-1] not in ('2', '3', '4')
                b = m.group(1).lower() not in ('в', 'на')
                c = attr.have([Z_GENDER], False, [1])
                if a or b or not c:
                    number = ordinal(m.group(2), p_zh)
        if number:
            return m.group(1) + ' ' + number + ' ' + m.group(3)
        return None


class OrdinalRule_2(RuleBase):
    """
    Описание: Порядковые числительные.
    Пример: "из 3 окна -> из третьего окна"
    """
    def __init__(self):
        self.mask = (
            r'\b([Сс]о?|[Ии]з|[Дд]о|[Кк]роме|[Оо]т|[Пп]осле) '
            r'(\d*1\d|\d*[02-9]?[02-9]) ([а-яё]+)\b')

    def check(self, m):
        number = ''
        attr = words.get_attr(m.group(3))
        if attr.have([M_GENDER, S_GENDER], False, [1]):
            number = ordinal(m.group(2), r_mu)
        elif attr.have([Z_GENDER], False, [1]):
            number = ordinal(m.group(2), r_zh)
        if number:
            return m.group(1) + ' ' + number + ' ' + m.group(3)
        return None


class OrdinalRule_3(RuleBase):
    """
    Описание: Порядковые числительные.
    Пример: "со 2 примером -> со вторым примером"
    """
    def __init__(self):
        self.mask = (r'\b([Сс]о? )(\d*1\d|\d*[02-9]?[02-9]) ([а-яё]+)\b')

    def check(self, m):
        number = ''
        attr = words.get_attr(m.group(3))
        if attr.have([M_GENDER, S_GENDER], False, [4]):
            number = ordinal(m.group(2), t_mu)
        elif attr.have([Z_GENDER], False, [2, 4, 5]):
            number = ordinal(m.group(2), t_zh)
        if number:
            return m.group(1) + number + ' ' + m.group(3)
        return None


class OrdinalRule_35(RuleBase):
    """
    Описание: Порядковые числительные.
    Пример: "во 2-й или 3-й комнатах -> во второй или третьей комнатах"
    """
    def __init__(self):
        self.mask = (
            r'\b([Вв]о?|[Нн]а|[Оо]б?|[Пп]ри) '
            r'(\d+)-й( или | и )(\d+)-й( ([а-я]+([ео]й|[иы]х) |)([а-яё]+))\b')

    def check(self, m):
        attr = words.get_attr(m.group(8))
        if attr.have([Z_GENDER], None, [5]):
            new = m.group(1) + ' ' + ordinal(m.group(2), p_zh) + m.group(3)
            new += ordinal(m.group(4), p_zh) + m.group(5)
            return new
        return None


class OrdinalRule_36(RuleBase):
    """
    Описание: Порядковые числительные.
    Пример: "2-й и 3-й комнат -> второй и третьей комнат"
    """
    def __init__(self):
        self.mask = (
            r'\b(\d+)-й( или | и )(\d+)-й'
            r'( ([А-Я]?[а-я]+([ео]й|[иы]х) |)([а-яё]+))\b')

    def check(self, m):
        attr = words.get_attr(m.group(7))
        if attr.have([Z_GENDER], None, [1]):
            new = ordinal(m.group(1), r_zh) + m.group(2)
            new += ordinal(m.group(3), r_zh) + m.group(4)
            return new
        return None


class OrdinalRule_37(RuleBase):
    """
    Описание: Порядковые числительные.
    Пример: "2-й и 3-й блок(и) -> второй и третий блок(и)"
    """
    def __init__(self):
        self.mask = (
            r'\b(\d+)-й( или | и )(\d+)-й( ([а-я]+([иы]й|[иы]е) |)([а-яё]+))\b')

    def check(self, m):
        attr = words.get_attr(m.group(7))
        if attr.have([M_GENDER], None, [0]):
            new = ordinal(m.group(1), i_mu) + m.group(2)
            new += ordinal(m.group(3), i_mu) + m.group(4)
            return new
        return None


class OrdinalRule_38(RuleBase):
    """
    Описание: Порядковые числительные.
    Пример: "2-е и 3-е числа -> второе и третье числа"
    """
    def __init__(self):
        self.mask = (
            r'\b(\d+)-е( или | и )(\d+)-е( ([а-я]+([ео]е|[иы]е) |)([а-яё]+))\b')

    def check(self, m):
        attr = words.get_attr(m.group(7))
        if attr.have([S_GENDER], None, [0, 3], only_case=True):
            new = ordinal(m.group(1), i_sr) + m.group(2)
            new += ordinal(m.group(3), i_sr) + m.group(4)
            return new
        return None


class OrdinalRule_39(RuleBase):
    """
    Описание: Порядковые числительные.
    Пример: "2 груша -> вторая груша, 3 окно -> третье окно"
            "18 день -> восемнадцатый день,
            "но: 18 мегаватт, 2 дверь"
    """
    def __init__(self):
        self.mask = (
            r'(?<![,.])\b(\d*[02-9][02-9]|\d*1\d|[2-9]) ([а-яё]+)\b')

    def check(self, m):
        number = ''
        attr = words.get_attr(m.group(2))
        if (attr.have([M_GENDER], False, [0])
            and not attr.have([M_GENDER], True, [1])
            and not m.group(2) in ('грамм', 'килограмм', 'миллиграмм',
                                   'парсек', 'килопарсек', 'мегапарсек',
                                   'человек')):
            number = ordinal(m.group(1), i_mu)
        if attr.have([S_GENDER], False, [0]):
            number = ordinal(m.group(1), i_sr)
        if attr.have([Z_GENDER], False, [0]) and not attr.have(case=[3]):
            number = ordinal(m.group(1), i_zh)
        if number:
            return number + ' ' + m.group(2)
        return None


class OrdinalRule_4(RuleBase):
    """
    Описание: Порядковые числительные.
              Именительный мужского рода.
              Творительный/предложный падеж мужского/среднего рода.
              Родительный/дательный/творительный/предложный падеж женского рода.
    Пример: "на 8-м этаже -> на восьмом этаже"
    """
    def __init__(self):
        self.mask = (r'\b(\d+)-(м|й) (([А-Я]?[а-яё]+(-[а-яё]+|)+'
                     r'[б-джзк-нп-тфхцчшщ]'
                     r'([ео][йм]|[иы]м) ){,2}([А-Я]?[а-яё]+))\b')

    def check(self, m):
        number = ''
        attr = words.get_attr(m.group(7).lower())
        if m.group(2) == 'м':
            if attr.have([M_GENDER, S_GENDER], False, [4]):
                number = ordinal(m.group(1), t_mu)
            elif (attr.have([M_GENDER, S_GENDER], False, [5])
                  or m.group(7) in ('берегу', 'бою', 'году', 'лесу', 'полку',
                                    'пруду', 'саду', 'углу', 'шкафу')):
                number = ordinal(m.group(1), p_mu)
        else:
            if attr.have([M_GENDER], False, [0]):
                number = ordinal(m.group(1), i_mu)
            elif attr.have([Z_GENDER], False, [1, 2, 4, 5]):
                number = ordinal(m.group(1), t_zh)
        if number:
            return number + ' ' + m.group(3)
        return None


class OrdinalRule_6(RuleBase):
    """
    Описание: Порядковые числительные.
    Пример:
    """
    def __init__(self):
        self.mask = (r'\b(\d+)-е (([а-яё]+[ео]е ){,2}([А-Я]?[а-яё]+[ео]))\b')

    def check(self, m):
        if words.have(m.group(4).lower(), [S_GENDER], False, [0, 3]):
            return ordinal(m.group(1), i_sr) + ' ' + m.group(2)
        return None


class OrdinalRule_7(RuleBase):
    """
    Описание: Порядковые числительные.
    Пример:
    """
    def __init__(self):
        self.mask = (r'(?<![,.])\b(\d*11|\d*[05-9]) ([а-яё]+)\b')

    def check(self, m):
        attr = words.get_attr(m.group(2))
        if attr.have([M_GENDER, S_GENDER], False, [1]):
            return ordinal(m.group(1), r_mu) + ' ' + m.group(2)
        return None


class OrdinalRule_8(RuleBase):
    """
    Описание: Порядковые числительные.
    Пример:
    """
    def __init__(self):
        self.mask = (r'(?<![,.])\b(\d*11|\d*[02-9]) ([а-яё]+)\b')

    def check(self, m):
        attr = words.get_attr(m.group(2))
        if attr.have([Z_GENDER], False, [3]) and not attr.have(case=[0]):
            if m.group(1)[-1] == '3':
                new = ordinal(m.group(1), r_mu)[:-3] + 'ю '
            else:
                new = ordinal(m.group(1), r_mu)[:-3] + 'ую '
            new += m.group(2)
            return new
        return None


class OrdinalRule_9(RuleBase):
    """
    Описание: Порядковые числительные.
    Пример:
    """
    def __init__(self):
        self.mask = (
            r'(\A|\n|\(| )(\d*[02-9][05-9]|\d*1\d|[5-9]) ([а-яё]+)\b')

    def check(self, m):
        number = ''
        attr = words.get_attr(m.group(3))
        if attr.have([M_GENDER, S_GENDER], False, [1]):
            if not attr.have(case=[0]):
                number = ordinal(m.group(2), r_mu)
        if attr.have([Z_GENDER], False, [1]):
            number = ordinal(m.group(2), r_zh)
        if number:
            return m.group(1) + number + ' ' + m.group(3)
        else:
            return None


class OrdinalRule_5(RuleBase):
    """
    Описание: Порядковые числительные. Дательный падеж.
    Пример: "23 дню -> двадцать третьему дню"
    """
    def __init__(self):
        self.mask = (
            r'(\A|\n|\(| )(\d*[02-9][02-9]|\d*1\d|[2-9]) ([а-яё]+)\b')

    def check(self, m):
        number = ''
        attr = words.get_attr(m.group(3))
        if attr.have([M_GENDER, S_GENDER], False, [2]):
            number = ordinal(m.group(2), d_mu)
        if (attr.have([Z_GENDER], False, [2])
            and not attr.have([Z_GENDER], False, [1, 5], all_case=True)):
            number = ordinal(m.group(2), d_zh)
        if number:
            return m.group(1) + number + ' ' + m.group(3)
        else:
            return None


class CardinalRule_10(RuleBase):
    """
    Описание: Количественные числительные.
              Прилагательные, в состав которых входят числительные.
    Пример: (3-кратный и т.п.)
    """
    def __init__(self):
        self.mask = (r'(?<![,.])\b((\d+) - |)(\d+)-([а-яё]{5,})\b')

    def check(self, m):
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
        num = sub('ста', 'сто', num)
        num = sub(r'(одной тысячи|одноготысяче)', 'тысяче', num)
        num = sub(r'\bодного', 'одно', num)
        return num + '-' + m.group(4)


class CardinalRule_11(RuleBase):
    """
    Описание: Количественные числительные. Родительный падеж.
    Пример:
    """
    def __init__(self):
        self.mask = (
            r'\b([Оо]т|[Сс]о?)'
            r'( [а-яё]+([иы]х|[ео]й|[ео]го) '
            r'| почти | примерно | приблизительно | плюс | минус | )'
            r'((\d+,|)(\d+)( [-и] | или )|)(\d+,|)(\d+)( ([а-яё]+ |)[а-яё]+ | )'
            r'('
            r'до( [а-яё]+([иы]х|[ео]й|[ео]го) '
            r'| почти | примерно | приблизительно | плюс | минус | )'
            r'((\d+,|)\d+( [-и] | или )|)(\d+,|)\d+'
            r'( ([а-яё]+([иы]х|[ео]й|[ео]го) |и более |и менее |)([а-яё]+)|)'
            r')\b')

    def check(self, m):
        if m.group(4):
            if m.group(5):
                pre = decimal(m.group(5)[:-1], m.group(6), 1)
            else:
                pre = cardinal(m.group(6), r_ca)
                if pre[-6:] == 'одного' and m.group(22) is not None:
                    if words.have(m.group(22), [Z_GENDER], None, [1]):
                        pre = pre[:-2] + 'й'
                    elif m.group(22) == 'суток':
                        pre = pre[:-3] + 'их'
            pre += m.group(7)
        else:
            pre = ''
        if m.group(8):
            number = decimal(m.group(8)[:-1], m.group(9), 1)
        else:
            number = cardinal(m.group(9), r_ca)
        if number[-6:] == 'одного' and m.group(22) is not None:
            if words.have(m.group(22), [Z_GENDER], None, [1]):
                number = number[:-2] + 'й'
            elif m.group(22) == 'суток':
                number = number[:-3] + 'их'
        return m.group(1) + m.group(2) + pre + number + m.group(10) + m.group(12)


class CardinalRule_12(RuleBase):
    """
    Описание: Количественные числительные.
              Родительный падеж второго числительного в конструкции.
    Пример: "числительное + существительное + вместо/из/против + числительное"
    """
    def __init__(self):
        self.mask = (
            r'\b((\d+ )([а-яё]{3,})( вместо | из | против ))(\d+,|)(\d+)\b')

    def check(self, m):
        attr = words.get_attr(m.group(3))
        if m.group(5):
            number = decimal(m.group(5)[:-1], m.group(6), 1)
        else:
            number = cardinal(m.group(6), r_ca)
            day_forms = ('сутки', 'суток', 'суткам', 'сутками', 'сутках')
            if condition(m.group(6)) and attr.have([Z_GENDER]):
                number = number[:-2] + 'й'
            elif number[-6:] == 'одного' and m.group(3) in day_forms:
                number = number[:-3] + 'их'
        return m.group(1) + number


class CardinalRule_13(RuleBase):
    """
    Описание: Количественные числительные.
    Пример:
    """
    def __init__(self):
        self.mask = (
            r'\b('
            r'[Бб]олее|[Мм]енее|[Бб]ольше|[Мм]еньше|[Вв]ыше|[Нн]иже|'
            r'[Дд][ао]льше|[Дд]ороже|[Дд]ешевле|[Оо]коло|[Сс]выше|[Сс]реди|'
            r'[Дд]ля|[Дд]о|[Ии]з|[Оо]т|[Бб]ез|[Уу]|[Вв]место|[Вв] возрасте'
            r'[Бб]лиже|[Вв] количестве|[Вв] пределах|[Вв] течение|[Дд]линнее|'
            r'[Вв] размере|[Нн]ач[инаетялсьо]{2,7} с|[Пп]орядка|[Пп]осле|'
            r'[Дд]остиг[авеийлнотшщюуья]{,5}|[Вв]ладел[аеимухцыь]{2,5}|'
            r'[Пп]ротив|[Сс]тарше|[Мм]оложе|[Кк]роме|[Пп]омимо|'
            r'[Нн]а протяжении|[Нн]е превы[сш][аи][авеийолтшщюья]{1,4}'
            r')'
            r'( [а-яё]+([иы]х|[ео]й|[ео]го) '
            r'| приблизительно | примерно | почти | плюс | минус | )'
            r'((\d+,|)(\d+)( - | или )|)(\d+,|)(\d+)'
            r'( ([а-яё]+([иы]х|[ео]й|[ео]го) |и более |и менее |)'
            r'([а-яё]{3,})|)\b')

    def check(self, m):
        if m.group(4):
            if m.group(5):
                pre = decimal(m.group(5)[:-1], m.group(6), 1)
            else:
                pre = cardinal(m.group(6), r_ca)
            if condition(m.group(6)) and m.group(13) is not None:
                attr = words.get_attr(m.group(13))
                if m.group(10) and attr.have([Z_GENDER], None, [1]):
                    pre = pre[:-2] + 'й'
                elif m.group(13) == 'суток':
                    pre = pre[:-3] + 'их'
            pre += m.group(7)
        else:
            pre = ''
        if m.group(8):
            number = decimal(m.group(8)[:-1], m.group(9), 1)
        else:
            number = cardinal(m.group(9), r_ca)
            if m.group(13) and condition(m.group(9)):
                attr = words.get_attr(m.group(13))
                if attr.have(Z_GENDER, False, [1]):
                    number = number[:-2] + 'й'
                elif m.group(13) == 'суток':
                    number = number[:-3] + 'их'
            elif m.group(3) and condition(m.group(9)):
                if m.group(3)[-1:] == 'й':
                    number = number[:-2] + 'й'
                elif m.group(3)[-1:] == 'х':
                    number = number[:-3] + 'их'
        new = m.group(1) + m.group(2) + pre + number + m.group(10)
        return new


class CardinalRule_14(RuleBase):
    """
    Описание: Количественные числительные. Предлог "с" + родительный падеж.
    Пример:
    """
    def __init__(self):
        self.mask = (r'\b([Сс]о?'
            r'( всех | [а-яё]+[иы]х | примерно | приблизительно '
            r'| почти | плюс | минус | ))'
            r'((\d+)( [-и] | или )|)(\d+)'
            r'(( [а-яё]+([иы]х|[ео]й|[ео]го)|) ([а-яё]+))\b')

    def check(self, m):
        attr = words.get_attr(m.group(10))
        if attr.have(None, None, [1]):
            if m.group(3):
                prenum = cardinal(m.group(4), r_ca)
                if condition(m.group(4)) and attr.have([Z_GENDER], None, [1]):
                    prenum = prenum[:-2] + 'й'
                prenum += m.group(5)
            else:
                prenum = ''
            prenum = m.group(1) + prenum
            number = cardinal(m.group(6), r_ca)
            if attr.have([Z_GENDER], False, [1]):
                number = number[:-2] + 'й'
            return prenum + number + m.group(7)
        return None


class CardinalRule_15(RuleBase):
    """
    Описание: Количественные числительные.
    Пример:
    """
    def __init__(self):
        self.mask = (
            r'(\A|\n|\(| )((\d+) - |)(1|\d*[02-9]1)'
            r'(( [а-яё]+[ео]го | )([а-яё]+))\b')

    def check(self, m):
        attr = words.get_attr(m.group(7))
        a = attr.have([M_GENDER, S_GENDER], False, [1])
        b = attr.have([M_GENDER], False, [3])
        c = attr.have([Z_GENDER], False, [1])
        if (a and not b) or c:
            number = cardinal(m.group(4), r_ca)
            if c:
                number = number[:-2] + 'й'
            if m.group(2) == '':
                pre = ''
            else:
                pre = cardinal(m.group(3), r_ca)
                pre += ' - '
            return m.group(1) + pre + number + m.group(5)
        return None


class CardinalRule_16(RuleBase):
    """
    Описание: Количественные числительные. Родительный падеж.
              (При числительном >20 в случае мужского рода возможен винительный
              падеж, но предпочтение отдаётся родительному.)              
    Пример: "3 дней -> трёх дней"
    """
    def __init__(self):
        self.mask = (
            r'(?<![,.])\b((\d+)( [-и] | или )|)'
            r'(\d*[02-9][234]|[234])(( [а-яё]+[иы]х | )([а-яё]+))\b')

    def check(self, m):
        attr = words.get_attr(m.group(7))
        a = attr.have([M_GENDER, S_GENDER, Z_GENDER], True, [1])
        b = m.group(7) in ('лет', 'человек')
        if a or b:
            if m.group(1):
                number = cardinal(m.group(2), r_ca)
                if attr.have(gender=Z_GENDER) and number[-2:] == 'го':
                    number = number[:-2] + 'й'
                number += m.group(3)
            else:
                number = ''
            return number + cardinal(m.group(4), r_ca) + m.group(5)
        return None


class CardinalRule_17(RuleBase):
    """
    Описание: Количественные числительные. Творительный падеж. Исключение.
    Пример:
    """
    def __init__(self):
        self.mask = (
            r'\b((состав(ил[аио]?|[ия]т|ля[ею]т)|потеря(л[аио]?|[ею]т)) \d+) '
            r'(погибшими|ранеными|убитыми)'
            r'(( и \d+) (погибшими|ранеными|убитыми)|)\b')

    def check(self, m):
        if m.group(6):
            new = m.group(7) + '_ ' + m.group(8)
        else:
            new = ''
        return m.group(1) + '_ ' + m.group(5) + new


class CardinalRule_18(RuleBase):
    """
    Описание: Количественные числительные. Творительный падеж.
    Пример:
    """
    def __init__(self):
        self.mask = (
            r'\b('
            r'(\d+,|)(\d+)'
            r'( - | или | и (почти |приблизительно |примерно |плюс |минус |))|'
            r')'
            r'(\d+,|)(\d+) '
            r'(([а-яё]+-|)[а-яё]+([аиыья]ми|[ео]м|[еиоы]й|ью))\b')

    def check(self, m):
        if m.group(1):
            if m.group(2):
                pre = decimal(m.group(2)[:-1], m.group(3), 3)
            else:
                pre = cardinal(m.group(3), t_ca)
                if condition(m.group(3)):
                    a = words.have(m.group(8), [Z_GENDER], False, [4])
                    b = words.have(m.group(8)[:-2], [Z_GENDER], False, [0])
                    c = words.have(m.group(8)[:-3] + 'ь', [Z_GENDER], False, [0])
                    if a or b or c:
                        pre = pre[:-2] + 'ой'
                    elif m.group(8) == 'сутками':
                        pre = cardinal(m.group(3), t_ca) + 'и'
            pre += m.group(4)
        else:
            pre = ''
        number = ''
        if m.group(6):
            number = decimal(m.group(6)[:-1], m.group(7), 3)
        else:
            if condition(m.group(7)):
                attr = words.get_attr(m.group(8))
                if attr.have([M_GENDER, S_GENDER], False, [4]):
                    number = cardinal(m.group(7), t_ca)
                elif attr.have([Z_GENDER], False, [4]):
                    number = cardinal(m.group(7), t_ca)[:-2] + 'ой'
                elif m.group(8) == 'сутками':
                    number = cardinal(m.group(7), t_ca) + 'и'
            elif m.group(8)[-2:] == 'ми':
                number = cardinal(m.group(7), t_ca)
        if number:
            return pre + number + ' ' + m.group(8)
        return None


class CardinalRule_19(RuleBase):
    """
    Описание: Количественные числительные. Предлоги творительного падежа.
    Пример:
    """
    def __init__(self):
        self.mask = (
            r'\b(([Мм]ежду|[Нн]ад|[Пп]еред|'
            r'[Пп]о сравнению со?|[Вв] сравнении со?) '
            r'(более чем |почти |приблизительно |примерно |плюс |минус |))'
            r'((\d+,|)(\d+)'
            r'( [-и] | или )'
            r'(почти |приблизительно |примерно |плюс |минус |)|)'
            r'(\d+,|)(\d+)\b(?!-)')

    def check(self, m):
        pre = m.group(1)
        if m.group(4):
            if m.group(5):
                pre += decimal(m.group(5)[:-1], m.group(6), 3)
            else:
                pre += cardinal(m.group(6), t_ca)
            pre = pre + m.group(7) + m.group(8)
        if m.group(9):
            number = decimal(m.group(9)[:-1], m.group(10), 3)
        else:
            number = cardinal(m.group(10), t_ca)
        return pre + number


class CardinalRule_20(RuleBase):
    """
    Описание: Количественные числительные. Предложный падеж.
    Пример:
    """
    def __init__(self):
        self.mask = (
            r'\b([Вв] |[Нн]а |[Оо]б? |[Пп]ри )((\d+,|)(\d+)( [-и] | или )|)'
            r'(около |почти |примерно |приблизительно |плюс |минус |'
            r'более чем |менее чем |)'
            r'(\d+)( ([а-яё]+([иы]х|[ео][йм]) |)([а-яё]{3,}))\b')

    def check(self, m):
        if m.group(2):
            if m.group(3):
                pre = decimal(m.group(3)[:-1], m.group(4), 4)
            else:
                pre = cardinal(m.group(4), p_ca)
                a = words.have(m.group(11), None, False, [2, 5])
                b = words.have(m.group(11)[:-1] + 'м', [Z_GENDER], True, [2])
                if condition(m.group(4)) and (a or b):
                    pre = pre[:-1] + 'й'
                elif m.group(11) == 'сутках':
                    pre = pre[:-2] + 'их'
            pre += m.group(5)
        else:
            pre = ''
        number = ''
        attr = words.get_attr(m.group(11))
        if condition(m.group(7)):
            if attr.have([M_GENDER, S_GENDER], False, [5]):
                number = cardinal(m.group(7), p_ca)
            elif attr.have([Z_GENDER], False, [2, 5]):
                number = cardinal(m.group(7), p_ca)[:-1] + 'й'
            elif m.group(11) == 'сутках':
                number = cardinal(m.group(7), p_ca)[:-2] + 'их'
        elif m.group(11)[-2:] in ('ах', 'ях'):
            number = cardinal(m.group(7), p_ca)
            number = cardinal(m.group(7), p_ca)
        if number:
            return m.group(1) + pre + m.group(6) + number + m.group(8)
        else:
            return None


class CardinalRule_22(RuleBase):
    """
    Описание: Количественные числительные. Предлоги предложного падежа.
    Пример:
    """
    def __init__(self):
        self.mask = (
            r'\b(([Оо]б?|[Пп]ри)( минус| плюс| более чем| менее чем|))'
            r'( (\d+)( ([-и]|или)( минус| плюс|) )| )(\d+)\b(?!,)')

    def check(self, m):
        number = ' '
        if m.group(4) != ' ':
            number += cardinal(m.group(5), p_ca) + m.group(6)
        return m.group(1) + number + cardinal(m.group(9), p_ca)


class CardinalRule_23(RuleBase):
    """
    Описание: Количественные числительные. Винительный падеж. Десятичные дроби.
    Пример:
    """
    def __init__(self):
        self.mask = (
            r'\b(([А-Яа-яЁё]{3,}) '
            r'(всего |ориентировочно |примерно |приблизительно |более чем |'
            r'не более чем |)в )'
            r'((\d+,|)(\d+) - |)(\d+),(\d+)\b')

    def check(self, m):
        preacc = sub('ё', 'е', m.group(2).lower())
        if preacc in pre_acc:
            new = m.group(1) 
            if m.group(4):
                if m.group(5):
                    new += decimal(m.group(5)[:-1], m.group(6), 5)
                else:
                    new += m.group(6)
                new += ' - '
            new += decimal(m.group(7), m.group(8), 5)
            return new
        return None


class CardinalRule_24(RuleBase):
    """
    Описание: Количественные числительные.
              Винительный падеж мужского рода числительных,
              оканчивающихся на 1, кроме 11.
    Пример:
    """
    def __init__(self):
        self.mask = (
            r'(\A|\n|\(| )((\d+) - |)(1|\d*[02-9]1)'
            r'(( [а-яё]+[ео]го | )([а-яё]+))\b')

    def check(self, m):
        attr = words.get_attr(m.group(7))
        if (attr.have([M_GENDER], False, [3])
            and not attr.have([M_GENDER], False, [0])):
            number = cardinal(m.group(4), v_ca)[:-2] + 'ного'
            if m.group(2) == '':
                pre = ''
            else:
                pre = cardinal(m.group(3), v_ca)
                if condition(m.group(3)):
                    pre = pre[:-2] + 'ного'
                elif pre[-3:] == 'два':
                    pre = pre[:-1] + 'ух'
                elif pre[-3:] == 'три' or pre[-3:] == 'ыре':
                    pre = pre[:-1] + 'ёх'
                pre += ' - '
            return m.group(1) + pre + number + m.group(5)
        return None


class CardinalRule_25(RuleBase):
    """
    Описание: Количественные числительные. Винительный падежи.
    Пример:
    """
    def __init__(self):
        self.mask = (
            r'\b([Нн]а|[Зз]а|[Пп]ро|[Сс]пустя|[Чч]ерез|состав[аеилотя]{2,4})'
            r'( (\d+,|)(\d+)( -| или)|) (\d+,|)(\d+)'
            r'(( [а-яё]+([ая]я|[ую]ю|[ео]е|[иы][йх]) | )([а-яё]+))\b')

    def check(self, m):
        attr = words.get_attr(m.group(11))
        a = attr.have([M_GENDER], False, [3])
        b = attr.have([M_GENDER], False, [0])
        c = a and not b
        d = attr.have([Z_GENDER], False, [1, 3])
        e = attr.have([Z_GENDER], True, [1])
        f = d or e
        g = attr.have([S_GENDER], False, [0, 1])
        h = attr.have([S_GENDER], True, [1])
        j = c or attr.have([M_GENDER], True, [1])
        if m.group(2):
            if m.group(3):
                pre = decimal(m.group(3)[:-1], m.group(4), 5)
            else:
                pre = cardinal(m.group(4), v_ca)
                if pre[-3:] == 'дин':
                    if j:
                        pre = pre[:-2] + 'ного'
                    elif f:
                        pre = pre[:-2] + 'ну'
                    elif g or h:
                        pre = pre[:-2] + 'но'
                elif pre[-3:] == 'два':
                    if (c or attr.have([M_GENDER, Z_GENDER], True, [1, 3],
                        all_case=True)):
                        pre = pre[:-1] + 'ух'
                    elif f:
                        pre = pre[:-1] + 'е'
                elif ((pre[-3:] == 'три' or pre[-3:] == 'ыре') and 
                    (c or attr.have([M_GENDER, Z_GENDER], True, [1, 3],
                    all_case=True))):
                    pre = pre[:-1] + 'ёх'
            pre += m.group(5) + ' '
        else:
            pre = ''

        if m.group(6):
            number = decimal(m.group(6)[:-1], m.group(7), 5)
        else:
            number = cardinal(m.group(7), v_ca)
            if number[-3:] == 'дин':
                if c:
                    number = number[:-2] + 'ного'
                elif attr.have([Z_GENDER], False, [3]):
                    number = number[:-2] + 'ну'
                elif attr.have([S_GENDER], False, [0, 3]):
                    number = number[:-2] + 'но'
            elif number[-3:] == 'два':
                if attr.have([Z_GENDER], True, [1]):
                    number = number[:-1] + 'ух'
                elif attr.have([Z_GENDER], False, [1]):
                    number = number[:-1] + 'е'

            elif ((number[-3:] == 'три' or number[-3:] == 'ыре')
                and attr.have([M_GENDER, Z_GENDER], True, [1, 3],
                all_case=True)):
                number = number[:-1] + 'ёх'

            elif (len(m.group(7)) > 3
                and (attr.have([M_GENDER, S_GENDER, Z_GENDER], True, [1])
                or m.group(11) in ('суток', 'лет'))):
                pass
        return m.group(1) + ' ' + pre + number + m.group(8)


class CardinalRule_27(RuleBase):
    """
    Описание: Количественные числительные.
              Винительный падеж женского рода.
    Пример:
    """
    def __init__(self):
        self.mask = (
            r'(?<![,.])\b(\d*[02-9]1|1)'
            r'(( [а-яё]+[ую]ю | с половиной | с лишним | )([а-яё]+))')

    def check(self, m):
        if words.have(m.group(4), [Z_GENDER], False, [3]):
            return cardinal(m.group(1), v_ca)[:-2] + 'ну' + m.group(2)
        return None


class CardinalRule_28(RuleBase):
    """
    Описание: Количественные числительные.
              Средний род (именительный/винительный падежи).
    Пример:
    """
    def __init__(self):
        self.mask = (
            r'(?<![,.])\b(\d*[02-9]1|1) '
            r'(([а-яё]+[ео]е |)([а-яё]+[ео]))\b')

    def check(self, m):
        if words.have(m.group(4), [S_GENDER], False, [0, 3]):
            if len(m.group(1)) > 1:
                if int(m.group(1)[:-1]) != 0:
                    number = m.group(1)[:-1] + '0_ одно'
                else:
                    number = m.group(1)[:-1] + '_ одно'
            else:
                number = m.group(1)[:-1] + 'одно'
            return number + ' ' + m.group(2)
        return None


class CardinalRule_29(RuleBase):
    """
    Описание: Количественные числительные.
              Женский род (именительный/винительный падежи).
    Пример:
    """
    def __init__(self):
        self.mask = (
            r'(\A|\n|\(| )(((\d+)( - | или | и ))|)(\d+,|)(\d+)'
            r'((( [а-яё]+([ая]я|[иы][ех]))+'
            r'| с половиной| с лишним|) ([а-яё]+))')

    def check(self, m):
        attr = words.get_attr(m.group(12))
        a = attr.have([Z_GENDER], False, [1])
        b = attr.have([Z_GENDER], False, [0]) and condition(m.group(7))
        if (a or b):
            new = m.group(1)
            if m.group(2):
                new += feminin(m.group(4)) + m.group(5)
            if m.group(6):
                new += m.group(6) + m.group(7) + m.group(8)
            else:
                new += feminin(m.group(7)) + m.group(8)
            return new
        return None


class CardinalRule_30(RuleBase):
    """
    Описание: Количественные числительные. Дательный падеж.
    Пример:
    """
    def __init__(self):
        self.mask = (
            r'(?<![,.])\b((\d+)( [-и] | или )|)(\d+)'
            r'(( [а-яё]+([иы]м|[ео]му) | )([а-яё]+([аиыя]м|у|ю|е)))\b')

    def check(self, m):
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
            if words.have(m.group(8), [M_GENDER, S_GENDER], False, [2]):
                number = cardinal(m.group(4), d_ca)
            elif words.have(m.group(8), [Z_GENDER], False, [2, 5]):
                number = cardinal(m.group(4), d_ca)[:-2] + 'й'
            elif m.group(8) == 'суткам':
                number = cardinal(m.group(4), d_ca)[:-3] + 'им'
        elif m.group(9) == 'ам' or m.group(9) == 'ям':
            number = cardinal(m.group(4), d_ca)
        if number:
            return pre + number +m.group(5)
        return None


class CardinalRule_31(RuleBase):
    """
    Описание: Количественные числительные. Дательный падеж.
    Пример: "к 25 -> к двадцати пяти"
    """
    def __init__(self):
        self.mask = (
            r'\b([Кк] |рав[нагеийлмоcуюыхья]{2,6} |эквивалент[аеноы]{2} )'
            r'((\d+,|)(\d+)( [-и] | или )|)(\d+,|)(\d+)\b')

    def check(self, m):
        number = ''
        if m.group(2):
            if m.group(3):
                number += decimal(m.group(3)[:-1], m.group(4), 2)
            else:
                number += cardinal(m.group(4), d_ca)
            number += m.group(5)
        if m.group(6):
            number += decimal(m.group(6)[:-1], m.group(7), 2)
        else:
            number += cardinal(m.group(7), d_ca)
        return m.group(1) + number


class CardinalRule_32(RuleBase):
    """
    Описание: Количественные числительные.
              Существует только во множественном числе.
    Пример:
    """
    def __init__(self):
        self.mask = (r'\b((\d+) - |)((\d+) (сутки|суток))')

    def check(self, m):
        pre = ''
        if m.group(1):
            pre = daynight(m.group(2), m.group(5)) + '-'
        return pre + daynight(m.group(4), m.group(5)) + ' ' + m.group(5)


class CardinalRule_33(RuleBase):
    """
    Описание: Количественные числительные.
              Предлог "по" при указании количества.
    Пример:
    """
    def __init__(self):
        self.mask = (r'\b([Пп]о )(\d*1(000){1,3})\b')

    def check(self, m):
        return m.group(1) + cardinal(m.group(2), d_ca)


class CardinalRule_35(RuleBase):
    """
    Описание: Количественные числительные.
              Предлог "по" при указании количества с десятичной дробью.
    Пример:
    """
    def __init__(self):
        self.mask = (r'\b([Пп]о )(\d+),(\d+)\b')

    def check(self, m):
        if condition(m.group(2)) or condition(m.group(3)):
            new = m.group(1) + decimal(m.group(2), m.group(3), 2)
            new = sub('ым', 'ых', new)
            return new
        else:
            return None


class CardinalRule_38(RuleBase):
    """
    Описание: Количественные числительные. Винительный падеж.
    Пример: "в 1,1 раза -> в одну целую одну десятую раза"
    """
    def __init__(self):
        self.mask = (r'\b([Вв] )((\d+,|)(\d+)( [-и] | или )|)(\d+,|)(\d+)'
                     r'( (тысячи|миллиона|миллиарда|триллиона) раз| раза?)\b')

    def check(self, m):
        new = m.group(1)
        if m.group(2):
            if m.group(3):
                new += decimal(m.group(3)[:-1], m.group(4), 5)
            else:
                new += m.group(4)
            new += m.group(5)
        if m.group(6):
            new += decimal(m.group(6)[:-1], m.group(7), 5)
        else:
            new += m.group(7)
        return new + m.group(8)


class Rule_1(RuleBase):
    """
    Описание: Десятичные дроби в именительном падеже.
    Пример:
    """
    def __init__(self):
        self.mask = (r'\b(\d+),(\d+)(\b|\Z)')

    def check(self, m):
        return decimal(m.group(1), m.group(2)) + m.group(3)


class Rule_2(RuleBase):
    """
    Описание: Буква Ё.
    Пример: "все небо" -> "всё небо"
    """
    def __init__(self):
        self.mask = (r'\b([Вв]с)е ([а-яё]+)\b')

    def check(self, m):
        if words.have(m.group(2), [S_GENDER], False, [0, 3]):
            return m.group(1) + 'ё ' + m.group(2)
        return None


class CardinalRule_34(RuleBase):
    """
    Описание: Количественные числительные. Винительный падеж.
    Пример:
    """
    def __init__(self):
        self.mask = (
            r'\b(([А-Яа-яЁё]{3,}) '
            r'(всего |ориентировочно |примерно |приблизительно |более чем |'
            r'не более чем |)в )'
            r'((\d+)( - | или )|)(\d+) ([а-яё]+)\b')

    def check(self, m):
        preacc = sub('ё', 'е', m.group(2).lower())
        if preacc in pre_acc:
            pre = m.group(1)
            if m.group(4):
                if words.have(m.group(8), [Z_GENDER], True, [1]):
                    pre += feminin(m.group(5), 5)
                else:
                    pre += cardinal(m.group(5), v_ca)
                pre += m.group(6)
            return pre + cardinal(m.group(7), v_ca) + " " + m.group(8)
        else:
            return None


class CardinalRule_26(RuleBase):
    """
    Описание: Количественные числительные. Предложный падеж.
    Пример: "в 21 принадлежащей -> в двадцати одной принадлежащей"
    """
    def __init__(self):
        self.mask = (r'\b([Вв] |[Нн]а |[Пп]ри |[Оо]б? )'
            r'(\d*[02-9]1|1)( [а-яё]+[ео](й|м)(|ся))\b')

    def check(self, m):
        new = m.group(1) + cardinal(m.group(2), p_ca)
        if m.group(4) == 'й':
            new = new[:-1] + 'й'
        return new + m.group(3)


class CardinalRule_21(RuleBase):
    """
    Описание: Количественные числительные. Предложный падеж.
    Пример: "в 2 из 3 случаев -> в двух из ..."
    """
    def __init__(self):
        self.mask = (r'\b([Вв] )(\d+)( из \d+ ([а-яё]+))\b')

    def check(self, m):
        number = cardinal(m.group(2), p_ca)
        a = condition(m.group(2))
        b = words.have(m.group(4), [Z_GENDER], None, [1])
        if a and b:
            number = number[:-1] + 'й'
        new = m.group(1) + number + m.group(3)
        return new


class OrdinalRule_40(RuleBase):
    """
    Описание: Порядковые числительные. Дательный падеж.
    Пример: "к 3 числу -> к третьему числу"
    """
    def __init__(self):
        self.mask = (r'\b([Кк]о? )(\d*[02-9][2-9]|\d*1\d|[2-9])'
            r'( [а-я]+[ео](му|й) | )([а-яё]+)\b')

    def check(self, m):
        attr = words.get_attr(m.group(5))
        if attr.have(None, False, [2]):
            new = ordinal(m.group(2), d_mu)
            if attr.have([Z_GENDER], False, [2]):
                new = new[:-2] + 'й'
            return m.group(1) + new + m.group(3) + m.group(5)
        return None


class CardinalRule_36(RuleBase):
    """
    Описание: Количественные числительные. Дательный падеж.
    Пример: "к 21 возвышающемуся -> к двадцати одному возвышающемуся"
    """
    def __init__(self):
        self.mask = (r'\b([Кк] |[Пп]о )'
            r'(\d*[02-9]1|1)( [а-яё]+[ео](й|му)(|ся))\b')

    def check(self, m):
        new = m.group(1) + cardinal(m.group(2), d_ca)
        if m.group(4) == 'й':
            new = cardinal(m.group(2), p_ca)[:-1] + 'й'
        return new + m.group(3)


class CardinalRule_37(RuleBase):
    """
    Описание: Десятичные дроби. Предложный падеж.
    Пример: "в 10,7 километра(х) -> в десяти целых семи десятых километра(х)"
    """
    def __init__(self):
        self.mask = (r'\b(([Вв]|[Пп]ри|[Оо]б?) (более чем |менее чем |))'
                     r'((\d+,|)(\d+)( [-и] | или )|)(\d+),(\d+)'
                     r'( ([а-я]+[оы](го|й|х) |)([а-я]+))\b')

    def check(self, m):
        attr = words.get_attr(m.group(13))
        new = m.group(1)
        if m.group(4):
            if m.group(5):
                pre = decimal(m.group(5)[:-1], m.group(6), 4)
            else:
                pre = cardinal(m.group(6), p_ca)
                if condition(m.group(6)) and attr.have([Z_GENDER], None, [1, 5]):
                    pre = pre[:-1] + 'й'
            new += pre + m.group(7)
        if (attr.have(None, False, [1]) or attr.have(None, True, [5])):
            new += decimal(m.group(8), m.group(9), 4) + m.group(10)
            return new
        else:
            return None


# ==========================
# Подготовка списков правил.
# ==========================

rules_list = (UnitRule_0(),
              UnitRule_2(),
              UnitRule_3(),         # родительный (следует перед UnitRule_4)
              UnitRule_4(),         # родительный
              UnitRule_5(),         # родительный (следует после UnitRule_4)
              UnitRule_8(),         # творительный
              UnitRule_1(),         # винительный
              UnitRule_6(),         # именительный/винительный
              UnitRule_7(),
              UnitRule_9(),         # предложный
              UnitRule_11(),        # именительный
              UnitRule_12(),
              TimeRule_1(),
              TimeRule_2(),
              TimeRule_3(),
              TimeRule_4(),
              QuasiRoman(),
              RomanRule_1(),
              RomanRule_2(),
              OrdinalRule_1(),
              OrdinalRule_2(),
              OrdinalRule_3(),
              OrdinalRule_35(),
              OrdinalRule_36(),
              OrdinalRule_37(),
              OrdinalRule_38(),
              OrdinalRule_6(),
              OrdinalRule_7(),
              OrdinalRule_8(),
              OrdinalRule_9(),
              OrdinalRule_5(),       # дательный
              OrdinalRule_40(),      # дательный
              )

rules_list_2 = (OrdinalRule_4(),
                OrdinalRule_39(),
                CardinalRule_20(),     # предложный /перед винительным/
                CardinalRule_21(),     # предложный /перед родительным/
                CardinalRule_23(),     # винительный
                CardinalRule_34(),     # винительный
                CardinalRule_25(),     # винительный
                CardinalRule_38(),     # винительный
                CardinalRule_11(),     # родительный
                CardinalRule_12(),
                CardinalRule_13(),
                CardinalRule_14(),
                CardinalRule_15(),
                CardinalRule_16(),
                CardinalRule_17(),     # творительный
                CardinalRule_18(),     # творительный
                CardinalRule_19(),
                CardinalRule_26(),
                CardinalRule_22(),
                CardinalRule_24(),
                CardinalRule_37(),
                CardinalRule_27(),     # именительный/винительный
                CardinalRule_28(),
                CardinalRule_29(),
                CardinalRule_30(),     # дательный
                CardinalRule_36(),
                CardinalRule_31(),
                CardinalRule_32(),
                CardinalRule_33(),
                CardinalRule_35(),
                CardinalRule_10(),
                Rule_1(),
                Rule_2(),
               )
