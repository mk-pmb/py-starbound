#!/usr/bin/python
# -*- coding: UTF-8, tab-width: 4 -*-

from __future__ import division

from sys import argv, stdin, stdout, stderr
from codecs import open as cfopen
import os.path

import starbound

import yaml
# ^-- Performance geeks: For using C Loader and Dumper, refer to
#     http://pyyaml.org/wiki/PyYAMLDocumentation



def main(invocation, *cli_args):
    src_fn = dest_fn = '-'
    data = fmt = None

    file_infos = (
        'type=identifier',
        'version',
        'name',
        'meta=get_metadata',
        'content=data',
        )

    cli_argi = iter(cli_args)
    for arg in cli_argi:
        if arg in ('-f', '--src'):
            src_fn = cli_argi.next()
            continue

        if arg in ('-t', '--format'):
            fmt = cli_argi.next()
            if fmt in ('guess', 'auto'):
                fmt = None
            continue

        if arg in ('-o', '--dest'):
            dest_fn = cli_argi.next()
            continue

        if arg in ('-L', '--load'):
            if guessfextfmt(fmt, src_fn) == 'yaml':
                with stdio_or_cfopen(src_fn, 'r', 'utf8') as fh:
                    data = yaml.safe_load(fh)
                continue
            with starbound.open_file(src_fn, fmt) as fh:
                data = obj2dict(fh, file_infos)
            continue

        if arg in ('-d', '--dive'):
            data = dive_into_dict(data, cli_split(cli_argi.next()))
            continue

        if arg in ('-k', '--keys'):
            data = data.keys()
            continue

        if arg in ('-F', '--filter'):
            data = filter_dict(data, cli_split(cli_argi.next()))
            continue

        if arg in ('-o', '--omit'):
            data = filter_dict(data, cli_split(cli_argi.next()), invert=True)
            continue

        if arg in ('-Y', '--dump'):
            print yaml.safe_dump(data).rstrip()
            continue

        if arg in ('-w', '--save'):
            if guessfextfmt(fmt, dest_fn) == 'yaml':
                with stdio_or_cfopen(dest_fn, 'w', 'utf8') as fh:
                    fh.write(yaml.safe_dump(data))
                continue
            raise AssertionError("Writing Starbound files isn't supported yet.",
                dest_fn)
            continue

        raise ValueError('unsupported option ' + arg)


def stdio_or_cfopen(fn, mode, encoding):
    if fn == '-':
        if mode.startswith('r'):
            return stdin
        return stdout
    return cfopen(fn, mode, encoding)


def guessfextfmt(force_fmt, fn):
    if force_fmt is not None:
        return force_fmt
    return os.path.splitext(fn)[1].lstrip('.')


def dive_into_dict(basedict, path):
    entry = basedict
    cwd = []
    for step in path:
        try:
            if isinstance(entry, (tuple, list,)):
                step = int(step)
            entry = entry[step]
        except Exception as err:
            raise KeyError('cannot dive deeper into dict', step, cwd, err)
        cwd.append(step)
    return entry


def cli_split(arg):
    arg = unicode(arg)
    if arg == '':
        return []
    if arg[0].isalnum():
        return [arg]
    return arg[1:].split(arg[0])


def obj2dict(obj, keys, dest = None):
    if dest is None:
        dest = {}
    for key in keys:
        alias = key.split('=', 1)
        if len(alias) > 1:
            alias, key = alias
        else:
            alias = key
        val = None
        try:
            val = obj.__getattribute__(key)
        except AttributeError as err:
            pass
        try:
            if val is None:
                val = obj.__getattr__(key)
        except AttributeError as err:
            pass
        try:
            val = val()
        except Exception as err:
            pass
        dest[alias] = val
    return dest


def filter_dict(src, keys, invert=False, dest=None):
    if dest is None:
        dest = {}
    if invert:
        # copy all entries except those in keys
        for key in src.viewkeys():
            if key not in keys:
                dest[key] = src[key]
    else:
        # copy the entries namedin keys
        for key in keys:
            alias = key.split('=', 1)
            if len(alias) > 1:
                alias, key = alias
            else:
                alias = key
            if src.has_key(key):
                dest[key] = src[key]
    return dest











if __name__ == '__main__':
    main(*argv)
