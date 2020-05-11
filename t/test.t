#!/usr/bin/env bash

# Copyright © 2020 Jakub Wilk <jwilk@jwilk.net>
# SPDX-License-Identifier: MIT

set -e -u
echo 1..1
base="${0%/*}/.."
cmd="$base/pystrings"
set -- "$cmd" "$cmd"
if [ -n "${PYTHON-}" ]
then
    set -- "$PYTHON" "$@"
fi
out=$(exec "$@")
sed -e 's/^/# /' <<< "$out"
if grep -q -x SyntaxError <<<"$out"
then
    echo ok 1
else
    echo not ok 1
fi

# vim:ts=4 sts=4 sw=4 et ft=sh
