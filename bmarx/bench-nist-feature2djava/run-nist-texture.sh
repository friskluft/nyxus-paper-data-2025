#!/bin/bash

IDIR="/data/decathlon/output/int"
SDIR="/data/decathlon/output/seg"
ODIR="/data/OUT-nistjavaplugin-texture"

set -e	# exitscript on error
set -x	# display each command

#==== Plugin v0.1.4 lives here https://hub.docker.com/r/wipp/wipp-feature2djava-plugin/tags

date

start=$(date +%s)

# Intensity: --features Feature2DJava_Mean,Feature2DJava_Entropy,Feature2DJava_Median,Feature2DJava_Mode,Feature2DJava_StandardDeviation,Feature2DJava_Skewness,Feature2DJava_Kurtosis,Feature2DJava_Hyperskewness,Feature2DJava_Hyperflatness
# Shape: --features Feature2DJava_Area,Feature2DJava_Aspect_Ratio_BB,Feature2DJava_Bounding_Box,Feature2DJava_Center_BB,Feature2DJava_Centroid,Feature2DJava_Circularity,Feature2DJava_Distance_From_Border,Feature2DJava_Eccentricity,Feature2DJava_ExtendBB,Feature2DJava_Orientation,Feature2DJava_Perimeter
# Texture: --features Feature2DJava_TContrast,Feature2DJava_TCorrelation,Feature2DJava_THomogeneity,Feature2DJava_TEnergy,Feature2DJava_TVariance,Feature2DJava_TEntropy,Feature2DJava_TInvDiffMoment,Feature2DJava_TSumAverage,Feature2DJava_TSumVariance,Feature2DJava_TSumEntropy,Feature2DJava_TDiffAverage,Feature2DJava_TDiffVariance,Feature2DJava_TDiffEntropy

features_texture="Feature2DJava_TContrast,Feature2DJava_TCorrelation,Feature2DJava_THomogeneity,Feature2DJava_TEnergy,Feature2DJava_TVariance,Feature2DJava_TEntropy,Feature2DJava_TInvDiffMoment,Feature2DJava_TSumAverage,Feature2DJava_TSumVariance,Feature2DJava_TSumEntropy,Feature2DJava_TDiffAverage,Feature2DJava_TDiffVariance,Feature2DJava_TDiffEntropy"
docker run -it --mount type=bind,source=/home/kharchenkoa2/work/data,target=/data 55cc0153ebb1 --imageDir $IDIR --partitionsDir $SDIR --iP ".*" --pP ".*" --outputDir $ODIR --features $features_texture

end=$(date +%s)
echo "Elapsed Time: $(($end-$start)) seconds"
echo "***" >> timing_texture.txt
date >> timing_texture.txt
echo $IDIR >> timing_texture.txt
echo $SDIR >> timing_texture.txt
echo $features_texture >> timing_texture.txt
echo "$(($end-$start)) seconds" >> timing_texture.txt

date
