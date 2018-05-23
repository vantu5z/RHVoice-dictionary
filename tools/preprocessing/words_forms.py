#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# импорт словарей
import words_muz
import words_zen
import words_sre

# константы с названием рода слова
M_GENDER = 'мужской'
Z_GENDER = 'женский'
S_GENDER = 'средний'


class Words():
    """
    Основной класс для работы со словами в разных формах.
    """
    def __init__(self):
        """
        Инициализация.
        """
        self.muz = WordsForms(words_muz.words, M_GENDER)
        self.zen = WordsForms(words_zen.words, Z_GENDER)
        self.sre = WordsForms(words_sre.words, S_GENDER)

    def get_attr(self, word):
        """
        Определение аттрибутов слова.
        Возвращает: <род>, <число>, (<список совпавших падежей>)
        """
        res, gender, plural, case = self.muz.get_attr(word)
        if not res:
            res, gender, plural, case = self.zen.get_attr(word)
        if not res:
            res, gender, plural, case = self.sre.get_attr(word)

        if res:
            return gender, plural, case
        else:
            return None, None, None

    def get_gender(self, word):
        """
        Определение рода.
        """
        gender, plural, case = self.get_attr(word)
        return gender

    def get_case_list(self, word):
        """
        Определение списка падежей.
        """
        gender, plural, case = self.get_attr(word)
        return case

    def is_plural(self, word):
        """
        Определение числа.
        """
        gender, plural, case = self.get_attr(word)
        return plural


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
            return True, self.gender, plural, case

        # проверка слов множественного числа
        plural = True
        case = self.get_case(word, plural)  
        if 1 in case:
            return True, self.gender, plural, case
        else:
            # если нет указанного слова в словаре
            return False, None, None, None

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
