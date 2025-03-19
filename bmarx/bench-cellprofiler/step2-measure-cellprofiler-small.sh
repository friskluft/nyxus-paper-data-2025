#!/bin/bash 

# *** SCRIPT TO RUN A SMALL FEATURE EXTRACTION FOR THE ACCURACY TEST ***

# Clean up results of a previous run
rm -rf  ./SCRATCHSPACE/OUTPUTSMALL/*

# Extract features
date
start=$(date +%s)
docker run -it --mount type=bind,source=/home/kharchenkoa2/work/bench-cellprofiler/SCRATCHSPACE,target=/playground 580ba77ce146 -p /playground/cellprofiler_4.2.4.cpipe -i /playground/SMALLDATA -o /playground/SMALLOUTPUT
end=$(date +%s)
echo "Elapsed Time: $(($end-$start)) seconds"
date
