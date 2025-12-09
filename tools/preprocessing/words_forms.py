#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from re import sub
from importlib.util import find_spec

is_morph = False
# импорт pymorphy2(3) для определения атрибутов слов
if find_spec("pymorphy3") is not None:
    import pymorphy3
    morph = pymorphy3.MorphAnalyzer()
    is_morph = True
elif find_spec("pymorphy2") is not None:
    import pymorphy2
    morph = pymorphy2.MorphAnalyzer()
    is_morph = True
else:
    print('Не установлен "pymorphy2" или "pymorphy3".\n'
          'Определение атрибутов слова будет вестись по встроенному словарю.')

# импорт словарей
from .dict import words_muz
from .dict import words_zen
from .dict import words_sre

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

        # поддержка pymorphy
        if is_morph:
            self.morph = morph
        else:
            self.morph = None

    def parse_morph(self, records):
        """
        Приведение результатов разобранного слова с помощью pymorphy
        к нужному виду.
        Возвращает: экземпляр AttrList
        """
        attr_list = AttrList()

        # если наиболее вероятная форма не существительное, то выходим
        tag = records[0].tag.cyr_repr
        if 'СУЩ' not in tag or '0' in tag:
            return attr_list
        norm_form = []
        # перебираем все варианты разбора
        # и составляем список слов в нормальной форме
        for rec in records:
            # отбрасываем не существительные
            tag = rec.tag.cyr_repr
            if 'СУЩ' not in tag:
                continue

            if rec.normal_form not in norm_form:
                norm_form.append(rec.normal_form)

        # составляем список вариантов разбора
        for item in norm_form:
            case_ed = [0, 0, 0, 0, 0, 0]
            case_mn = [0, 0, 0, 0, 0, 0]
            gender = None
            plural = None

            for rec in records:
                if rec.normal_form == item:
                    tag = rec.tag.cyr_repr

                    # род
                    if gender is None:
                        if   'ор' in tag: gender = O_GENDER
                        elif 'мр' in tag: gender = M_GENDER
                        elif 'жр' in tag: gender = Z_GENDER
                        elif 'ср' in tag: gender = S_GENDER
                        else:
                            continue

                    # число
                    plural = 'мн' in tag

                    if plural:
                        case = case_mn
                    else:
                        case = case_ed

                    # совпадение падежей
                    if 'им' in tag: case[0] = 1
                    if 'рд' in tag: case[1] = 1
                    if 'дт' in tag: case[2] = 1
                    if 'вн' in tag: case[3] = 1
                    if 'тв' in tag: case[4] = 1
                    if 'пр' in tag: case[5] = 1

            if 1 in case_ed and gender is not None:
                attr_list.append(WordAttributes(gender, False, case_ed))
            if 1 in case_mn and gender is not None:
                attr_list.append(WordAttributes(gender, True, case_mn))

        return attr_list

    def get_attr(self, word):
        """
        Определение атрибутов слова.
        Возвращает: экземпляр AttrList
        """
        # если подключен pymorphy
        if self.morph:
            result = self.morph.parse(word)
            attr_list = self.parse_morph(result)
            return attr_list

        # поиск слова по словарю
        attr_list = AttrList()
        for item in [self.muz, self.zen, self.sre]:
            attrs = item.get_attr(word)
            for attr in attrs:
                if not attr.fuzzy:
                    attr_list.append(attr)

        return attr_list

    def have(self, word, gender=None, plural=None, case=None,
             all_case=False, only_case=False):
        """
        Проверка на наличие атрибутов.
        """
        attr_list = self.get_attr(word)
        return attr_list.have(gender, plural, case, all_case, only_case)


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
        attrs = []
        for plural in [False, True]:
            case = self.get_case(word, plural)
            if 1 in case:
                attrs.append(WordAttributes(self.gender, plural, case))
        if attrs:
            return attrs
        # если нет указанного слова в словаре
        return [WordAttributes(None)]

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

    def have(self, gender=None, plural=None, case=None,
             all_case=False, only_case=False):
        """
        Проверка на наличие атрибутов.
        """
        for attr in self:
            if attr.have(gender, plural, case, all_case, only_case):
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

    def have(self, gender=None, plural=None, case=None,
             all_case=False, only_case=False):
        """
        Проверка на наличие атрибутов.
        Флаги:
          all_case  - содержит все указанные падежи
          only_case - содержит только указанные падежи
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

            if only_case:
                temp_case = self.case.copy()
                for c in case:
                    temp_case[c] = 0
                for c in temp_case:
                    if c == 1:
                        return False
                if all_case:
                    return have_all
                return True

            if all_case and have_all:
                return True
            if not all_case and present:
                return True
            return False

        return True
