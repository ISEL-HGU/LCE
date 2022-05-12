@echo off
cd .\result
if exist ".\*.csv" then del *.csv
cd ..
if exist ".\pool\" then echo "pool already exists" else mkdir pool
cd .\pool
if exist ".\jsoup\"then echo "jsoup already exists" else git clone https://github.com/jhy/jsoup
cd ..
python ./main.py -g jsoup_gumtree_vector.csv -c jsoup_commit_file.csv -t testVector.csv
