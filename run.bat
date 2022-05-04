@ECHO OFF
cd LAS
rem mvn clean package

java -cp ./LAS/target/LAS-0.0.1-SNAPSHOT.jar main.LAS
rem  C:/repository/fv4202/pool/Closure_rank-1_old.java C:/repository/fv4202/pool/Closure_rank-1_new.java
cd ..
rem python ./main.py -g target/gumtreeVector.csv