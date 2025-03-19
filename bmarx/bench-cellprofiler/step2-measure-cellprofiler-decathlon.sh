#!/bin/bash 

# *** SCRIPT TO RUN A SMALL FEATURE EXTRACTION FOR THE ACCURACY TEST ***

# Clean up results of a previous run
##################### rm -rf  ./SCRATCHSPACE/OUTPUTSMALL/*

# Extract features
date
start=$(date +%s)
docker run -it --mount type=bind,source=/home/kharchenkoa2/work/data/decathlon/output,target=/playground 580ba77ce146 -p /playground/cellprofiler_4.2.4.cpipe -i /playground/ -o /playground/OUTCELLPROFILER
end=$(date +%s)
echo "Elapsed Time: $(($end-$start)) seconds"
date
