# Settings

IDIR = "C:\\WORK\\AXLE\\data\\tissuenet_v1_split\\step2_tissuenet_v1_train_int_flat_test"
SDIR = "C:\\WORK\\AXLE\\data\\tissuenet_v1_split\\step3_tissuenet_v1_train_mask_flat_test"
GREYDEPTH_MIN = 10
GREYDEPTH_MAX = 30

# NB: only coupled features
flist = ["GLCM_ASM_0","GLCM_ASM_45","GLCM_ASM_90","GLCM_ASM_135","GLCM_ACOR_0","GLCM_ACOR_45","GLCM_ACOR_90","GLCM_ACOR_135","GLCM_CLUPROM_0","GLCM_CLUPROM_45","GLCM_CLUPROM_90","GLCM_CLUPROM_135","GLCM_CLUSHADE_0","GLCM_CLUSHADE_45","GLCM_CLUSHADE_90","GLCM_CLUSHADE_135","GLCM_CLUTEND_0","GLCM_CLUTEND_45","GLCM_CLUTEND_90","GLCM_CLUTEND_135","GLCM_CONTRAST_0","GLCM_CONTRAST_45","GLCM_CONTRAST_90","GLCM_CONTRAST_135","GLCM_CORRELATION_0","GLCM_CORRELATION_45","GLCM_CORRELATION_90","GLCM_CORRELATION_135","GLCM_DIFAVE_0","GLCM_DIFAVE_45","GLCM_DIFAVE_90","GLCM_DIFAVE_135","GLCM_DIFENTRO_0","GLCM_DIFENTRO_45","GLCM_DIFENTRO_90","GLCM_DIFENTRO_135","GLCM_DIFVAR_0","GLCM_DIFVAR_45","GLCM_DIFVAR_90","GLCM_DIFVAR_135","GLCM_DIS_0","GLCM_DIS_45","GLCM_DIS_90","GLCM_DIS_135","GLCM_ENERGY_0","GLCM_ENERGY_45","GLCM_ENERGY_90","GLCM_ENERGY_135","GLCM_ENTROPY_0","GLCM_ENTROPY_45","GLCM_ENTROPY_90","GLCM_ENTROPY_135","GLCM_HOM1_0","GLCM_HOM1_45","GLCM_HOM1_90","GLCM_HOM1_135","GLCM_HOM2_0","GLCM_HOM2_45","GLCM_HOM2_90","GLCM_HOM2_135","GLCM_ID_0","GLCM_ID_45","GLCM_ID_90","GLCM_ID_135","GLCM_IDN_0","GLCM_IDN_45","GLCM_IDN_90","GLCM_IDN_135","GLCM_IDM_0","GLCM_IDM_45","GLCM_IDM_90","GLCM_IDM_135","GLCM_IDMN_0","GLCM_IDMN_45","GLCM_IDMN_90","GLCM_IDMN_135","GLCM_INFOMEAS1_0","GLCM_INFOMEAS1_45","GLCM_INFOMEAS1_90","GLCM_INFOMEAS1_135","GLCM_INFOMEAS2_0","GLCM_INFOMEAS2_45","GLCM_INFOMEAS2_90","GLCM_INFOMEAS2_135","GLCM_IV_0","GLCM_IV_45","GLCM_IV_90","GLCM_IV_135","GLCM_JAVE_0","GLCM_JAVE_45","GLCM_JAVE_90","GLCM_JAVE_135","GLCM_JE_0","GLCM_JE_45","GLCM_JE_90","GLCM_JE_135","GLCM_JMAX_0","GLCM_JMAX_45","GLCM_JMAX_90","GLCM_JMAX_135","GLCM_JVAR_0","GLCM_JVAR_45","GLCM_JVAR_90","GLCM_JVAR_135","GLCM_SUMAVERAGE_0","GLCM_SUMAVERAGE_45","GLCM_SUMAVERAGE_90","GLCM_SUMAVERAGE_135","GLCM_SUMENTROPY_0","GLCM_SUMENTROPY_45","GLCM_SUMENTROPY_90","GLCM_SUMENTROPY_135","GLCM_SUMVARIANCE_0","GLCM_SUMVARIANCE_45","GLCM_SUMVARIANCE_90","GLCM_SUMVARIANCE_135","GLCM_VARIANCE_0","GLCM_VARIANCE_45","GLCM_VARIANCE_90","GLCM_VARIANCE_135"]

