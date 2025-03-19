#!/bin/bash

EXEPATH="/home/kharchenkoa2/work/windcharm-morphology/build3/wndchrm.exe"
IDIR="/home/kharchenkoa2/work/data/decathlon/output/int"
SDIR="/home/kharchenkoa2/work/data/decathlon/output/seg"
ODIR="/home/kharchenkoa2/work/data/OUT-wc-SHAPE"
TIMEFILE="timing_decathlon_SHAPE.txt"
FEATURESET="Morphological" # See file c:\work\axle\wnd-charm\wnd-charm-morphology-aws\src\Tasks.cpp

# BGND on timing:  https://www.baeldung.com/linux/bash-calculate-time-elapsed

date

# protocol
echo "*** SHAPE" >> $TIMEFILE
date >> $TIMEFILE
echo "EXEPATH" $EXEPATH >> $TIMEFILE
echo "IDIR" $IDIR >> $TIMEFILE
echo "SDIR" $SDIR >> $TIMEFILE
echo "ODIR" $ODIR >> $TIMEFILE
echo "processing...">> $TIMEFILE

start=$(date +%s)
$EXEPATH --DataPath $IDIR --LabeledData $SDIR --ImageTransformationName Original --FeatureAlgorithmName $FEATURESET --output $ODIR
end=$(date +%s)

# protocol
echo "Elapsed Time: $(($end-$start)) seconds" >> $TIMEFILE

echo "Elapsed Time: $(($end-$start)) seconds"

date

