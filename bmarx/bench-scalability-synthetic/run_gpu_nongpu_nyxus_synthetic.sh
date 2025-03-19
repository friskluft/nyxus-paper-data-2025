#!/bin/bash

####################################################################
EXEPATH="/home/kharchenkoa2/work/nyxus-softtuning/BLD2/nyxus"
DATADIR="/home/kharchenkoa2/work/data/synthetic3"
OUTDIR="/home/kharchenkoa2/work/data/OUT-tissuenet"
####################################################################

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

####################################################################
N="100000"
eyeN="100k" # eye-friendly N
S="100"
eyeS="100"
FPATT="synthetic_nrois=${N}_roiarea=${S}\.ome\.tif"
####################################################################

	USEGPU="TRUE" #### <---ACHTUNG!
	TIMEFILE="gpunogpu_n${eyeN}_s${eyeS}_gpu=${USEGPU}.output"
	launchNyx


####################################################################
N="100000"
eyeN="100k" # eye-friendly N
S="1000"
eyeS="1K"
FPATT="synthetic_nrois=${N}_roiarea=${S}\.ome\.tif"
####################################################################

	USEGPU="TRUE" #### <---ACHTUNG!
	TIMEFILE="gpunogpu_n${eyeN}_s${eyeS}_gpu=${USEGPU}.output"
	launchNyx


####################################################################
N="100000"
eyeN="100k" # eye-friendly N
S="10000"
eyeS="10K"
FPATT="synthetic_nrois=${N}_roiarea=${S}\.ome\.tif"
####################################################################

	USEGPU="TRUE" #### <---ACHTUNG!
	TIMEFILE="gpunogpu_n${eyeN}_s${eyeS}_gpu=${USEGPU}.output"
	launchNyx


####################################################################
N="100000"
eyeN="100k" # eye-friendly N
S="100000"
eyeS="100K"
FPATT="synthetic_nrois=${N}_roiarea=${S}\.ome\.tif"
####################################################################

	USEGPU="TRUE" #### <---ACHTUNG!
	TIMEFILE="gpunogpu_n${eyeN}_s${eyeS}_gpu=${USEGPU}.output"
	launchNyx



#
#	USEGPU="FALSE" #### <---ACHTUNG!
#	TIMEFILE="gpunogpu_n${eyeN}_s${eyeS}_gpu=${USEGPU}.output"
#
#		launchNyx






