#!/usr/bin/python2

# Copyright 2012 Nikolay Orlyuk
# Distributed under the terms of the GNU General Public License v2

from subprocess import check_output
import xml.etree.ElementTree as ET
import sys

ws_dirs = sys.argv[1:]

mi_props_xml = check_output(["svn", "propget", "-R", "--xml", "svn:mergeinfo"] + ws_dirs)
mi_props = ET.fromstring(mi_props_xml)

for target in mi_props.findall("target"):
    print (target.attrib["path"])
    for prop in target.findall("property"):
        if prop.attrib["name"] != "svn:mergeinfo": continue
        print(prop.text)
    print ("----")

