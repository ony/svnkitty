#!/usr/bin/python2

# Copyright 2012 Nikolay Orlyuk
# Distributed under the terms of the GNU General Public License v2

from subprocess import check_output
import xml.etree.ElementTree as ET
import sys
import os.path

class BaseCase(object): __slots__ = ('revision', 'path', 'info')

class SupMerge(BaseCase): pass
class SubMerge(BaseCase): pass

#sys.exit()



class Workspace(object):
    __slots__ = ('_info',)

    def __init__(self):
        self._info = {}

    @classmethod
    def _walkup(cls, node):
        subnodes = []
        if os.path.ismount(node): raise StopIteration
        while True:
            (node, subnode) = os.path.split(node)
            subnodes.insert(0, subnode)
            if os.path.ismount(node): raise StopIteration
            yield node, subnodes

    def inherited(self, path):
        for node, subnodes in self._walkup(path):
            info = self._info.get(node)
            if info is None: continue
            if len(subnodes) == 0: return info
            # do not in non-inheritable ranges
            info = filter(lambda x: x[2], info)
            # adjust paths
            info = map(lambda x: (x[0], "/".join([x[1]] + subnodes), x[2]), info)
            return (subnodes, frozenset(info))
        return None

    def __setitem__(self, path, info):
        self._info[path] = info

    def __getitem__(self, path):
        info = self._info.get(path)
        if info is not None: return info
        return self.inherited(path)[1] # only mergeinfo

    @property
    def mergepoints(self): return self._info.keys()

def unmerged_revisions(ws):
    for mp in ws.mergepoints:
        inherited = ws.inherited(mp)
        if inherited is None: continue
        info = ws[mp]
        # non-inheritable revs from info is also important
        dinfo = info.symmetric_difference(inherited[1])
        for item in dinfo:
            print (item, inherited[0])
            yield (item, inherited[0])

def parse_mergeinfo(text):
    print(text)
    for entry in text.split('\n'):
        [source, ranges] = entry.split(':',1)
        for revs in ranges.split(','):
            if revs.endswith('*'):
                # non-inheritable mergeinfo
                revs = revs[:-1]
                inherit = False
            else: inherit = True

            if '-' in revs:
                [start, stop] = revs.split('-', 1)
                values = range(int(start), int(stop)+1)
            else:
                values = [int(revs)]

            for rev in values:
                print((rev,source,inherit))
                yield rev, source, inherit

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

def get_repo_root(ws_dirs = []):
    args = ["svn", "info", "--xml"] + ws_dirs
    #print(args)
    info_str = check_output(args)
    #print(info_str)
    info_xml = ET.fromstring(info_str)

    #print(info_xml["entry/repository/root"])
    # only one repo root for all ws_dirs expected
    [info] = list(frozenset(map(lambda x: x.text, info_xml.findall("entry/repository/root"))))
    return info


def get_log(revs = None, ws_dirs = []):
    root = get_repo_root(ws_dirs)
    if revs is None: revs_arg = []
    elif len(revs) == 0: raise StopIteration
    else: revs_arg = ["-c" + ",".join(map(str,revs))]
    args = ["svn", "log", "--xml", "-v"] + revs_arg + [root]
    print(args)
    log_out = check_output(args)
    print(log_out)


ws = Workspace()
ws_dirs = sys.argv[1:]
for target, mi in get_mergeinfo(ws_dirs):
    ws[target] = mi
    print (target, mi)

revs = frozenset(map(lambda x: x[0][0], unmerged_revisions(ws)))
print(revs)

get_log(revs, ws_dirs)
#for entry in get_log(revs, ws_dirs):
#    print(entry)
