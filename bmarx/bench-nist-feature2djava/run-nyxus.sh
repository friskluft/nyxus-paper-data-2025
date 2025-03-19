#!/bin/bash 

EXPERIMENT_NAME="Tissuenet"
DATADIR="/home/ec2-user/work/data/tissuenet"
OUTDIR="/home/ec2-user/work/data/OUTPUT-tissuenet"
ls -s -a $DATADIR

#=== Request echoing of each command executed 
set -x

rm -rf $OUTDIR
mkdir -p $OUTDIR

date
start=$(date +%s)

# Intensity:  
#   ./nyxus --useGpu=true --verbosity=0 --features=*ALL_INTENSITY* --intDir=$DATADIR/int --segDir=$DATADIR/seg --outDir=$OUTDIR --filePattern=.* --csvFile=separatecsv --loaderThreads=1 --reduceThreads=8 

# Morphology:  
#   ./nyxus --useGpu=true --verbosity=0 --features=AREA_PIXELS_COUNT,CENTROID_X,CENTROID_Y,BBOX_XMIN,BBOX_YMIN,BBOX_WIDTH,BBOX_HEIGHT,ORIENTATION,ECCENTRICITY,ASPECT_RATIO,EXTENT --intDir=$DATADIR/int --segDir=$DATADIR/seg --outDir=$OUTDIR --filePattern=.* --csvFile=separatecsv --loaderThreads=1 --reduceThreads=8 

# GLCM:  
#   ./nyxus --useGpu=true --verbosity=3 --features=GLCM_CONTRAST,GLCM_CORRELATION,GLCM_VARIANCE,GLCM_INVERSEDIFFERENCEMOMENT,GLCM_SUMAVERAGE,GLCM_SUMVARIANCE,GLCM_SUMENTROPY,GLCM_ENTROPY,GLCM_DIFFERENCEVARIANCE,GLCM_DIFFERENCEENTROPY --glcmAngles=0 --intDir=$DATADIR/int --segDir=$DATADIR/seg --outDir=$OUTDIR --filePattern=.* --csvFile=separatecsv --loaderThreads=1 --reduceThreads=8 

# Intensity + Morphology (as IMEA):  
#	./nyxus --useGpu=true --verbosity=0 --features=*ALL_INTENSITY*,AREA_PIXELS_COUNT,CENTROID_X,CENTROID_Y,BBOX_XMIN,BBOX_YMIN,BBOX_WIDTH,BBOX_HEIGHT,ORIENTATION,ECCENTRICITY,ASPECT_RATIO,EXTENT --intDir=$DATADIR/int --segDir=$DATADIR/seg --outDir=$OUTDIR --filePattern=.* --csvFile=separatecsv --loaderThreads=1 --reduceThreads=8 

# Intensity + Morphology + 4 GLCM features (as matlab IPT):  
./nyxus --useGpu=true --verbosity=0 --features=*ALL_INTENSITY*,AREA_PIXELS_COUNT,CENTROID_X,CENTROID_Y,BBOX_XMIN,BBOX_YMIN,BBOX_WIDTH,BBOX_HEIGHT,ORIENTATION,ECCENTRICITY,ASPECT_RATIO,EXTENT,GLCM_CONTRAST,GLCM_CORRELATION,GLCM_VARIANCE,GLCM_ENTROPY --intDir=$DATADIR/int --segDir=$DATADIR/seg --outDir=$OUTDIR --filePattern=.* --csvFile=separatecsv --loaderThreads=1 --reduceThreads=8 

# All together
#   ./nyxus --useGpu=true --verbosity=0 --features=*ALL_INTENSITY*,AREA_PIXELS_COUNT,CENTROID_X,CENTROID_Y,BBOX_XMIN,BBOX_YMIN,BBOX_WIDTH,BBOX_HEIGHT,ORIENTATION,ECCENTRICITY,ASPECT_RATIO,EXTENT,*ALL_GLCM* --glcmAngles=0 --intDir=$DATADIR/int --segDir=$DATADIR/seg --outDir=$OUTDIR --filePattern=.* --csvFile=separatecsv --loaderThreads=1 --reduceThreads=8 

end=$(date +%s)
echo "Experiment: $EXPERIMENT_NAME Elapsed Time: $(($end-$start)) seconds"
echo "Experiment: $EXPERIMENT_NAME Elapsed Time: $(($end-$start)) seconds" > timing_$EXPERIMENT_NAME.txt
date

