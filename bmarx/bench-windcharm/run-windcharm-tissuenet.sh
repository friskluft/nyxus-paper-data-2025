#!/bin/bash 

#==== https://www.baeldung.com/linux/bash-calculate-time-elapsed 

date

start=$(date +%s)
/home/ec2-user/work/wnd-charm-Morphology/build3/wndchrm.exe --DataPath /home/ec2-user/work/data/tissuenet/intensity --LabeledData /home/ec2-user/work/data/tissuenet/labels --ImageTransformationName Original --FeatureAlgorithmName Morphological --output ./ 
end=$(date +%s)
echo "Elapsed Time: $(($end-$start)) seconds"

date

#=== Results
#	Segmentation fault on p3_y1_r48_c1.ome.sig (~60%)
#	1341 seconds (1341 / 6 * 10 = 2235)
