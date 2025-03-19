#!/bin/bash

DATADIR="/home/jesse/Desktop/mini_tissuenet/"
OUTFILE="out.csv"
ls -s -a $DATADIR

#=== Request echoing of each command executed
set -x
date
start=$(date +%s)

java -jar target/RadiomicsJ-jar-with-dependencies.jar -i $DATADIR/int -m $DATADIR/seg -o $OUTFILE -features GLCM,GLDZM

end=$(date +%s)
echo "Experiment: $EXPERIMENT_NAME Elapsed Time: $(($end-$start)) seconds"
echo "Experiment: $EXPERIMENT_NAME Elapsed Time: $(($end-$start)) seconds" > timing_$EXPERIMENT_NAME.txt
date
