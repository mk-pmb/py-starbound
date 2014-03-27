#!/usr/bin/python
# -*- coding: UTF-8, tab-width: 4 -*-

import sys
import os.path
sys.path.insert(1, os.path.abspath(os.path.join(__file__, '../../..')))

import osutil
import ntpath
import posixpath
import macpath


somepaths = [
    '/root/.ssh',
    '../../../../etc/shadow',
    'subdir/../../updir/../foo',
    's\t\range\n\ames',
    's\\t\\range\\n\\ames',
    'totally/legit',
    'totally/legit/dir/',
    'down/and/up/again/../../../../',
    '.gitignore',
    './.gitignore',
    ]

os_path_libs = (
    ('posix', posixpath,),
    ('win', ntpath,),
    ('mac', macpath,),
    )

for p in somepaths:
    print 'orig:\t', p
    print 'repr:\t', repr(p)
    try:
        for os, lib in os_path_libs:
            print os + ':\t', osutil.normsubpath(p, lib.normpath)
    except Exception as err:
        print err
    print
