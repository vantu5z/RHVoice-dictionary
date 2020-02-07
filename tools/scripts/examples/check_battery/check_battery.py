#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Проверка состояния заряда батареи

from rhvoice_tools import rhvoice_say
from rhvoice_tools.scripts import is_battery_low

s = is_battery_low()
if s:
    rhvoice_say(s)
