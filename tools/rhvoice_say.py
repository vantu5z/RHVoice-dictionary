#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import subprocess
import configparser
from os.path import exists as path_exists
from os.path import expanduser
from rhvoice_tools import text_prepare


def rhvoice_say(text):
    if text:
        """
        Чтение текста RHVocie с предварительнгой обработкой текста.
        """
        txt = text_prepare(text)        # предварительная подготовка текста

        # открываем файл конфигурации
        file_name = expanduser("~") + '/.config/rhvoice_say.conf'
        config = configparser.ConfigParser(allow_no_value=True)
        # с учетом регистра
        config.optionxform = str
        if not path_exists(file_name):
            # если файл отсутствует, создаем новый со стандартными настройками
            config['Settings'] = {"; Использовать Speech Dispatcher для чтения ('True' или 'False')": None,
                                  'use_speech_dispatcher': False,
                                  '; Громкость в процентах (от -100 до 100)': None,
                                  'volume': 0,
                                  '; Скорость в процентах (от -100 до 100)': None,
                                  'rate': 0,
                                  '; Высота в процентах (от -100 до 100)': None,
                                  'pitch': 0,
                                  '; Голос для чтения': None,
                                  'voice': 'Aleksandr+Alan'}
            with open(file_name, 'w') as configfile:
                config.write(configfile)
        config.read(file_name)
        settings = config['Settings']
        use_SD = settings.getboolean('use_speech_dispatcher')
        voice = settings.get('voice')
        volume = settings.getint('volume')
        rate = settings.getint('rate')
        pitch = settings.getint('pitch')

        if use_SD:
            # -e, --pipe-mode (Pipe from stdin to stdout plus Speech Dispatcher)
            # -w, --wait (Wait till the message is spoken or discarded)
            # -y, --synthesis-voice (Set the synthesis voice)
            # -r, --rate (Set the rate of the speech)
            #            (between -100 and +100, default: 0)
            # -i, --volume (Set the volume (intensity) of the speech)
            #              (between -100 and +100, default: 0)
            # -p, --pitch (Set the pitch of the speech)
            #             (between -100 and +100, default: 0)
            p = subprocess.Popen(['spd-say',
                                  "-e", "-w",
                                  "-y" + voice,
                                  "-i %d" % volume,
                                  "-r %d" % rate,
                                  "-p %d" % pitch
                                  ],
                                 stdin=subprocess.PIPE)
        else:
            # -p <spec>, --profile <spec> (voice profile)
            # -r <percent>,  --rate <percent> (speech rate)
            # -v <percent>,  --volume <percent> (speech volume)
            # -t <percent>,  --pitch <percent> (speech pitch)
            p = subprocess.Popen(['RHVoice-test',
                                  "-p " + voice,
                                  "-v %d" % (volume + 100),
                                  "-r %d" % (rate + 100),
                                  "-t %d" % (pitch + 100)
                                  ],
                                 stdin=subprocess.PIPE)
        p.communicate(txt.encode('utf-8'))
    else:
        print('Нет текста для чтения...')
