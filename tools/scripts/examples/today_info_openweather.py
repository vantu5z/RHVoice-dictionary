#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyowm
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
        owm = pyowm.OWM(API_key=key, language='ru')
        observation = owm.weather_at_place(city)
        w = observation.get_weather()
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
                % (w.get_temperature('celsius').get('temp'),
                   get_wind_direction(w.get_wind().get('deg')),
                   w.get_wind().get('speed'),
                   w.get_pressure().get('press')*0.75006375541921,
                   w.get_humidity(),
                   w.get_detailed_status()
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
