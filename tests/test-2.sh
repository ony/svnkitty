# Copyright 2012 Nikolay Orlyuk
# Distributed under the terms of the GNU General Public License v2

ws trunk
run mkdir -p p/{m1,m2}
run svn add *
commit "test hierarchy"

branch submerge

ws branches/submerge
run touch p/file.txt
run svn add p/file.txt
commit "change on branch for top folder"

ws trunk
run svn merge {\^/branches/submerge/,}p
commit "full merge"

ws branches/submerge
run touch p/m{1,2}/file.txt
run svn add p/m{1,2}/file.txt
commit "new files on branch"

ws trunk
run svn merge {\^/branches/submerge/,}p/m1
commit "partial submerge"

ws branches/submerge
run svn merge --record-only -c7 {"$SVNROOT"/trunk/,}p
commit "mark revision of partial submerge to trunk as already merged to branch"

branch supmerge

ws branches/supmerge
run svn rm p/file.txt
commit "rm on branch"

ws trunk
run svn merge -N {\^/branches/supmerge/,}p
commit "partial supmerge"

ws branches/submerge
run svn merge {\^/trunk/,}p
commit "rebase submerge on top of trunk"

ws trunk
assert_mergeinfo testdata-1-before.txt
svn-mi-cleanup.py
assert_mergeinfo testdata-1-after.txt
