#!/bin/bash

EXPERIMENT_NAME="radiomicsJ"

DATADIR="/home/ec2-user/work/data/mini"
OUTFILE="out"
ls -s -a $DATADIR

#=== Request echoing of each command executed
set -x

date
start=$(date +%s)

#===  Calculate all the features
# declare -a arr=("ALL")

#=== Intensity
# declare -a arr=("IntensityBasedStatistics" "IntensityHistogram" "LocalIntensityFeatures")

#=== Texture
# declare -a arr=("GLCM" "GLDZM" "NGLDM" "GLSZM" "NGTDM")

#=== Shape
# declare -a arr=("Morphological" "Shape2D")

#=== Miscellanea
declare -a arr=("Fractal" "Diagnostics")

#=== Calculate specific feature groups
#declare -a arr=(
#    "GLCM"
#    "GLDZM"
#    "NGLDM"
#    "GLSZM"
#    "NGTDM"
#    "Morphological"
#    "Shape2D"
#    "IntensityBasedStatistics"
#    "IntensityHistogram"
#    "Fractal"
#    "Diagnostics"
#    "LocalIntensityFeatures"
#)

# featureSelection=${(j:+:)arr} # <--zsh
featureSelection=$(IFS=_ ; echo "${arr[*]}") # <-- bash
echo $featureSelection > feature_selection.txt

rm out_$featureSelection/*
mkdir out_$featureSelection

> timing_$EXPERIMENT_NAME.txt

for i in "${arr[@]}"
do 
    touch out/"$i.csv"
    java -jar target/RadiomicsJ-jar-with-dependencies.jar -i $DATADIR/int -m $DATADIR/seg -o $OUTFILE/"$i.csv" -features "$i" 
done 

date
end=$(date +%s)
echo ">>> $EXPERIMENT_NAME Elapsed Time: $(($end-$start)) seconds"
echo ">>> $EXPERIMENT_NAME Elapsed Time: $(($end-$start)) seconds" >> timing_$EXPERIMENT_NAME_$featureSelection.txt


