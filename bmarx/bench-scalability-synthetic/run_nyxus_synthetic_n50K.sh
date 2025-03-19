#!/bin/bash

EXEPATH="/home/kharchenkoa2/work/nyxus-softtuning/BLD2/nyxus"
DATADIR="/home/kharchenkoa2/work/data/synthetic3"
OUTDIR="/home/kharchenkoa2/work/data/OUT-tissuenet"

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

launchNyx()
{
	echo "---------- $FPATT $DATADIR $TIMEFILE"

	# check availability in int and seg subdirectories

	# __ convert file pattern into proper file name for [[-e]]
	#	BGND: https://stackoverflow.com/questions/2871181/replacing-some-characters-in-a-string-with-another-character
	fname="${FPATT//\\./.}"
	echo $FPATT
	echo $fname

	if [[ ! -e $DATADIR/int/$fname ]] ; then
		echo "unavailable $DATADIR/int/$fname" > error_$fname
		exit 1
	fi

        if [[ ! -e $DATADIR/seg/$fname ]] ; then
                echo "unavailable $DATADIR/seg/$fname" > error_$fname
                exit 1
        fi

        # timing
        date
        start=$(date +%s)

        # run Nyxus
        $EXEPATH --useGpu=$USEGPU --filePattern=$FPATT --intDir=$DATADIR/int --segDir=$DATADIR/seg --outDir=$OUTDIR --resultFname=f_synth_$eyeN --verbose=1 --outputType=singlecsv --features=*ALL* --reduceThreads=8

        # timing
        end=$(date +%s)
        echo "Image: $FPATT Elapsed Time: $(($end-$start)) seconds"
        printf "FPATT: $FPATT \nUSEGPU: $USEGPU\nDATADIR: $DATADIR \nOUTDIR: $OUTDIR \nSETTINGSFILE: $SETTINGSFILE \nElapsed Time: $(($end-$start)) seconds \n" > $TIMEFILE
        date
}

#----------------------------

N="50000"
eyeN="50K" # eye-friendly N
USEGPU="TRUE"

#----------------------------

FPATT="synthetic_nrois=${N}_roiarea=100\.ome\.tif"
TIMEFILE="kunstig_tid_n${eyeN}_s100_usegpu=${USEGPU}.output"

	launchNyx

FPATT="synthetic_nrois=${N}_roiarea=1000\.ome\.tif"
TIMEFILE="kunstig_tid_n${eyeN}_s1K_usegpu=${USEGPU}.output"
 
 	launchNyx
 
FPATT="synthetic_nrois=${N}_roiarea=10000\.ome\.tif"
TIMEFILE="kunstig_tid_n${eyeN}_s10K_usegpu=${USEGPU}.output"
 
 	launchNyx
 
FPATT="synthetic_nrois=${N}_roiarea=100000\.ome\.tif"
TIMEFILE="kunstig_tid_n${eyeN}_s100K_usegpu=${USEGPU}.output"

	launchNyx






