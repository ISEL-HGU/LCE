#!/bin/bash

cd result
rm -rf *.csv
rm -rf *.txt
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

cd result
rm -rf diff*.txt
cd ..

cd candidates
rm -rf *.java
cd ..

python3 validator.py -f meta_resultPool.csv -d jsoup -n 100 >> result/log.txt