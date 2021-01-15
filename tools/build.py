#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import makedirs
from shutil import rmtree, copy
from site import getsitepackages


try:
    # удаление какталога с предыдущей сборкой
    rmtree('build')
except:
    pass

dest_dir = "build/%s/rhvoice_tools" % getsitepackages()[0]

# создание каталогов в build
dirs = ['preprocessing/dict',
        'scripts',
        'rhvoice-say',
        'rhvoice-config'
       ]
for item in dirs:
    makedirs(dest_dir + "/" + item)

files = ['__init__.py',
         'rhvoice-say/rhvoice_say.py',
         'rhvoice-config/rhvoice_conf_gui.py',
         'preprocessing/functions.py',
         'preprocessing/rules.py',
         'preprocessing/templates.py',
         'preprocessing/text_prepare.py',
         'preprocessing/words_forms.py',
         'preprocessing/dict/words_muz.py',
         'preprocessing/dict/words_sre.py',
         'preprocessing/dict/words_zen.py',
         'scripts/__init__.py',
         'scripts/battary_status.py',
         'scripts/forismatic_quotes.py',
         'scripts/greeting.py',
         'scripts/time_utils.py'
        ]
for file in files:
    copy(file, "%s/%s" % (dest_dir, file))

# копирование файлов в bin
files = ['rhvoice-say/rhvoice_say',
         'rhvoice-config/rhvoice_config',
        ]
makedirs("build/usr/bin/")
for file in files:
    copy(file, "build/usr/bin/")
