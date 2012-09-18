# Copyright 2012 Nikolay Orlyuk
# Distributed under the terms of the GNU General Public License v2

ws trunk
run mkdir -p p/m{1,2}
run touch p/m{1,2}/file.txt
run svn add *
commit "initial"

branch feature

ws branches/feature
echo "see subdirs" > p/file.txt
commit "top folder commit"

ws trunk
run svn merge {\^/branches/feature/,}
commit "full merge"

branch hotfix

ws branches/feature
echo "hi" > p/m1/file.txt
commit "hi on branch"

ws trunk
run svn merge {\^/branches/feature/,}p/m1
commit "partial merge"


ws branches/hotfix
echo "fix" > p/m2/file.txt
commit "hotifx on other branch"

ws trunk
run svn merge --reintegrate {\^/branches/hotfix/,}
svn diff
commit "full merge of hotfix"

assert_mergeinfo testdata-4-before.txt
