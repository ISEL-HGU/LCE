#!/bin/bash

cd result
#if [ -f "*.csv" ]; then
   rm -rf *.csv
#fi

#if [ -f "*.txt" ]; then
   rm -rf *.txt
#fi

cd ..

if [ -d "pool" ]; then
   echo "pool already exists"
else
   mkdir pool
fi

cd pool
if [ -d "jsoup" ]; then
   echo "jsoup already exists"
else
   git clone https://github.com/jhy/jsoup
fi

cd ..
python3 main.py -g jsoup_gumtree_vector.csv -c jsoup_commit_file.csv -t testVector.csv > result/log.txt