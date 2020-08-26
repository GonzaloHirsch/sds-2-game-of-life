#!/bin/bash

Len=$1
len=$2
dim=2
percent=$3
tm=$4
rule=$5

mvn clean package

python3 generator/random_input_generator.py -L "$Len" -l "$len" -d 2 -p "$percent"
java -jar ./target/sds-tp2-1.0-SNAPSHOT-jar-with-dependencies.jar -sf ./parsable_files/static.txt -df ./parsable_files/dynamic.txt -t "$tm" -r "$rule"
python visualization/visualize2D.py --interval 100