#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Скрипт предварительной обработки текста для
# синтезатора речи RHVoice Ольги Яковлевой
# By capricorn2001 & vantu5z

from re import sub, finditer

from .templates import (samples_1, samples_2, samples_3,
                        stress_marker_samples,
                        units, zh_units,
                        forms,
                        pre_acc,
                        r_ca, d_ca, v_ca, t_ca, p_ca,
                        adj_pad, mn_pad, mu_pad, sr_pad, zh_pad,
                        greekletters)
from .functions import (condition, cardinal, ordinal, roman2arabic, replace,
                        substant, feminin, daynight, decimal)
from .rules import (rules_list, ArithmExpr)


def text_prepare(text, stress_marker=False, debug=False, debug_list=None):
    """
    Основная функция обработки текста.
    """

    # Обработка простых арифметических выражений
    text = ArithmExpr().run(text)

    # применение шаблонов
    for sample in samples_1:
        text = sub(sample[0], sample[1], text)

    # применение правил
    for rule in rules_list:
        text = rule.run(text, debug, debug_list)

    # применение шаблонов
    for sample in samples_2:
        length = len(text)
        for m in finditer(sample[0], text):
            new = eval(sample[1])
            text = replace(text, new, length, m.start(), m.end())

    # буквы греческого алфавита
    for letter_name, letters in greekletters.items():
        for letter in letters:
            text = sub(letter, letter_name, text)

    # окончательная обработка
    for sample in samples_3:
        text = sub(sample[0], sample[1], text)

    # шаблоны с указанием символа ударения
    if stress_marker:
        for sample in stress_marker_samples(stress_marker):
            text = sub(sample[0], sample[1], text)

    return text
