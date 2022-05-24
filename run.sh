# remove remaining result files from previous run
# $0 = shell_script, $1 = hash-id, $2 = project-id
echo "executing "$0" on batch_"$1"_"$2"..."

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
python3 main.py -g jsoup_gumtree_vector.csv -c jsoup_commit_file.csv -t targetVector.csv > result/log.txt
#python3 main.py -g jsoup_gumtree_vector.csv -c jsoup_commit_file.csv -t testVector.csv > result/log.txt
# remove remaining diff texts
cd result
rm -rf diff*.txt
cd ..
# remove remaining candidate source codes
cd candidates
rm -rf *.java
cd ..
python3 validator.py -f meta_resultPool.csv -d jsoup -n 10 -r /home/codemodel/leshen/APR/target/$1/outputs/prepare_pool_source >> result/log.txt