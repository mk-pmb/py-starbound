#!/usr/bin/python
# -*- coding: UTF-8, tab-width: 4 -*-

from __future__ import division

from sys import argv, stdin, stdout, stderr
from codecs import open as cfopen
import os.path
import starbound
import yaml



def main(invocation, *cli_args):
    src_fn = dest_fn = '-'
    data = fmt = None

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

        if arg in ('-O', '--dest'):
            dest_fn = cli_argi.next()
            continue

        if arg in ('-L', '--load'):
            if guessfextfmt(fmt, src_fn) == 'yaml':
                with stdio_or_cfopen(src_fn, 'r', 'utf8') as fh:
                    data = yaml.safe_load(fh)
                continue
            with starbound.open_file(src_fn, fmt) as file:
                data = file.data
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






















if __name__ == '__main__':
    main(*argv)