import sys
import glob
import os
import matplotlib.pyplot as plt
import numpy as np
from nyxus import Nyxus
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing   # encoding labels -> integers
from sklearn import metrics
from tqdm import tqdm

def get_within_mean (f, columns, roiclasses, cls):
    sum = 0
    n = 0
    f.reset_index()
    for idx, row in tqdm(f.iterrows(), desc='mean '+cls):
        if roiclasses[idx] == cls:
            for c in columns:
                sum = sum + row[c]
                n = n+1
    m = sum / n
    return m

def get_global_mean (f, columns):
    m = 0
    n = 0
    f.reset_index()
    for idx, row in tqdm(f.iterrows(), desc='global mean'):
        for c in columns:
            m += row[c]
            n += 1
    return m/n

def get_within_var (f, columns, roiclasses, cls, m):
    sum = 0
    n = 0
    f.reset_index()
    for idx, row in tqdm(f.iterrows(), desc='within '+cls):
        if roiclasses[idx] == label:
            for c in columns:
                d = row[c] - m
                sum = sum + d*d    
                n += 1
    return sum / n

def get_between_var (f, columns):
    sum = 0
    n = 0
    # mean
    m = get_global_mean (f, columns)
    # variance
    f.reset_index()
    for idx, row in tqdm(f.iterrows()):
        for c in columns:
            d = row[c] - m
            sum = sum + d*d    
            n += 1
    return sum / n

def get_within_over_between (f, columns, roiclasses):
    C = set (roiclasses)
    withinVars = {}
    for cls in C:
        m = get_within_mean (f, columns, roiclasses, cls)
        v = get_within_var (f, columns, roiclasses, cls, m)
        withinVars[cls] = v
        print('within class', cls, 'mean=', m, 'var=', v)
        
    print('between')
    glbVar = get_between_var (f, columns)
    print('glbVar=', glbVar)
    
    # the final metric
    sumW = 0
    for v in withinVars:
        sumW += withinVars[v]
    print('total withinVar=',sumW)
    sumWOB = sumW / glbVar
    return sumWOB

def normalize_cols (f, columns):
    ret = f
    for c in tqdm(columns):
        ret[c]=(f[c] - f[c].min()) / (f[c].max() - f[c].min())
    return ret

# quickly extract features. We need them only for class labels
nyx = Nyxus(["MEAN"])
F = nyx.featurize_directory (IDIR, SDIR, file_pattern='.*_c0.*', output_type='pandas')

# mine class labels (note: labels are positional)
L = [] 
for idx, row in tqdm(F.iterrows()):
    fname = row['mask_image']
    label = fname.split("_")[-3]
    L.append(label)

U = set(L)
print(f"labels: {U}")

# prepare buffers
X = [i for i in range(GREYDEPTH_MIN, GREYDEPTH_MAX, 5)] # gray depths
Y = [] # future wb-statistic values
print(f"buffers - ready X={X}")

# extract features parameterized by 'X' and calculate stats
print("beginning iterations")
for nG in tqdm(X):
    print('------------- nG=', nG, ' -------------------')
    
    # featurize
    nyx = Nyxus(["*ALL_GLCM*"])
    nyx.set_metaparam ("glcm/greydepth=" + str(nG))
    nyx.set_metaparam ("glcm/offset=1")
    F = nyx.featurize_directory (IDIR, SDIR, '.*_c0.ome.tif')   
    
    # suppress NANs
    F.replace ([np.inf, -np.inf], np.nan, inplace=True)
    F.replace (np.nan, 0.0, inplace=True)
    
    # normalize
    Fn = normalize_cols (F, flist)    
    
    # calculate WOB
    wob = get_within_over_between (Fn, flist, L)
    print ('WOB=', wob)
    Y.append (wob)

# save the series
fdir = "C:/WORK/AXLE/demo-2023-07__REMAKE/"
fname = "XY_grey2wob1s" + str(GREYDEPTH_MIN) + "-" + str(GREYDEPTH_MAX) + ".csv"
print (f"saving the series as {(fdir+"/"+fname)}")
Y_ = [1.0*y for y in Y]    # amplify/attenuate if needed
dfXY = pd.DataFrame ({'X': X, 'Y': Y_ })
dfXY.to_csv (fdir+"/"+fname)

