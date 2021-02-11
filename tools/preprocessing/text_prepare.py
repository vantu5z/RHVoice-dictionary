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
                        i_mu, i_sr, i_zh, i_mn,
                        r_ca, r_mn, r_mu, r_sr, r_zh,
                        d_ca, d_mn, d_mu, d_sr, d_zh,
                        v_ca, v_zh,
                        t_ca, t_mn, t_mu, t_sr, t_zh,
                        p_ca, p_mn, p_mu, p_sr, p_zh,
                        adj_pad, mn_pad, mu_pad, sr_pad, zh_pad,
                        greekletters)
from .functions import (condition, cardinal, ordinal, roman2arabic, replace,
                        substant, feminin, daynight, decimal)
from .rules import rules_list, rules_list_2


def text_prepare(text, stress_marker=False, debug=False):
    """
    Основная функция обработки текста.
    """

    # применение шаблонов
    for sample in samples_1:
        text = sub(sample[0], sample[1], text)

    # применение правил
    for rule in rules_list:
        text = rule.run(text, debug)

    # применение шаблонов
    for sample in samples_2:
        length = len(text)
        for m in finditer(sample[0], text):
            new = eval(sample[1])
            text = replace(text, new, length, m.start(), m.end())

    # применение правил
    for rule in rules_list_2:
        text = rule.run(text, debug)

    # буквы греческого алфавита
    for letter_name, letters in greekletters.items():
        for letter in letters:
            text = sub(letter, letter_name, text)

    # окончателная обработка
    for sample in samples_3:
        text = sub(sample[0], sample[1], text)

    # шаблоны с указанием символа ударения
    if stress_marker:
        for sample in stress_marker_samples(stress_marker):
            text = sub(sample[0], sample[1], text)

    return text
