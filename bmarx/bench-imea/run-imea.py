

import os
import cv2
import numpy as np
#from matplotlib import pyplot as plt
import imea

# Test Imea
bw = np.zeros((50, 50), dtype='bool')
bw[10:20, 10:20] = True
bw[22:32, 10:20] = True
bw[34:44, 10:20] = True
shape_measurements = imea.shape_measurements_2d(bw)
print ('shape_measurements=' + str(shape_measurements))

# assign directory
dir = '/home/ec2-user/work/data/mini/seg'
 
# iterate over files in
# that directory
for fn in os.listdir(dir):
    f = os.path.join(dir, fn)
    # checking if it is a file
    if os.path.isfile(f):
        print (f)
        img = cv2.imread(f, 2)
        threshed = cv2.inRange (img, 14, 14)
        bw = np.array (threshed, dtype='bool')
        type(bw)
        print (bw)
        shape_measurements = imea.shape_measurements_2d (bw, 0.001)
        print ('shape_measurements=' + str(shape_measurements))
