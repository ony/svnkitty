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
run svn merge {"$SVNROOT"/branches/submerge/,}p
commit "full merge"

ws branches/submerge
run touch p/m{1,2}/file.txt
run svn add p/m{1,2}/file.txt
commit "new files on branch"

ws trunk
run svn merge {"$SVNROOT"/branches/submerge/,}p/m1
commit "partial submerge"

branch supmerge

ws branches/supmerge
run svn rm p/file.txt
commit "rm on branch"

ws trunk
svnup
run svn merge -N {"$SVNROOT"/branches/supmerge/,}p
commit "partial supmerge"

ws trunk
run svn propget -R svn:mergeinfo

