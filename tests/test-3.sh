# Copyright 2012 Nikolay Orlyuk
# Distributed under the terms of the GNU General Public License v2

ws trunk
run mkdir -p p/{m1,m2}
run svn add *
run touch p/file.txt
run svn add p/file.txt
run touch p/m{1,2}/file.txt
run svn add p/m{1,2}/file.txt
commit "test hierarchy"

branch supmerge

ws branches/supmerge
run svn rm p/file.txt
run svn rm p/m1/file.txt
commit "rm on branch"

ws trunk
run svn merge -N {\^/branches/supmerge/,}p
commit "partial supmerge"
