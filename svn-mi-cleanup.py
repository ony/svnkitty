#!/usr/bin/python2

# Copyright 2012 Nikolay Orlyuk
# Distributed under the terms of the GNU General Public License v2

from subprocess import check_output
import xml.etree.ElementTree as ET
import sys

def parse_mergeinfo(text):
    for entry in text.split('\n'):
        [source, ranges] = entry.split(':',1)
        for revs in ranges.split(','):
            if revs.endswith('*'):
                # non-inheritable mergeinfo 
                revs = revs[:-1]
            if '-' in revs:
                [start, stop] = revs.split('-', 1)
                values = range(int(start), int(stop)+1)
            else:
                values = [int(revs)]

            for rev in values:
                print((source,rev))
                yield source, rev

def get_mergeinfo(ws_dirs = []):
    mi_props_xml = check_output(["svn", "propget", "-R", "--xml", "svn:mergeinfo"] + ws_dirs)
    mi_props = ET.fromstring(mi_props_xml)

    for target in mi_props.findall("target"):
        target_path = target.attrib["path"]
        #print (target_path)
        for prop in target.findall("property"):
            if prop.attrib["name"] != "svn:mergeinfo": continue
            mergeinfo = frozenset(parse_mergeinfo(prop.text))
            #print (mergeinfo)
            yield target_path, mergeinfo
        #print ("----")

ws_dirs = sys.argv[1:]
for target, mi in get_mergeinfo(ws_dirs):
    print (target, mi)

