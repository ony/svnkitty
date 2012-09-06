#!/usr/bin/python2

# Copyright 2012 Nikolay Orlyuk
# Distributed under the terms of the GNU General Public License v2

from subprocess import check_output
import sys

ws_dir = sys.argv[1]

mi_props = check_output(["svn", "propget", "-R", "--xml", "svn:mergeinfo", ws_dir])

print(mi_props)

