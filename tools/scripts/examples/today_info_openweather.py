#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyowm.owm import OWM
from pyowm.utils.config import get_default_config
from rhvoice_tools.scripts import get_time, get_date, get_weekday, get_greeting
from rhvoice_tools import rhvoice_say
from datetime import datetime


def get_data(key, city):
    """
    Получение данных на сегодняшний день.
    key - ключ от openweathermap.org
    city - город с уточнением страны
    """
    get_err = False
    try:
        config_dict = get_default_config()
        config_dict['language'] = 'ru'
        owm = OWM(api_key=key, config=config_dict)
        mgr = owm.weather_manager()
        w = mgr.weather_at_place(city).weather
    except:
        get_err = "Сведения о погоде получить не удалось."

    data = ("%s. "
            "Сегодня %s, %s. "
            "Время %s. "
            % (get_greeting(),
               get_weekday(),
               get_date(),
               get_time())
           )

    if not get_err:
        data += ("Температура за окном %d ℃. "
                "Ветер %s, %d м в секунду. "
                "Атмосферное давление %d мм рт. ст. "
                "Относительная влажность воздуха %d %%. "
                "%s."
                % (w.temperature('celsius').get('temp'),
                   get_wind_direction(w.wind().get('deg')),
                   w.wind().get('speed'),
                   w.pressure.get('press')*0.75006375541921,
                   w.humidity,
                   w.detailed_status
                  )
               )
    else:
        data += get_err

    return data

def get_wind_direction(deg):
    """
    Направление ветра заданное в градусах.
    """
    direction = ['северный', 'северо-восточный', 'восточный', 'юго-восточный',
                 'южный', 'юго-западный','западный','северо-западный']
    x = deg // 45
    y = deg % 45
    if y>45/2:
        x += 1
    return direction[x]


key = 'ключ от openweathermap.org'
city = 'Moscow,RU'
rhvoice_say(get_data(key, city))
