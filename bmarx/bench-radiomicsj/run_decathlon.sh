#!/bin/bash

JARPATH="/home/kharchenkoa2/work/radiomicsj/target/RadiomicsJ-2.1.1-SNAPSHOT-jar-with-dependencies.jar"
DATADIR="/home/kharchenkoa2/work/data/decathlon-splitroi-tif"
OUTDIR="/home/kharchenkoa2/work/data/OUT-radj"
SETTINGSFILE="/home/kharchenkoa2/work/bench-radiomicsj/settings_2D_example.properties"

# check paths
if [[ ! -e $JARPATH ]] ; then
  echo "ERROR! $JARPATH"
  exit 1
fi

if [[ ! -e $DATADIR ]] ; then 
  echo "ERROR! $DATADIR"
  exit 1
fi

if [[ ! -e $OUTDIR ]] ; then
  echo "ERROR! $OUTDIR"
  exit 1
fi

if [[ ! -e $SETTINGSFILE ]] ; then 
  echo "ERROR! $SETTINGSFILE"
  exit 1
fi

# request echoing of each command executed
set -x

# timing
date
start=$(date +%s)

# run RadiomicsJ
java -Djava.awt.headless=true -jar $JARPATH -i $DATADIR/int -m $DATADIR/seg -o $OUTDIR -s $SETTINGSFILE

# timing
end=$(date +%s)
echo "Experiment: $DATADIR Elapsed Time: $(($end-$start)) seconds"
printf "JARPATH: $JARPATH \nDATADIR: $DATADIR \nOUTDIR: $OUTDIR \nSETTINGSFILE: $SETTINGSFILE \nElapsed Time: $(($end-$start)) seconds \n" > run_accuracy_timing.output
date


