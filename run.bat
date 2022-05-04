@ECHO OFF
rem cd LAS
rem mvn clean package

rem java -cp ./LAS/target/LAS-0.0.1-SNAPSHOT.jar main.LAS C:/repository/fv4202/pool/Closure_rank-1_old.java C:/repository/fv4202/pool/Closure_rank-1_new.java
rem cd ..
cd ./result
del *.csv
cd ..
python ./main.py -g gumtreeVector.csv -t testVector.csv -r 60