#!/bin/bash 

#0) Pull Cellprofiler 4.2.4's Docker image from https://hub.docker.com/r/cellprofiler/cellprofiler/tags:
docker pull cellprofiler/cellprofiler:4.2.4

# (Why this Cellprofiler version? - Because our pipeline file is for Cellprofiler version 4.2.4 exactly.)

#1) Create directories for the data and output:
mkdir SCRATCHSPACE
mkdir SCRATCHSPACE/DATA
mkdir SCRATCHSPACE/OUTPUT  

(Idea of doing this - isolate the image from corrupting data on our test machine.)

#2) Copy the data
cp -R ~/work/data/tissuenet/int ./SCRATCHSPACE/DATA
cp -R ~/work/data/tissuenet/seg ./SCRATCHSPACE/DATA

#3) Copy the pipeline file 
cp cellprofiler_4.2.4.cpipe ./SCRATCHSPACE

#4) Pull a Cellprofiler Docker image:

docker pull cellprofiler/cellprofiler
docker images

#5) Assuming the image is 580ba77ce146 we can run it versus our data and pipeline with command
#
#       docker run -it --mount type=bind,source=/home/ec2-user/work/benchmarks/cellprofiler/SCRATCHSPACE,target=/playground 580ba77ce146 -p /playground/cellprofiler_4.2.4.cpipe -i /playground/DATA -o /playground/OUTPUT
#
# or a separate measurement command:

nohup ./step2_measure.sh > console_output.txt &

# The contents of file measure.sh is the following:

#       # Clean up results of a previous run
#       rm -rf  ./SCRATCHSPACE/OUTPUT/*
#
#       # Extract features
#       date
#       start=$(date +%s)
#       docker run -it --mount type=bind,source=/home/ec2-user/work/benchmarks/cellprofiler/SCRATCHSPACE,target=/playground 580ba77ce146 -p /playground/cellprofiler_4.2.4.cpipe -i /playground/DATA -o /playground/OUTPUT
#       end=$(date +%s)
#       echo "Elapsed Time: $(($end-$start)) seconds"
#       date
