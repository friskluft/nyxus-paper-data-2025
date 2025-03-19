#!/bin/bash 

EXPERIMENT_NAME="banchmarking_Pyradiomics"

#	DATADIR="/home/ec2-user/work/data/mini"
#	OUTDIR="/home/ec2-user/work/data/OUTPUT-mini"
#	ls -s -a $DATADIR

#	IDIR = "/C/WORK/AXLE/benchmarks/bench-pyradiomics/sampledata-multisegment/int"
#	SDIR = "/C/WORK/AXLE/benchmarks/bench-pyradiomics/sampledata-multisegment/seg"
#	ODIR = "/C/WORK/AXLE/benchmarks/bench-pyradiomics/OUTPUT-pyradiomics"

IDIR="/home/kharchenkoa2/work/data/decathlon-splitroi-tif/int"
SDIR="/home/kharchenkoa2/work/data/decathlon-splitroi-tif/seg"
ODIR="/home/kharchenkoa2/work/bench-pyradiomics2024/OUT-pyrad"

#=== Request echoing of each command executed 
set -x

rm -rf $OUTDIR
mkdir -p $OUTDIR

date
start=$(date +%s)

# files=(/home/ec2-user/work/data/tissuenet/convert_int/*)
files=($IDIR/*)

for fpath in ${files[@]}
do
  fn=${fpath##*/}
  # pyradiomics "/home/ec2-user/work/data/tissuenet/convert_int/${fn}" "/home/ec2-user/work/data/tissuenet/convert_seg/${fn}" -o "/home/ec2-user/work/benchmarks/pyradiomics/OUTPUT-pyradiomics/${fn}.csv" --format csv --jobs 8 

  ls "$IDIR/${fn}"

  pyradiomics "$IDIR/${fn}" "$SDIR/${fn}" -o "$ODIR/${fn}.csv" --format csv --jobs 8 

done

end=$(date +%s)
echo "Experiment: $EXPERIMENT_NAME Elapsed Time: $(($end-$start)) seconds"
echo "Experiment: $EXPERIMENT_NAME Elapsed Time: $(($end-$start)) seconds" > timing_$EXPERIMENT_NAME.txt
date

