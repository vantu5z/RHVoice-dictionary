#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .preprocessing.text_prepare import text_prepare as do_prepare


def text_prepare(text):
    return do_prepare(text)
