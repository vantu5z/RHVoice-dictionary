#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import version_info
from os import makedirs
from shutil import copyfile, rmtree


site_pkg = "python%d.%d/site-packages" % (version_info.major, version_info.minor)

try:
    rmtree('build')
except:
    pass

dest_dir = "build/lib/%s/rhvoice_preprocessing" % site_pkg

makedirs(dest_dir + '/preprocessing/dict')

files = ['__init__.py',
         'rhvoice_say.py',
         'preprocessing/functions.py',
         'preprocessing/rules.py',
         'preprocessing/templates.py',
         'preprocessing/text_prepare.py',
         'preprocessing/words_forms.py',
         'preprocessing/dict/words_muz.py',
         'preprocessing/dict/words_sre.py',
         'preprocessing/dict/words_zen.py'
        ]
for file in files:
    copyfile(file, "%s/%s" % (dest_dir, file))
