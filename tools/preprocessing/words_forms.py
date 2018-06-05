#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# импорт pymorphy2 для определения атрибутов слов
try:
    import pymorphy2
    morph = pymorphy2.MorphAnalyzer()
    is_morph = True
except:
    print('Не установлен "pymorphy2".'
          'Определение аттрибутов слова будет вестись по словарю.')
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
        Возвращает: экземпляр attr
        """
        # первый разбор слова
        first_tag = records[0].tag.cyr_repr

        # число
        plural = 'мн' in first_tag

        # род
        if   'ор' in first_tag: gender = O_GENDER
        elif 'мр' in first_tag: gender = M_GENDER
        elif 'жр' in first_tag: gender = Z_GENDER
        elif 'ср' in first_tag: gender = S_GENDER
        else:
            return None

        # совпадение падежей
        case = [0, 0, 0, 0, 0, 0]
        for item in records:
            tag = item.tag.cyr_repr
            if ('СУЩ' in tag):
                if 'им' in tag: case[0] = 1
                if 'рд' in tag: case[1] = 1
                if 'дт' in tag: case[2] = 1
                if 'вн' in tag: case[3] = 1
                if 'тв' in tag: case[4] = 1
                if 'пр' in tag: case[5] = 1

        if 1 in case:
            return WordAttributes(gender, plural, case)
        else:
            return WordAttributes(None)

    def get_attr(self, word):
        """
        Определение аттрибутов слова.
        Возвращает: экземпляр attr
        """
        # если подключен pymorphy2
        if self.morph:
            result = self.morph.parse(word)
            attr = self.parse_morph(result)
            return attr

        # поиск слова по словарю
        attr = self.muz.get_attr(word)
        if attr.fuzzy:
            attr = self.zen.get_attr(word)
        if attr.fuzzy:
            attr = self.sre.get_attr(word)

        return attr

    def get_gender(self, word):
        """
        Определение рода.
        """
        attr = self.get_attr(word)
        return attr.gender

    def get_case_list(self, word):
        """
        Определение списка падежей.
        """
        attr = self.get_attr(word)
        return attr.case

    def is_plural(self, word):
        """
        Определение числа.
        """
        attr = self.get_attr(word)
        return attr.plural

    def have(self, word, gender=None, plural=None, case=None, all_case=False):
        attr = self.get_attr(word)
        return attr.have(gender, plural, case, all_case)


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
        Определение аттрибутов слова.
        """
        # проверка слов единственного числа
        plural = False
        case = self.get_case(word, plural)
        if 1 in case:
            return WordAttributes(self.gender, plural, case)

        # проверка слов множественного числа
        plural = True
        case = self.get_case(word, plural)
        if 1 in case:
            return WordAttributes(self.gender, plural, case)
        else:
            # если нет указанного слова в словаре
            return WordAttributes(None)

    def get_case(self, word, plural):
        """
        Определение падежей слова указанного числа.
        """
        case = [0, 0, 0, 0, 0, 0]

        if plural:
            for i, w_case in enumerate(self.mn_case):
                if word in w_case:
                    case[i] = 1
        else:
            for i, w_case in enumerate(self.ed_case):
                if word in w_case:
                    case[i] = 1
        return case

    def is_in_specified(self, case_n, plural, word):
        """
        Проверка наличия слова с указанными параметрами.
        """
        if plural:
            if word in self.mn_case[case_n]:
                return True
        else:
            if word in self.ed_case[case_n]:
                return True
        return False


class WordAttributes():
    """
    Аттрибуты слова.
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
        Проверка на наличие аттрибутов.
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
