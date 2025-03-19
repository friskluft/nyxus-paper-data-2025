#!/bin/bash 

EXPERIMENT_NAME="banc-mini-Decathlon-pyradiomics"

#	DATADIR="/home/ec2-user/work/data/mini"
#	OUTDIR="/home/ec2-user/work/data/OUTPUT-mini"
#	ls -s -a $DATADIR

#	IDIR = "/C/WORK/AXLE/benchmarks/bench-pyradiomics/sampledata-multisegment/int"
#	SDIR = "/C/WORK/AXLE/benchmarks/bench-pyradiomics/sampledata-multisegment/seg"
#	ODIR = "/C/WORK/AXLE/benchmarks/bench-pyradiomics/OUTPUT-pyradiomics"

IDIR="/home/kharchenkoa2/work/data/decathlon-splitroi-tif/int"
SDIR="/home/kharchenkoa2/work/data/decathlon-splitroi-tif/seg"
ODIR="/home/kharchenkoa2/work/bench-pyradiomics2024/OUT-pyrad-SHAPE"	# watch --param ./mr_2d_extraction_XYZ.yaml below !!!

#=== Request echoing of each command executed 
set -x

rm -rf $OUTDIR
mkdir -p $OUTDIR

date
start=$(date +%s)

echo "Experiment: $EXPERIMENT_NAME starting: $($start) seconds" > timing_$EXPERIMENT_NAME.txt

# files=(/home/ec2-user/work/data/tissuenet/convert_int/*)
files=($IDIR/*)

for fpath in ${files[@]}
do
  fn=${fpath##*/}

  #ls "$IDIR/${fn}"
  tentEnd=$(date +%s)
  echo "--------------------- timestamp: $(($tentEnd-$start)) s"

  pyradiomics "$IDIR/${fn}" "$SDIR/${fn}" -o "$ODIR/${fn}.csv" --format csv --jobs 8 --param ./mr_2d_extraction_SHAPE.yaml

done

end=$(date +%s)
echo "Experiment: $EXPERIMENT_NAME Elapsed Time: $(($end-$start)) seconds"
echo "Experiment: $EXPERIMENT_NAME Elapsed Time: $(($end-$start)) seconds" >> timing_$EXPERIMENT_NAME.txt
date

