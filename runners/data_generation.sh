#!/bin/bash

Len=$1
len=$2
dim=$3
tm=$4

for per in 10 20 30 40 50 60 70 80 90 100
do
  echo "Processing %$per percentage..."
  echo "$dim Living $per" > parsable_files/living_percent_vs_time.txt
  echo "$dim Radius $per" > parsable_files/radius_vs_time.txt
  python3 generator/random_input_generator.py -L "$Len" -l "$len" -d "$dim" -p "$per"
  cp parsable_files/dynamic.txt parsable_files/dynamic_copy.txt
  for rule in 1 2 3
  do
    cp parsable_files/dynamic_copy.txt parsable_files/dynamic.txt
    java -jar ./target/sds-tp2-1.0-SNAPSHOT-jar-with-dependencies.jar -sf ./parsable_files/static.txt -df ./parsable_files/dynamic.txt -t "$tm" -r "$rule"
    filename="$dim""d_$rule""r_$per""p.avi"
    if [ $dim -eq '3' ]; then
      echo "3D BABE"
    else
      python3 visualization/visualize2D.py --mov-file $filename --interval $tm
    fi
  done
  python3 visualization/evolution_graph_visualize.py parsable_files/radius_vs_time.txt
  python3 visualization/evolution_graph_visualize.py parsable_files/living_percent_vs_time.txt
done