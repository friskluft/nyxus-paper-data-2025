#!/bin/bash 

# Clean up results of a previous run
rm -rf  ./SCRATCHSPACE/OUTPUT/*

# Extract features
date
start=$(date +%s)
docker run -it --mount type=bind,source=/home/ec2-user/work/benchmarks/cellprofiler/SCRATCHSPACE,target=/playground 580ba77ce146 -p /playground/cellprofiler_4.2.4.cpipe -i /playground/DATA -o /playground/OUTPUT
end=$(date +%s)
echo "Elapsed Time: $(($end-$start)) seconds"
date
