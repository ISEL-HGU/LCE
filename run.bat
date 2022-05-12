rem cd LAS
rem mvn clean package

rem java -cp ./LAS/target/LAS-0.0.1-SNAPSHOT.jar main.LAS C:/repository/fv4202/pool/Closure_rank-1_old.java C:/repository/fv4202/pool/Closure_rank-1_new.java
rem cd ..
cd ./result
del *.csv
cd ..
python ./main.py -g Grasscutter_vector.csv -c Grasscutter_file_commit.csv -t testVector.csv