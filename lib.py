# encoding=UTF-8

# Copyright © 2011-2016 Jakub Wilk <jwilk@jwilk.net>
# SPDX-License-Identifier: MIT

'''
AST manipulation
'''

import functools
import ast
import sys
import tokenize

if sys.version_info >= (3, 2):
    python_open = tokenize.open
elif sys.version_info < (3,):
    def python_open(path):
        return open(path, 'rU')

if str is not bytes:
    unicode = str

def _extract_strings(obj):
    if isinstance(obj, (str, bytes, unicode)):
        if obj:
            yield obj
        return
    if isinstance(obj, list):
        for item in obj:
            for s in _extract_strings(item):
                yield s
        return
    if isinstance(obj, ast.AST):
        for name, node in ast.iter_fields(obj):
            for s in _extract_strings(node):
                yield s
        return

def extract_strings(path):
    with python_open(path) as file:
        source = file.read()
    try:
        tree = ast.parse(source, filename=path)
    except TypeError as exc:
        raise SyntaxError(exc)
    for s in _extract_strings(tree):
        yield s
    source_iter = iter(source.splitlines(True))
    readline = functools.partial(next, source_iter)
    for tp, token, srow_scol, erow_ecol, line in tokenize.generate_tokens(readline):
        if tp == tokenize.COMMENT:
            yield token

__all__ = [
    'extract_strings',
]

# vim:ts=4 sts=4 sw=4 et
