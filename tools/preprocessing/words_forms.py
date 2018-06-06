#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from re import sub

# импорт pymorphy2 для определения атрибутов слов
try:
    import pymorphy2
    morph = pymorphy2.MorphAnalyzer()
    is_morph = True
except:
    print('Не установлен "pymorphy2".'
          'Определение атрибутов слова будет вестись по словарю.')
    is_morph = False

# импорт словарей
import words_muz
import words_zen
import words_sre

# константы с названием рода слова
M_GENDER = 'мужской'
Z_GENDER = 'женский'
S_GENDER = 'средний'
O_GENDER = 'общий'


class Words():
    """
    Основной класс для работы со словами в разных формах.
    """
    def __init__(self):
        """
        Инициализация.
        """
        # инициализация словарей
        self.muz = WordsForms(words_muz.words, M_GENDER)
        self.zen = WordsForms(words_zen.words, Z_GENDER)
        self.sre = WordsForms(words_sre.words, S_GENDER)

        # поддержка pymorphy2
        if is_morph:
            self.morph = morph
        else:
            self.morph = None

    def parse_morph(self, records):
        """
        Приведение результатов разобранного слова с помощью pymorphy2
        к нужному виду.
        Возвращает: экземпляр AttrList
        """
        attr_list = AttrList()

        # перебираем все варианты разбора
        for rec in records:
            tag = rec.tag.cyr_repr

            # отбрасываем не существительные
            if 'СУЩ' not in tag:
                continue

            # род
            if   'ор' in tag: gender = O_GENDER
            elif 'мр' in tag: gender = M_GENDER
            elif 'жр' in tag: gender = Z_GENDER
            elif 'ср' in tag: gender = S_GENDER
            else:
                continue

            # число
            plural = 'мн' in tag

            # совпадение падежей
            case = [0, 0, 0, 0, 0, 0]
            if 'им' in tag: case[0] = 1
            if 'рд' in tag: case[1] = 1
            if 'дт' in tag: case[2] = 1
            if 'вн' in tag: case[3] = 1
            if 'тв' in tag: case[4] = 1
            if 'пр' in tag: case[5] = 1

            if 1 in case:
                attr_list.append(WordAttributes(gender, plural, case))

        return attr_list

    def get_attr(self, word):
        """
        Определение атрибутов слова.
        Возвращает: экземпляр AttrList
        """
        # если подключен pymorphy2
        if self.morph:
            result = self.morph.parse(word)
            attr_list = self.parse_morph(result)
            return attr_list

        # поиск слова по словарю
        attr_list = AttrList()
        for item in [self.muz, self.zen, self.sre]:
            attr = item.get_attr(word)
            if not attr.fuzzy:
                attr_list.append(attr)

        return attr_list

    def have(self, word, gender=None, plural=None, case=None, all_case=False):
        """
        Проверка на наличие атрибутов.
        """
        attr_list = self.get_attr(word)
        return attr_list.have(gender, plural, case, all_case)


class WordsForms():
    """
    Описание слов в разных формах одного рода.
    """
    def __init__(self, words, gender):
        """
        Инициализация.
        """
        # род слов
        self.gender = gender
        # падежи для единственного числа
        self.ed_case = [[], [], [], [], [], []]
        # падежи для множественного числа
        self.mn_case = [[], [], [], [], [], []]

        # загрузка слов по спискам
        for em in words:
            # единственные числа
            for i, word in enumerate(em[0]):
                self.ed_case[i].append(word)
            # множественные числа
            for i, word in enumerate(em[1]):
                self.mn_case[i].append(word)

    def get_attr(self, word):
        """
        Определение атрибутов слова.
        """
        for plural in [False, True]:
            case = self.get_case(word, plural)
            if 1 in case:
                return WordAttributes(self.gender, plural, case)

        # если нет указанного слова в словаре
        return WordAttributes(None)

    def get_case(self, word, plural):
        """
        Определение падежей слова указанного числа.
        """
        case = [0, 0, 0, 0, 0, 0]

        if plural:
            case_list = self.mn_case
        else:
            case_list = self.ed_case

        word = sub('ё', 'е', word)
        for i, w_case in enumerate(case_list):
            if word in [sub('ё', 'е', rem_yo) for rem_yo in w_case]:
                case[i] = 1

        return case


class AttrList(list):
    """
    Список атрибутов слова.
    """
    def __init__(self):
        """
        Инициализация.
        """
        # инициализация себя как списка
        list.__init__(self)

    def have(self, gender=None, plural=None, case=None, all_case=False):
        """
        Проверка на наличие атрибутов.
        """
        for attr in self:
            if attr.have(gender, plural, case, all_case):
                return True
        return False


class WordAttributes():
    """
    Атрибуты слова.
    """
    def __init__(self, gender=None, plural=None, case=[0, 0, 0, 0, 0, 0]):
        """
        Инициализация.
        """
        self.gender = gender
        self.plural = plural
        self.case = case

        # если что-то не указано, ставим пометку об этом
        if gender is None or plural is None or case is None:
            self.fuzzy = True
        else:
            self.fuzzy = False

        if self.case is None:
            self.case = [0, 0, 0, 0, 0, 0]

    def have(self, gender=None, plural=None, case=None, all_case=False):
        """
        Проверка на наличие атрибутов.
        """
        if self.fuzzy:
            return False

        if gender is not None and not (self.gender in gender):
            return False

        if plural is not None and self.plural != plural:
            return False

        if case:
            # проверка на наличие падежей
            present = False
            have_all = True
            for c in case:
                if self.case[c]:
                    present = True
                else:
                    have_all = False
            if all_case and have_all:
                return True
            elif not all_case and present:
                return True
            else:
                return False

        return True
