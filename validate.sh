cd result

#if [ -f *.txt ]; then
    rm -rf *.txt
#fi

cd ..
python3 validator.py -f meta_resultPool.csv -d jsoup -n 10