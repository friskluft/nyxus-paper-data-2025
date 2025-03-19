#!/bin/bash

# EXEPATH="/home/kharchenkoa2/work/nyxusbuild1/nyxus"
EXEPATH="/home/kharchenkoa2/work/nyxus-softtuning/BLD1/nyxus"
DATADIR="/home/kharchenkoa2/work/data/decathlon/output"
OUTDIR="/home/kharchenkoa2/work/data/OUT-decathlon"
OUTFNAME="f_decathlon.csv"
N_THREADS=8
TIMEFNAME="nyxus_timing_decathlon.output"

# check paths
if [[ ! -e $EXEPATH ]] ; then
  echo "ERROR! $EXEPATH"
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

# request echoing of each command executed
set -x

# timing
date
start=$(date +%s)

# run Nyxus
ARGS="--useGpu=true --intDir=$DATADIR/int --segDir=$DATADIR/seg --coarseGrayDepth=100 --features=*ALL* --filePattern=.* --outDir=$OUTDIR --resultFname=$OUTFNAME --verbose=1 --outputType=singlecsv --reduceThreads=$N_THREADS"
$EXEPATH $ARGS

# timing
end=$(date +%s)
echo "Elapsed Time: $(($end-$start)) seconds"
echo "***" >> $TIMEFNAME
date >> $TIMEFNAME
echo $DATADIR >> $TIMEFNAME
printf "Command line: $EXEPATH $ARGS \n" >> $TIMEFNAME
printf "Elapsed Time: $(($end-$start)) seconds \n" >> $TIMEFNAME
date




