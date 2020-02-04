#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import version_info
from os import makedirs
from shutil import copyfile, rmtree


site_pkg = "python%d.%d/site-packages" % (version_info.major,
                                          version_info.minor)
try:
    # удаление какталога с предыдущей сборкой
    rmtree('build')
except:
    pass

dest_dir = "build/lib/%s/rhvoice_tools" % site_pkg

# создание каталогов в build
makedirs(dest_dir + '/preprocessing/dict')
makedirs(dest_dir + '/scripts')

files = ['__init__.py',
         'rhvoice_say.py',
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
    copyfile(file, "%s/%s" % (dest_dir, file))
