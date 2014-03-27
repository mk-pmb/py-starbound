#!/usr/bin/python
# -*- coding: UTF-8, tab-width: 4 -*-


from __future__ import division

import sys
import os.path
import posixpath



def normsubpath(path, target_opsys_normpath = None):
    # convert to posix syntax to allow os-independent checks:
    path = posixpath.normpath(path)

    # security checks
    if path.lstrip('.').startswith('/'):
        raise ValueError('path points upwards', path)

    # convert back to platform-dependent path syntax:
    if target_opsys_normpath is None:
        target_opsys_normpath = os.path.normpath
    path = target_opsys_normpath(path)
    return path











if __name__ == '__main__':
    if len(sys.argv) < 2:
        print '\n'.join([func.__name__ for func in globals().values()
                         if type(func).__name__ == 'function'])
    else:
        globals()[sys.argv[1]](*sys.argv[2:])
