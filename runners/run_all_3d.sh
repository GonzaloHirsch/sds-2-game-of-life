#!/bin/bash

Len=$1
len=$2
dim='3'
tm=$3
rule=$4

echo "Processing rule $rule"
for per in 10 20 30 40 50 60 70 80 90 100
do
  for iter in 1 2 3 4 5
  do
    python3 generator/random_input_generator.py -L "$Len" -l "$len" -d "$dim" -p "$per"
    java -jar ./target/sds-tp2-1.0-SNAPSHOT-jar-with-dependencies.jar -sf ./parsable_files/static.txt -df ./parsable_files/dynamic.txt -t "$tm" -r "$rule"
  done
  echo "Processing $per%"
done