# remove remaining result files from previous run
# $0 = shell_script
# $1 = hash-id_project-id : hash-id and D4J project ID of execution

echo "executing "$0" on batch_"$1"..."
cd /home/codemodel/leshen/APR/target/$1/outputs
mkdir fv4202 # make result directory
cd /home/codemodel/leshen/APR/LCE

# $2 = gumtree_vector : change vector pool
# $3 = commit_file : commit IDs and file paths of each change vector
# $4 = targetVector : change vector between target vector and a commit just before that target vector
# $5 = result_dir: where resulting vectors will appear # /home/codemodel/leshen/APR/target/$1_$2/outputs/fv4202

python3 main.py -g $2 -c $3 -t $4 -r $5/log.txt

# remove remaining diff texts
cd result
rm -rf diff*.txt
cd ..
# remove remaining candidate source codes
cd candidates
rm -rf *.java
cd ..
python3 validator.py -f meta_resultPool.csv -d jsoup -n 10 -r $5 >> $5/log.txt