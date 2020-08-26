#!/bin/bash

Len='50'
len='15'
dim='3'
tm='100'

for rule in 1 2 3
  do
  echo "Processing rule $rule"
  for per in 10 20 30 40 50 60 70 80 90 100
  do
    for iter in 1 2 3 4 5 6 7 8 9 10
    do
      python3 generator/random_input_generator.py -L "$Len" -l "$len" -d "$dim" -p "$per"
      java -jar ./target/sds-tp2-1.0-SNAPSHOT-jar-with-dependencies.jar -sf ./parsable_files/static.txt -df ./parsable_files/dynamic.txt -t "$tm" -r "$rule"
    done
    echo "Processing $per%"
  done
done