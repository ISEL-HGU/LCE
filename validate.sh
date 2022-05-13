cd .\result
if [ -f ".\*.txt"] then del *.txt
cd ..
python validator.py -f meta_resultPool.csv -d jsoup -n 1