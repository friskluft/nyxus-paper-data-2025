#!/bin/bash

EXEPATH="/home/kharchenkoa2/work/nyxusbuild1/nyxus"
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


FPATT="synthetic_nrois=500000_roiarea=10\.ome\.tif"
TIMEFILE="run_nyxus_synthetic_timing_n500000_s10.output"

	# timing
	date
	start=$(date +%s)

	# run Nyxus
	$EXEPATH --filePattern=$FPATT --intDir=$DATADIR/int --segDir=$DATADIR/seg --outDir=$OUTDIR --resultFname=f_tissuenet --verbose=1 --useGpu=true --outputType=singlecsv --features=*ALL* --reduceThreads=8 

	# timing
	end=$(date +%s)
	echo "Image: $FPATT Elapsed Time: $(($end-$start)) seconds"
	printf "FPATT: $FPATT \nDATADIR: $DATADIR \nOUTDIR: $OUTDIR \nSETTINGSFILE: $SETTINGSFILE \nElapsed Time: $(($end-$start)) seconds \n" > $TIMEFILE
	date

FPATT="synthetic_nrois=500000_roiarea=100\.ome\.tif"
TIMEFILE="run_nyxus_synthetic_timing_n500000_s100.output"

	# timing
	date
	start=$(date +%s)

	# run Nyxus
	$EXEPATH --filePattern=$FPATT --intDir=$DATADIR/int --segDir=$DATADIR/seg --outDir=$OUTDIR --resultFname=f_tissuenet --verbose=1 --useGpu=true --outputType=singlecsv --features=*ALL* --reduceThreads=8 

	# timing
	end=$(date +%s)
	echo "Image: $FPATT Elapsed Time: $(($end-$start)) seconds"
	printf "FPATT: $FPATT \nDATADIR: $DATADIR \nOUTDIR: $OUTDIR \nSETTINGSFILE: $SETTINGSFILE \nElapsed Time: $(($end-$start)) seconds \n" > $TIMEFILE
	date

FPATT="synthetic_nrois=500000_roiarea=500\.ome\.tif"
TIMEFILE="run_nyxus_synthetic_timing_n500000_s500.output"

	# timing
	date
	start=$(date +%s)

	# run Nyxus
	$EXEPATH --filePattern=$FPATT --intDir=$DATADIR/int --segDir=$DATADIR/seg --outDir=$OUTDIR --resultFname=f_tissuenet --verbose=1 --useGpu=true --outputType=singlecsv --features=*ALL* --reduceThreads=8 

	# timing
	end=$(date +%s)
	echo "Image: $FPATT Elapsed Time: $(($end-$start)) seconds"
	printf "FPATT: $FPATT \nDATADIR: $DATADIR \nOUTDIR: $OUTDIR \nSETTINGSFILE: $SETTINGSFILE \nElapsed Time: $(($end-$start)) seconds \n" > $TIMEFILE
	date

FPATT="synthetic_nrois=500000_roiarea=1000\.ome\.tif"
TIMEFILE="run_nyxus_synthetic_timing_n500000_s1000.output"

	# timing
	date
	start=$(date +%s)

	# run Nyxus
	$EXEPATH --filePattern=$FPATT --intDir=$DATADIR/int --segDir=$DATADIR/seg --outDir=$OUTDIR --resultFname=f_tissuenet --verbose=1 --useGpu=true --outputType=singlecsv --features=*ALL* --reduceThreads=8 

	# timing
	end=$(date +%s)
	echo "Image: $FPATT Elapsed Time: $(($end-$start)) seconds"
	printf "FPATT: $FPATT \nDATADIR: $DATADIR \nOUTDIR: $OUTDIR \nSETTINGSFILE: $SETTINGSFILE \nElapsed Time: $(($end-$start)) seconds \n" > $TIMEFILE
	date

FPATT="synthetic_nrois=500000_roiarea=10000\.ome\.tif"
TIMEFILE="run_nyxus_synthetic_timing_n500000_s10000.output"

	# timing
	date
	start=$(date +%s)

	# run Nyxus
	$EXEPATH --filePattern=$FPATT --intDir=$DATADIR/int --segDir=$DATADIR/seg --outDir=$OUTDIR --resultFname=f_tissuenet --verbose=1 --useGpu=true --outputType=singlecsv --features=*ALL* --reduceThreads=8 

	# timing
	end=$(date +%s)
	echo "Image: $FPATT Elapsed Time: $(($end-$start)) seconds"
	printf "FPATT: $FPATT \nDATADIR: $DATADIR \nOUTDIR: $OUTDIR \nSETTINGSFILE: $SETTINGSFILE \nElapsed Time: $(($end-$start)) seconds \n" > $TIMEFILE
	date

FPATT="synthetic_nrois=500000_roiarea=100000\.ome\.tif"
TIMEFILE="run_nyxus_synthetic_timing_n500000_s100000.output"

	# timing
	date
	start=$(date +%s)

	# run Nyxus
	$EXEPATH --filePattern=$FPATT --intDir=$DATADIR/int --segDir=$DATADIR/seg --outDir=$OUTDIR --resultFname=f_tissuenet --verbose=1 --useGpu=true --outputType=singlecsv --features=*ALL* --reduceThreads=8 

	# timing
	end=$(date +%s)
	echo "Image: $FPATT Elapsed Time: $(($end-$start)) seconds"
	printf "FPATT: $FPATT \nDATADIR: $DATADIR \nOUTDIR: $OUTDIR \nSETTINGSFILE: $SETTINGSFILE \nElapsed Time: $(($end-$start)) seconds \n" > $TIMEFILE
	date





