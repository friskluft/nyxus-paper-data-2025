#!/bin/bash 

EXPERIMENT_NAME="Mock_Cellprofiler_on_Tissuenet"
DATADIR="/home/ec2-user/work/data/tissuenet"
OUTDIR="/home/ec2-user/work/data/OUTPUT-tissuenet"
ls -s -a $DATADIR

#=== Request echoing of each command executed 
set -x

rm -rf $OUTDIR
mkdir -p $OUTDIR

date
start=$(date +%s)

# Mock Cellprofiler
./nyxus --useGpu=true --verbosity=0 --features=*FEATURESET1* --glcmAngles=0 --intDir=$DATADIR/int --segDir=$DATADIR/seg --outDir=$OUTDIR --filePattern=.* --csvFile=separatecsv --loaderThreads=1 --reduceThreads=8 

end=$(date +%s)
echo "Experiment: $EXPERIMENT_NAME Elapsed Time: $(($end-$start)) seconds"
echo "Experiment: $EXPERIMENT_NAME Elapsed Time: $(($end-$start)) seconds" > timing_$EXPERIMENT_NAME.txt
date

