#!/usr/bin/python
# -*- coding: UTF-8, tab-width: 4 -*-


from __future__ import division

import sys
import os.path
import posixpath



def normsubpath(path, target_os_path = None):
    if target_os_path is None:
        target_os_path = os.path
    rel_up = target_os_path.join(target_os_path.pardir, '')
    path = target_os_path.normpath(path)
    path = target_os_path.relpath(path)
    if path.startswith(rel_up):
        raise ValueError('path points upwards', path)
    return  path











if __name__ == '__main__':
    if len(sys.argv) < 2:
        print '\n'.join([func.__name__ for func in globals().values()
                         if type(func).__name__ == 'function'])
    else:
        globals()[sys.argv[1]](*sys.argv[2:])
