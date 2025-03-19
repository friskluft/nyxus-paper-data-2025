#!/bin/bash 

#==== https://www.baeldung.com/linux/bash-calculate-time-elapsed 

date

start=$(date +%s)

# -- extract morphology
/home/ec2-user/work/wnd-charm-Morphology/build3/wndchrm.exe --DataPath /home/ec2-user/work/benchmarks/cellprofiler/SCRATCHSPACE/SMALLDATA/int --LabeledData /home/ec2-user/work/benchmarks/cellprofiler/SCRATCHSPACE/SMALLDATA/seg --ImageTransformationName original --FeatureAlgorithmName Morphological --output ./ 

# -- save the result
mv ./output.csv ./accuracy-output-morphology.csv

# -- extract intensity
/home/ec2-user/work/wnd-charm-Morphology/build3/wndchrm.exe --DataPath /home/ec2-user/work/benchmarks/cellprofiler/SCRATCHSPACE/SMALLDATA/int --LabeledData /home/ec2-user/work/benchmarks/cellprofiler/SCRATCHSPACE/SMALLDATA/seg --ImageTransformationName original --FeatureAlgorithmName PixelIntensityStatistics --output ./

# -- save the result
mv ./output.csv ./accuracy-output-intensity.csv

end=$(date +%s)
echo "Elapsed Time: $(($end-$start)) seconds"

date

#=== Results
#	Segmentation fault on p3_y1_r48_c1.ome.sig (~60%)
#	1341 seconds (1341 / 6 * 10 = 2235)
