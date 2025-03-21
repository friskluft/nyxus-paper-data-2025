# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 12:16:44 2022

@author: udvikler
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt
import imea
import os
import pandas as pd
import datetime

#Timing
t_a = datetime.datetime.now()

'''
# Test Imea
bw = np.zeros((50, 50), dtype='bool')
bw[10:20, 10:20] = True
bw[22:32, 10:20] = True
bw[34:44, 10:20] = True
shape_measurements = imea.shape_measurements_2d(bw)
print ('shape_measurements=' + str(shape_measurements))
'''

'''
# Test CV2
img = cv2.imread('C:\WORK\AXLE\data\mini\seg\p0_y1_r1_c0.ome.tif', 2)
ret, threshold1 = cv2.threshold (img, 14, 16, cv2.THRESH_BINARY)
threshold2 = cv2.inRange (img, 14, 14)
titles = ['original', 'thresholded1', 'thresholded2']
images = [img, threshold2, threshold1]
for i in range(2):
    plt.subplot (3,2,i+1), plt.imshow (images[i], 'gray')
    plt.title(titles[i])
    plt.xticks([]), plt.yticks([])
plt.show()
print(img)
'''

dir = '/home/kharchenkoa2/work/data/decathlon/output/seg'
out_dir = '/home/kharchenkoa2/work/bench-imea/OUT-decathlon'

# iterate over files in
# that directory
n_digestedFslides = 0	# for progress
Slides = os.listdir(dir)
n_slides = len(Slides)
for fn in Slides:
    f = os.path.join(dir, fn)
    # checking if it is a file
    if os.path.isfile(f):

        # progress
        # (slide no.)
        n_digestedFslides = n_digestedFslides + 1
        perc = float(n_digestedFslides) / float(n_slides) * 100.
        # (time)
        t_elapRunning = datetime.datetime.now() - t_a
        #
        print (f'{perc} %\t{t_elapRunning.seconds} s\tfile {f}')

        # Prepare the destination
        feResult = []
        f_csv = os.path.join (out_dir, fn) + '.csv'
        # Read the image
        img = cv2.imread(f, 2)
        # iterate labels
        print('\tLABELS', end=' ', flush=True)
        unkLabels = np.unique(img)
	
        # any ROI in this slide?
        if len(unkLabels) < 2:
            print (f'file {f} : no ROI')
            continue
	
        for label in unkLabels:
            if (label == 0):
                continue
            print (f'{label} ', end='', flush=True)
            threshed = cv2.inRange (img, int(label), int(label))
            bw = np.array (threshed, dtype='bool')
            #--debug-- print(bw)		
            fvals = imea.shape_measurements_2d (bw)
            feResult.append(fvals)
        print ('DONE', flush=True)
        # Output
        feResult = pd.concat(feResult)
        feResult.to_csv(f_csv)

# Timing
t_b = datetime.datetime.now()
t_elap = t_b - t_a
print (t_elap.seconds, 'seconds')
print (t_elap.microseconds, 'microseconds')

