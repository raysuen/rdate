#!/bin/bash 

git add *
git commit -m "`~/raysuen/bin/rdate.py -f "%Y%m%d"`"
git push -u origin "master"
