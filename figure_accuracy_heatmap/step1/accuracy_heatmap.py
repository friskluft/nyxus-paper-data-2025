import math # NAN, INF checks
import numpy as np
import pandas as pd

#**** option: IBSI ****   
NYXUS_INPUT = "C:\\WORK\\AXLE\\paper2022\\accuracyHeatmap\\nyxus_accuracy_common.csv"   # IBSI enabled
RESULTFILE = "C:\\WORK\\AXLE\\paper2022\\accuracyHeatmap\\__raw_heatmap_data__IBSI.csv" # IBSI enabled

#**** option: NO IBSI ****  
''' 
NYXUS_INPUT = "C:\\WORK\\AXLE\\paper2022\\accuracyHeatmap\\nyxus_accuracy_textureASpyr_noibsi.csv"
RESULTFILE = "C:\\WORK\\AXLE\\paper2022\\accuracyHeatmap\\__raw_heatmap_data__NOIBSI.csv"
'''

CORRMETHOD = 'pearson'
NOTAVAILABLE = -1
SPACER = -1

# Feature extraction results

#--- assemble Nyxus
R_nyx_common = pd.read_csv (NYXUS_INPUT) # no IBSI

# purpose of mocking: GLCM with Matlab
# command line: 
#       --ibsi=0 --coarseGrayDepth=100 --glcmOffset=1 --features=*ALL_GLCM* --resultFname=nyxus_accuracy_mock_matlab --outDir=C:\WORK\AXLE\data\OUTPUT --verbose=3 --useGpu=false --outputType=singlecsv --intDir=C:\WORK\AXLE\benchmarks\bench-pyradiomics\sampledata-tissuenet\int --segDir=C:\WORK\AXLE\benchmarks\bench-pyradiomics\sampledata-tissuenet\seg --filePattern=p0_y1_r100_c0\.ome\.tif --reduceThreads=1 
R_nyx_matlab = pd.read_csv ("C:\\WORK\\AXLE\\paper2022\\accuracyHeatmap\\nyxus_accuracy_mock_matlab.csv") 
Cols = R_nyx_matlab.columns
for col in Cols:
    R_nyx_matlab.rename (columns={col: 'mockmatlab_'+col}, inplace=True)

# purpose of mocking: GABOR  with WC
# command line: 
#       --gaborthold=0.1 --gaborfreqs=1,2,3,4,5,6,7 --gabortheta=90,90,90,90,90,90,90 --gaborgamma=0.5 --gaborsig2lam=0.56 --gaborf0=0.1 --gaborkersize=38 --features=GABOR --resultFname=nyxus_accuracy_mock_wc --outDir=C:\WORK\AXLE\data\OUTPUT --verbose=3 --useGpu=false --outputType=singlecsv --intDir=C:\WORK\AXLE\benchmarks\bench-pyradiomics\sampledata-tissuenet\int --segDir=C:\WORK\AXLE\benchmarks\bench-pyradiomics\sampledata-tissuenet\seg --filePattern=p0_y1_r100_c0\.ome\.tif --reduceThreads=1 
R_nyx_wc = pd.read_csv ("C:\\WORK\\AXLE\\paper2022\\accuracyHeatmap\\nyxus_accuracy_mock_wc.csv") 
Cols = R_nyx_wc.columns
for col in Cols:
    R_nyx_wc.rename (columns={col: 'mockwc_'+col}, inplace=True)

R_nyx = pd.concat ([R_nyx_matlab, R_nyx_wc, R_nyx_common], axis=1)
#---

R_cp = pd.read_csv ("C:\\WORK\\AXLE\\paper2022\\accuracyHeatmap\\cellprofiler_cp_labelobj.csv")
R_imea = pd.read_csv ("C:\\WORK\\AXLE\\paper2022\\accuracyHeatmap\\imea_accuracy_p0_y1_r100_c0.ome.tif.csv")
R_matlab = pd.read_csv ("C:\\WORK\\AXLE\\paper2022\\accuracyHeatmap\\matlab_features_tissuenet_accuracy.csv")
R_nist = pd.read_csv ("C:\\WORK\\AXLE\\paper2022\\accuracyHeatmap\\nist_accuracy_p0_y1_r100_c0.ome.tif.csv")
R_pyr = pd.read_csv ("C:\\WORK\\AXLE\\paper2022\\accuracyHeatmap\\pyradiomics_accuracy_p0_y1_r100_c0.tiff.csv")
R_radj = pd.read_csv ("C:\\WORK\\AXLE\\paper2022\\accuracyHeatmap\\RadiomicsFeatures-20240129192450150__p0_y1_r100_c0.ome.tif.csv")

# -- assemble WND-CHARM
R_wc_haralick = pd.read_csv ("C:\\WORK\\AXLE\\paper2022\\accuracyHeatmap\\wc-accuracy-output-haralick.csv") # WC doesn't provide feature names in its output CSV-file. Use source file src/textures/haralick/haralick.cpp instead
R_wc_int = pd.read_csv ("C:\\WORK\\AXLE\\paper2022\\accuracyHeatmap\\wc-accuracy-output-intensity.csv")
R_wc_shape = pd.read_csv ("C:\\WORK\\AXLE\\paper2022\\accuracyHeatmap\\wc-accuracy-output-morphology-FIXED.csv")
R_wc_misc_zernike = pd.read_csv ("C:\\WORK\\AXLE\\paper2022\\accuracyHeatmap\\wc-accuracy-output-zernike.csv")
R_wc_misc_gabor = pd.read_csv ("C:\\WORK\\AXLE\\paper2022\\accuracyHeatmap\\wc-accuracy-output-gabor.csv")
R_wc = pd.concat ([R_wc_haralick, R_wc_int, R_wc_shape, R_wc_misc_zernike, R_wc_misc_gabor], axis=1)   # Combined

# -- MITK is special: it can't produce output for all the feature groups, so its feature output is split to parts 
R_mitk_inten = pd.read_csv ("C:\\WORK\\AXLE\\paper2022\\accuracyHeatmap\\mitk_accuracy_fo-fon-foh.csv")
R_mitk_glcm = pd.read_csv ("C:\\WORK\\AXLE\\paper2022\\accuracyHeatmap\\mitk_accuracy_cooc2.csv")    
R_mitk_gldz = pd.read_csv ("C:\\WORK\\AXLE\\paper2022\\accuracyHeatmap\\mitk_accuracy_gldz.csv")
R_mitk_ngld = pd.read_csv ("C:\\WORK\\AXLE\\paper2022\\accuracyHeatmap\\mitk_accuracy_ngld.csv")
R_mitk_ngtd = pd.read_csv ("C:\\WORK\\AXLE\\paper2022\\accuracyHeatmap\\mitk_accuracy_ngtd.csv")
R_mitk_rl = pd.read_csv ("C:\\WORK\\AXLE\\paper2022\\accuracyHeatmap\\mitk_accuracy_rl.csv")
R_mitk_texture = pd.concat ([R_mitk_inten, R_mitk_glcm, R_mitk_gldz, R_mitk_ngld, R_mitk_ngtd, R_mitk_rl], axis=1)   # Combined

# Note: CP's Intensity_MassDisplacement_intensity is a member of morphology table
Fmap_intensity = np.array([
# Layout: 
    ["---", "---",  "---",  "---",  "---",  "---",  "---",  "---",  "---", "!image=banner_intensity.png"], # banner
#   [0]nyxus                            [1]cellprofiler                                 [2]imea     [3]matlab       [4]mitk         [5]nist                             [6]pyr                                      [7]radj                                                             [8]wc                               [9]         figure feature name
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    ["COV",                             "-cp",                                          "-imea",    "-matlab",      "First Order::Coefficient Of Variation",  "-nist",                            "-pyr",                                     "IntensityBasedStatistical_CoefficientOfVariation",                 "-wc",                              'CVAR'],    # Coef of var
    ["COVERED_IMAGE_INTENSITY_RANGE",   "-cp",                                          "-imea",    "-matlab",      "First Order::Covered Image Intensity Range",  "-nist",                            "-pyr",                                     "-radj",                                                            "-wc",                              'CIIR'],    # Covered img inten range
    ["EDGE_INTEGRATED_INTENSITY",       "Intensity_IntegratedIntensityEdge_intensity",  "-imea",    "-matlab",      "-mitk",        "-nist",                            "-pyr",                                     "-radj",                                                            "-wc",                              'IIE'],     # IIE
    ["EDGE_MAX_INTENSITY",              "Intensity_MaxIntensityEdge_intensity",         "-imea",    "-matlab",      "-mitk",        "-nist",                            "-pyr",                                     "-radj",                                                            "-wc",                              'EImax'],   # Edge intensity max   
    ["EDGE_MEAN_INTENSITY",             "Intensity_MeanIntensityEdge_intensity",        "-imea",    "-matlab",      "-mitk",        "-nist",                            "-pyr",                                     "-radj",                                                            "-wc",                              'EImean'],  # Edge intensity mean
    ["EDGE_MIN_INTENSITY",              "Intensity_MinIntensityEdge_intensity",         "-imea",    "-matlab",      "-mitk",        "-nist",                            "-pyr",                                     "-radj",                                                            "-wc",                              'EImin'],   # Edge intensity min
    ["EDGE_STDDEV_INTENSITY",           "Intensity_StdIntensityEdge_intensity",         "-imea",    "-matlab",      "-mitk",        "-nist",                            "-pyr",                                     "-radj",                                                            "-wc",                              'EIstd'],   # Edge intensity std
    ["ENERGY",                          "-cp",                                          "-imea",    "-matlab",      "First Order::Energy",  "-nist",                            "original_firstorder_Energy",               "IntensityBasedStatistical_Energy",                                 "original-energy",                  'ENER'],    # Energy
    ["ENTROPY",                         "-cp",                                          "-imea",    "entropy",      "First Order::Entropy",  "Feature2DJava_Entropy",            "original_firstorder_Entropy",              "-radj",                                                            "original-entropy",                 'entro'],   # Entropy
    ["EXCESS_KURTOSIS",                 "-cp",                                          "-imea",    "-matlab",      "First Order::Excess Kurtosis",   "-nist",                            "-pyr",                                     "-radj",                                                            "-wc",                              'kurt'],    # Excess kurtosis
    ["HYPERFLATNESS",                   "-cp",                                          "-imea",    "-matlab",      "-mitk",        "Feature2DJava_Hyperflatness",      "-pyr",                                     "-radj",                                                            "-wc",                              'hflat'],   # Hyperflatness
    ["HYPERSKEWNESS",                   "-cp",                                          "-imea",    "-matlab",      "-mitk",        "Feature2DJava_Hyperskewness",      "-pyr",                                     "-radj",                                                            "-wc",                              'hskew'],   # Hyperskewness
    ["INTEGRATED_INTENSITY",            "Intensity_IntegratedIntensity_intensity",      "-imea",    "-matlab",      "-mitk",        "-nist",                            "-pyr",                                     "-radj",                                                            "-wc",                              'II'],      # II
    ["-nyx",                            "-cp",                                          "-imea",    "-matlab",      "-mitk",        "-nist",                            "-pyr",                                     "-radj",                                                            "-wc",                              'Ihist'],   # Intensity features over histogram
    ["INTERQUARTILE_RANGE",             "-cp",                                          "-imea",    "IQR",          "First Order::Interquartile Range",   "-nist",                            "original_firstorder_InterquartileRange",   "IntensityBasedStatistical_Interquartile",                          "original-interquartile_range",     'IQR'],     # IQR
    ["KURTOSIS",                        "-cp",                                          "-imea",    "kurtosis",     "First Order::Kurtosis",   "Feature2DJava_Kurtosis",           "original_firstorder_Kurtosis",             "IntensityBasedStatistical_Kurtosis",                               "original-kurtosis",                'kurt'],    # Kurtosis
    ["MEAN_ABSOLUTE_DEVIATION",         "-cp",                                          "-imea",    "MAD",          "First Order::Mean Absolute Deviation",  "-nist",                            "original_firstorder_MeanAbsoluteDeviation",    "IntensityBasedStatistical_MeanAbsoluteDeviation",              "original-mean_absolute_deviation", 'MAD'],     # MAD
    ["MAX",                             "Intensity_MaxIntensity_intensity",             "-imea",    "max",          "First Order::Maximum",  "-nist",                            "original_firstorder_Maximum",              "IntensityBasedStatistical_Maximum",                                "original-max",                     'max'],     # Max
    ["-nyx",                            "-cp",                                          "-imea",    "-matlab",      "-mitk",        "-nist",                            "-pyr",                                     "-radj",                                                            "-wc",                              'MD'],      # MD
    ["MEAN",                            "Intensity_MeanIntensity_intensity",            "-imea",    "mean",         "First Order::Mean",  "Feature2DJava_Mean",               "original_firstorder_Mean",                 "IntensityBasedStatistical_Mean",                                   "original-mean",                    'mean'],    # Mean
    ["MEDIAN",                          "Intensity_MedianIntensity_intensity",          "-imea",    "median",       "First Order::Median",  "Feature2DJava_Median",             "original_firstorder_Median",               "IntensityBasedStatistical_Median",                                 "original-median",                  'med'],     # Median
    ["MEDIAN_ABSOLUTE_DEVIATION",       "Intensity_MADIntensity_intensity",             "-imea",    "-matlab",      "First Order::Mean Absolute Deviation",  "-nist",                            "-pyr",                                     "IntensityBasedStatistical_MedianAbsoluteDeviation",                "-wc",                              'med AD'],  # Median abs dev
    ["MIN",                             "Intensity_MinIntensity_intensity",             "-imea",    "min",          "First Order::Minimum",  "-nist",                            "original_firstorder_Minimum",              "IntensityBasedStatistical_Minimum",                                "original-min",                     'min'],     # Min
    ["-nyx",                            "-cp",                                          "-imea",    "-matlab",      "-mitk",  "-nist",                            "-pyr",                                     "-radj",                                                            "-wc",                              'minIE'],   # Min IE
    ["MODE",                            "-cp",                                          "-imea",    "mode",         "First Order::Mode",  "Feature2DJava_Mode",               "-pyr",                                     "-radj",                                                            "original-mode",                    'mode'],    # Mode
    ["-nyx",                            "-cp",                                          "-imea",    "-matlab",      "First Order::Mode Probability",  "-nist",                            "-pyr",                                     "-radj",                                                            "-wc",                              'modeP'],   # Mode probability
    ["P01",                             "-cp",                                          "-imea",    "P1",           "-mitk",  "-nist",                            "-pyr",                                     "-radj",                                                            "-wc",                              'p1'],      # Percentiles 1%
    ["P10",                             "-cp",                                          "-imea",    "P10",          "First Order::10th Percentile",  "-nist",                            "original_firstorder_10Percentile",         "IntensityBasedStatistical_Percentile10",                           "original-p10",                     'p10'],     # Percentiles 10%
    ["P25",                             "Intensity_LowerQuartileIntensity_intensity",   "-imea",    "P25",          "First Order::25th Percentile",  "-nist",                            "-pyr",                                     "-radj",                                                            "original-p25",                     'p25'],     # Percentiles 25
    ["P75",                             "Intensity_UpperQuartileIntensity_intensity",   "-imea",    "P75",          "First Order::75th Percentile",  "-nist",                            "-pyr",                                     "-radj",                                                            "original-p75",                     'p75'],     # Percentiles 75
    ["P90",                             "-cp",                                          "-imea",    "P90",          "First Order::90th Percentile",  "-nist",                            "original_firstorder_90Percentile",         "IntensityBasedStatistical_Percentile90",                           "original-p90",                     'p90'],     # Percentiles 90
    ["P99",                             "-cp",                                          "-imea",    "P99",          "-mitk",  "-nist",                            "-pyr",                                     "-radj",                                                            "-wc",                              'p99'],     # Percentiles 99%
    ["QCOD",                            "-cp",                                          "-imea",    "-matlab",      "First Order::Quantile Coefficient Of Dispersion",  "-nist",                            "-pyr",                                     "IntensityBasedStatistical_QuartileCoefficientOfDispersion",        "-wc",                              'QCoD'],    # Quantile coef of disp
    ["RANGE",                           "-cp",                                          "-imea",    "range",        "First Order::Range",  "-nist",                            "original_firstorder_Range",                "IntensityBasedStatistical_Range",                                  "original-range",                   'range'],   # Range
    ["ROBUST_MEAN_ABSOLUTE_DEVIATION",  "-cp",                                          "-imea",    "-matlab",      "First Order::Robust Mean Absolute Deviation",   "-nist",                            "original_firstorder_RobustMeanAbsoluteDeviation",   "IntensityBasedStatistical_RobustMeanAbsoluteDeviation",   "original-robust_mean_absolute_deviation",  'RMAD'],    # RMAD
    ["ROBUST_MEAN",                     "-cp",                                          "-imea",    "-matlab",      "First Order::Robust Mean",  "-nist",                            "-pyr",                                     "-radj",                                                            "-wc",                              'Rmean'],   # Rmean
    ["ROOT_MEAN_SQUARED",               "-cp",                                          "-imea",    "RMS",          "First Order::Root Mean Square",  "-nist",                            "original_firstorder_RootMeanSquared",      "IntensityBasedStatistical_RootMeanSquared",                        "original-root_mean_squared",       'RMS'],     # RMS
    ["STANDARD_ERROR",                  "-cp",                                          "-imea",    "stder",        "-mitk",        "-nist",                            "-pyr",                                     "IntensityBasedStatistical_StandardError",                          "-wc",                        'SE'],      # SE
    ["SKEWNESS",                        "-cp",                                          "-imea",    "skewness",     "First Order::Skewness",  "Feature2DJava_Skewness",           "original_firstorder_Skewness",             "IntensityBasedStatistical_Skewness",                               "original-skewness",                'skew'],    # Skewness
    ["STANDARD_DEVIATION",              "Intensity_StdIntensity_intensity",             "-imea",    "STD",          "First Order::Unbiased Standard deviation",  "Feature2DJava_StandardDeviation",  "-pyr",                                     "IntensityBasedStatistical_StandardDeviation",                      "original-standard_deviation",      'STD'],     # STD
    ["STANDARD_DEVIATION_BIASED",       "-cp",                                          "-imea",    "-matlab",      "First Order::Biased Standard deviation",  "-nist",                            "-pyr",                                     "-radj",                                                            "-wc",                              'STDB'],    # STD biased
    ["UNIFORMITY",                      "-cp",                                          "-imea",    "-matlab",      "First Order::Uniformity",  "-nist",                            "original_firstorder_Uniformity",           "-radj",                                                            "original-uniformity",              'uni'],     # Uniformity
    ["UNIFORMITY_PIU",                  "-cp",                                          "-imea",    "-matlab",      "-mitk",        "-nist",                            "-pyr",                                     "-radj",                                                            "-wc",                              'uniP'],    # Uniformity PIU
    ["VARIANCE",                        "-cp",                                          "-imea",    "var",          "First Order::Unbiased Variance",  "-nist",                            "original_firstorder_Variance",             "IntensityBasedStatistical_Variance",                               "-wc",                              'var'],     # Variance
    ["VARIANCE_BIASED",                 "-cp",                                          "-imea",    "-matlab",      "First Order::Biased Variance",  "-nist",                            "-pyr",                                     "-radj",                                                            "-wc",                        'varB']     # Variance (biased)
    ])

mitk_GLCM_JVAR_MEAN = "Co-occurenced Based Features::Mean Joint Variance"
mitk_GLCM_JE_MEAN = "Co-occurenced Based Features::Mean Joint Entropy"
mitk_GLCM_JMAX_MEAN = "Co-occurenced Based Features::Mean Joint Maximum"
mitk_GLCM_JAVE_MEAN = "Co-occurenced Based Features::Mean Joint Average"
mitk_GLCM_DIFAVE_AVE = "Co-occurenced Based Features::Mean Difference Average"
mitk_GLCM_DIFVAR_AVE = "Co-occurenced Based Features::Mean Difference Variance"
mitk_GLCM_DIFENTRO_AVE = "Co-occurenced Based Features::Mean Difference Entropy"
mitk_GLCM_SUMAVERAGE_AVE = "Co-occurenced Based Features::Mean Sum Average"
mitk_GLCM_SUMVARIANCE_AVE = "Co-occurenced Based Features::Mean Sum Variance"
mitk_GLCM_SUMENTROPY_AVE = "Co-occurenced Based Features::Mean Sum Entropy"
mitk_GLCM_ASM_AVE = "Co-occurenced Based Features::Mean Angular Second Moment"
mitk_GLCM_CONTRAST_AVE = "Co-occurenced Based Features::Mean Contrast"
mitk_GLCM_DIS_AVE = "Co-occurenced Based Features::Mean Dissimilarity"
mitk_GLCM_ID_AVE = "Co-occurenced Based Features::Mean Inverse Difference"
mitk_GLCM_IDN_AVE = "Co-occurenced Based Features::Mean Inverse Difference Normalized"
mitk_GLCM_IDM_AVE = "Co-occurenced Based Features::Mean Inverse Difference Moment"
mitk_GLCM_IDMN_AVE = "Co-occurenced Based Features::Mean Inverse Difference Moment Normalized"
mitk_GLCM_IV_AVE = "Co-occurenced Based Features::Mean Inverse Variance"
mitk_GLCM_CORRELATION_AVE = "Co-occurenced Based Features::Mean Correlation"
mitk_GLCM_ACOR_AVE = "Co-occurenced Based Features::Mean Autocorrelation"
mitk_GLCM_CLUTEND_AVE = "Co-occurenced Based Features::Mean Cluster Tendency"
mitk_GLCM_CLUSHADE_AVE = "Co-occurenced Based Features::Mean Cluster Shade"
mitk_GLCM_CLUPROM_AVE = "Co-occurenced Based Features::Mean Cluster Prominence"
mitk_GLCM_INFOMEAS1_AVE = "Co-occurenced Based Features::Mean First Measure of Information Correlation"
mitk_GLCM_INFOMEAS2_AVE = "Co-occurenced Based Features::Mean Second Measure of Information Correlation"
mitk_GLCM_ROW_MAX_MEAN = "Co-occurenced Based Features::Mean Row Maximum"
mitk_GLCM_ROW_AVE_MEAN = "Co-occurenced Based Features::Mean Row Average"
mitk_GLCM_ROW_VAR_MEAN = "Co-occurenced Based Features::Mean Row Variance"
mitk_GLCM_ROW_ENTRO_MEAN = "Co-occurenced Based Features::Mean Row Entropy"
mitk_GLCM_ROWCOL_ENTRO1_MEAN = "Co-occurenced Based Features::Mean First Row-Column Entropy"
mitk_GLCM_ROWCOL_ENTRO2_MEAN = "Co-occurenced Based Features::Mean Second Row-Column Entropy"

mitk_GLRLM_SRE_AVE = "Run Length::Short run emphasis Means"
mitk_GLRLM_LRE_AVE = "Run Length::Long run emphasis Means"
mitk_GLRLM_GLN_AVE = "Run Length::Grey level nonuniformity Means"
mitk_GLRLM_GLNN_AVE = "Run Length::Grey level nonuniformity normalized Means"
mitk_GLRLM_RLN_AVE = "Run Length::Run length nonuniformity Means"
mitk_GLRLM_RLNN_AVE = "Run Length::Run length nonuniformity normalized Means"
mitk_GLRLM_LGLRE_AVE="Run Length::Low grey level run emphasis Means"
mitk_GLRLM_HGLRE_AVE="Run Length::High grey level run emphasis Means"
mitk_GLRLM_SRLGLE_AVE="Run Length::Short run low grey level emphasis Means"
mitk_GLRLM_SRHGLE_AVE="Run Length::Short run high grey level emphasis Means"
mitk_GLRLM_LRLGLE_AVE="Run Length::Long run low grey level emphasis Means"
mitk_GLRLM_LRHGLE_AVE="Run Length::Long run high grey level emphasis Means"
mitk_GLRLM_RP_AVE="Run Length::Run percentage Means"
mitk_GLRLM_GLV_AVE="Run Length::Grey level variance Means"
mitk_GLRLM_RV_AVE="Run Length::Run length variance Means"
mitk_GLRLM_RE_AVE="Run Length::Run length entropy Means"

Fmap_texture = np.array([
#   [0]nyxus                [1]cellprofiler                                         [2]imea     [3]matlab               [4]mitk                         [5]nist                                 [6]pyr                              [7]radj                                         [8]wc                       [9] figure feature name
    ["---", "---",  "---",  "---",  "---",  "---",  "---",  "---",  "---", "!image=banner_texture.png"], # banner
    # GLCM:
    ["---", "---",  "---",  "---",  "---",  "---",  "---",  "---",  "---", "!text=$\\blacktriangledown$GLCM"], # banner
    ["GLCM_ASM_0",		    "Texture_AngularSecondMoment_intensity_3_00_256",       "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",		                        "-radj",                                        "-wc",	                    "ASM 0"],	# Angular second moment, IBSI # 8ZQL (PyRad: Joint Energy)
    ["GLCM_ASM_45",		    "Texture_AngularSecondMoment_intensity_3_01_256",       "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",		                        "-radj",                                        "-wc",	                    "ASM 45"],	# Angular second moment, IBSI # 8ZQL (PyRad: Joint Energy)
    ["GLCM_ASM_90",	    	"Texture_AngularSecondMoment_intensity_3_02_256",       "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",		                        "-radj",                                        "-wc",	                    "ASM 90"],	# Angular second moment, IBSI # 8ZQL (PyRad: Joint Energy)
    ["GLCM_ASM_135",	    "Texture_AngularSecondMoment_intensity_3_03_256",       "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",		                        "-radj",                                        "-wc",	                    "ASM 135"],	# Angular second moment, IBSI # 8ZQL (PyRad: Joint Energy)
    ["GLCM_ASM_AVE",	    "-cp",                                                  "-imea",    "-matlab",              mitk_GLCM_ASM_AVE,              "-nist",                                "original_glcm_JointEnergy",		"GLCM_AngularSecondMoment",                     "HaralickTextures()[0]",    "E|ASM"],	# Angular second moment, IBSI # 8ZQL (PyRad: Joint Energy) ---Quirks---> "$\\overline{ASM}$"
    ["GLCM_ACOR_0",		    "-cp",                                                  "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",	                            "-radj",                                        "-wc",	                    "AC 0"],     # Autocorrelation, IBSI # QWB0
    ["GLCM_ACOR_AVE",		"-cp",                                                  "-imea",    "-matlab",              mitk_GLCM_ACOR_AVE,             "-nist",                                "original_glcm_Autocorrelation",	"GLCM_Autocorrection",                          "-wc",	                    "E|AC"],     # Autocorrelation, IBSI # QWB0

    ["GLCM_CLUPROM_0",	    "-cp",                                                  "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",	                            "-radj",                                        "-wc",	                    "CP 0"],		# Cluster prominence, IBSI # AE86
    ["GLCM_CLUPROM_AVE",	"-cp",                                                  "-imea",    "-matlab",              mitk_GLCM_CLUPROM_AVE,          "-nist",                                "original_glcm_ClusterProminence",	"GLCM_ClusterProminence",                       "-wc",	                    "E|CP"],		# Cluster prominence, IBSI # AE86

    ["GLCM_CLUSHADE_0", 	"-cp",                                                  "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",		                        "-radj",                                        "-wc",	                    "CS 0"],		# Cluster shade, IBSI # 7NFM
    ["GLCM_CLUSHADE_AVE",	"-cp",                                                  "-imea",    "-matlab",              mitk_GLCM_CLUSHADE_AVE,         "-nist",                                "original_glcm_ClusterShade",		"GLCM_ClusterShade",                            "-wc",	                    "E|CS"],		# Cluster shade, IBSI # 7NFM

    ["GLCM_CLUTEND_AVE",	"-cp",                                                  "-imea",    "-matlab",              mitk_GLCM_CLUTEND_AVE,          "-nist",                                "original_glcm_ClusterTendency",	"GLCM_ClusterTendency",                         "-wc",	                    "E|CT"],		# Cluster tendency, IBSI # DG8W
   
    ["GLCM_CONTRAST_0",		"Texture_Contrast_intensity_3_00_256",                  "-imea",    "-matlab",       "-mitk",                        "-nist",                                "-pyr",			                    "-radj",                                        "-wc",	                    "CON 0"],	# Contrast, IBSI # ACUI
    ["mockmatlab_"+"GLCM_CONTRAST_0",		"-cp",      "-imea",    "GlcmContrast_0",       "-mitk",                        "-nist",                                "-pyr",			                    "-radj",                                        "-wc",	                    "CON 0/matl"],	# Contrast, IBSI # ACUI
    ["GLCM_CONTRAST_45",	"Texture_Contrast_intensity_3_01_256",                  "-imea",    "-matlab",       "-mitk",                       "-nist",                                "-pyr",			                    "-radj",                                        "-wc",	                    "CON 45"],	# Contrast, IBSI # ACUI
    ["mockmatlab_"+"GLCM_CONTRAST_45",	"-cp",          "-imea",    "GlcmContrast_45",       "-mitk",                       "-nist",                                "-pyr",			                    "-radj",                                        "-wc",	                    "CON 45/matl"],	# Contrast, IBSI # ACUI
    ["GLCM_CONTRAST_90",	"Texture_Contrast_intensity_3_02_256",                  "-imea",    "-matlab",       "-mitk",                       "-nist",                                "-pyr",			                    "-radj",                                        "-wc",	                    "CON 90"],	# Contrast, IBSI # ACUI
    ["mockmatlab_"+"GLCM_CONTRAST_90",	"-cp",          "-imea",    "GlcmContrast_90",       "-mitk",                       "-nist",                                "-pyr",			                    "-radj",                                        "-wc",	                    "CON 90/matl"],	# Contrast, IBSI # ACUI
    ["GLCM_CONTRAST_135",	"Texture_Contrast_intensity_3_03_256",                  "-imea",    "-matlab",       "-mitk",                      "-nist",                                "-pyr",			                    "-radj",                                        "-wc",	                    "CON 135"],	# Contrast, IBSI # ACUI
    ["mockmatlab_"+"GLCM_CONTRAST_135",	"-cp",      "-imea",    "GlcmContrast_135",       "-mitk",                      "-nist",                                "-pyr",			                    "-radj",                                        "-wc",	                    "CON 135/matl"],	# Contrast, IBSI # ACUI
    ["GLCM_CONTRAST_AVE",	"-cp",                                                  "-imea",    "-matlab",              mitk_GLCM_CONTRAST_AVE,         "Feature2DJava_TContrast_Average",      "original_glcm_Contrast",			"GLCM_Contrast",                                "HaralickTextures()[1]",	"E|CON"],	# Contrast, IBSI # ACUI

    ["GLCM_CORRELATION_0",		"Texture_Correlation_intensity_3_00_256",           "-imea",    "-matlab",    "-mitk",                        "-nist",                                "-pyr",	                            "-radj",                                        "-wc",	                    "COR 0"],	# Correlation, IBSI # NI2N
    ["mockmatlab_"+"GLCM_CORRELATION_0",  "-cp",    "-imea",    "GlcmCorrelation_0",    "-mitk",                        "-nist",                                "-pyr",	                            "-radj",                                        "-wc",	                    "COR 0/matl"],	# Correlation, IBSI # NI2N
    ["GLCM_CORRELATION_45",		"Texture_Correlation_intensity_3_01_256",           "-imea",    "-matlab",   "-mitk",                        "-nist",                                "-pyr",	                            "-radj",                                        "-wc",	                    "COR 45"],	# Correlation, IBSI # NI2N
    ["mockmatlab_"+"GLCM_CORRELATION_45",    "-cp", "-imea",    "GlcmCorrelation_45",   "-mitk",                        "-nist",                                "-pyr",	                            "-radj",                                        "-wc",	                    "COR 45/matl"],	# Correlation, IBSI # NI2N
    ["GLCM_CORRELATION_90",		"Texture_Correlation_intensity_3_02_256",           "-imea",    "-matlab",   "-mitk",                        "-nist",                                "-pyr",	                            "-radj",                                        "-wc",	                    "COR 90"],	# Correlation, IBSI # NI2N
    ["mockmatlab_"+"GLCM_CORRELATION_90",  "-cp",   "-imea",    "GlcmCorrelation_90",   "-mitk",                        "-nist",                                "-pyr",	                            "-radj",                                        "-wc",	                    "COR 90/matl"],	# Correlation, IBSI # NI2N
    ["GLCM_CORRELATION_135",	"Texture_Correlation_intensity_3_03_256",           "-imea",    "-matlab",  "-mitk",                        "-nist",                                "-pyr",	                            "-radj",                                        "-wc",	                    "COR 135"],	# Correlation, IBSI # NI2N
    ["mockmatlab_"+"GLCM_CORRELATION_135",	"-cp",   "-imea",    "GlcmCorrelation_135",  "-mitk",                        "-nist",                                "-pyr",	                            "-radj",                                        "-wc",	                    "COR 135/matl"],	# Correlation, IBSI # NI2N
    ["GLCM_CORRELATION_AVE",	"-cp",                                              "-imea",    "-matlab",              mitk_GLCM_CORRELATION_AVE,      "Feature2DJava_TCorrelation_Average",   "original_glcm_Correlation",	    "GLCM_Correlation",                             "HaralickTextures()[2]",	"E|COR"],	# Correlation, IBSI # NI2N

    ["GLCM_DIFAVE_0",		"-cp",                                                  "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",	                            "-radj",                                        "-wc",	                    "DA 0"],		# Difference average, IBSI # TF7R
    ["GLCM_DIFAVE_AVE",		"-cp",                                                  "-imea",    "-matlab",              mitk_GLCM_DIFAVE_AVE,           "Feature2DJava_TDiffAverage_Average",   "original_glcm_DifferenceAverage",	"GLCM_DifferenceAverage",                       "-wc",	                    "E|DA"],		# Difference average, IBSI # TF7R
    
    ["GLCM_DIFENTRO_0",		"Texture_DifferenceEntropy_intensity_3_00_256",         "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",	                            "-radj",                                        "-wc",	                    "DE 0"],		# Difference entropy, IBSI # NTRS
    ["GLCM_DIFENTRO_45",	"Texture_DifferenceEntropy_intensity_3_01_256",         "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",	                            "-radj",                                        "-wc",	                    "DE 45"],		# Difference entropy, IBSI # NTRS
    ["GLCM_DIFENTRO_90",	"Texture_DifferenceEntropy_intensity_3_02_256",         "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",	                            "-radj",                                        "-wc",	                    "DE 90"],		# Difference entropy, IBSI # NTRS
    ["GLCM_DIFENTRO_135",	"Texture_DifferenceEntropy_intensity_3_03_256",         "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",	                            "-radj",                                        "-wc",	                    "DE 135"],		# Difference entropy, IBSI # NTRS
    ["GLCM_DIFENTRO_AVE",	"-cp",                                                  "-imea",    "-matlab",              mitk_GLCM_DIFENTRO_AVE,         "Feature2DJava_TDiffEntropy_Average",   "original_glcm_DifferenceEntropy",	"GLCM_DifferenceEntropy",                       "HaralickTextures()[10]",   "E|DE"],		# Difference entropy, IBSI # NTRS

    ["GLCM_DIFVAR_0",		"Texture_DifferenceVariance_intensity_3_00_256",        "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",	                            "-radj",                                        "-wc",	                    "DV 0"],		# Difference variance, IBSI # D3YU
    ["GLCM_DIFVAR_45",		"Texture_DifferenceVariance_intensity_3_01_256",        "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",	                            "-radj",                                        "-wc",	                    "DV 45"],		# Difference variance, IBSI # D3YU
    ["GLCM_DIFVAR_90",		"Texture_DifferenceVariance_intensity_3_02_256",        "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",	                            "-radj",                                        "-wc",	                    "DV 90"],		# Difference variance, IBSI # D3YU
    ["GLCM_DIFVAR_135",		"Texture_DifferenceVariance_intensity_3_03_256",        "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",                             "-radj",                                        "-wc",	                    "DV 135"],		# Difference variance, IBSI # D3YU
    ["GLCM_DIFVAR_AVE",		"-cp",                                                  "-imea",    "-matlab",              mitk_GLCM_DIFVAR_AVE,           "Feature2DJava_TDiffVariance_Average",  "original_glcm_DifferenceVariance",	"GLCM_DifferenceVariance",                      "HaralickTextures()[9]",	"E|DV"],		# Difference variance, IBSI # D3YU
    
    ["GLCM_DIS_0",		    "-cp",                                                  "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",		                        "-radj",                                        "-wc",	                    "DIS 0"],	# Dissimilarity, IBSI # 8S9J
    ["GLCM_DIS_AVE",	    "-cp",                                                  "-imea",    "-matlab",              mitk_GLCM_DIS_AVE,              "-nist",                                "-pyr",		                        "GLCM_Dissimilarity",                           "-wc",	                    "E|DIS"],	# mean Dissimilarity, IBSI # 8S9J
    
    ["GLCM_ENERGY_0",		"-cp",                                                  "-imea",    "-matlab",         "-mitk",                        "-nist",                                "-pyr",								"-radj",                                        "-wc",	                    "E 0"],	    # Energy
    ["mockmatlab_"+"GLCM_ENERGY_0",		"-cp",                                      "-imea",    "GlcmEnergy_0",         "-mitk",                        "-nist",                                "-pyr",								"-radj",                                        "-wc",	                    "E 0/matl"],	    # Energy
    ["GLCM_ENERGY_45",		"-cp",                                                  "-imea",    "-matlab",        "-mitk",                        "-nist",                                "-pyr",								"-radj",                                        "-wc",	                    "E 45"],	# Energy
    ["mockmatlab_"+"GLCM_ENERGY_45",		"-cp",                                      "-imea",    "GlcmEnergy_45",        "-mitk",                        "-nist",                                "-pyr",								"-radj",                                        "-wc",	                    "E 45/matl"],	# Energy
    ["GLCM_ENERGY_90",		"-cp",                                                  "-imea",    "-matlab",        "-mitk",                        "-nist",                                "-pyr",								"-radj",                                        "-wc",	                    "E 90"],	# Energy
    ["mockmatlab_"+"GLCM_ENERGY_90",		"-cp",                                      "-imea",    "GlcmEnergy_90",        "-mitk",                        "-nist",                                "-pyr",								"-radj",                                        "-wc",	                    "E 90/matl"],	# Energy
    ["GLCM_ENERGY_135",		"-cp",                                                  "-imea",    "-matlab",       "-mitk",                        "-nist",                                "-pyr",								"-radj",                                        "-wc",	                    "E 135"],	# Energy
    ["mockmatlab_"+"GLCM_ENERGY_135",		"-cp",                                      "-imea",    "GlcmEnergy_135",       "-mitk",                        "-nist",                                "-pyr",								"-radj",                                        "-wc",	                    "E 135/matl"],	# Energy
    ["GLCM_ENERGY_AVE",		"-cp",                                                  "-imea",    "-matlab",              "-mitk",                        "Feature2DJava_TEnergy_Average",        "-pyr",								"-radj",                                        "-wc",	                    "E|E"],	    # Energy
    
    ["GLCM_ENTROPY_0",	    "Texture_Entropy_intensity_3_00_256",                   "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",								"-radj",                                        "-wc",	                    "ENT 0"],	# Entropy
    ["GLCM_ENTROPY_45",	    "Texture_Entropy_intensity_3_01_256",                   "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",								"-radj",                                        "-wc",	                    "ENT 45"],	# Entropy
    ["GLCM_ENTROPY_90",	    "Texture_Entropy_intensity_3_02_256",                   "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",								"-radj",                                        "-wc",	                    "ENT 90"],	# Entropy
    ["GLCM_ENTROPY_135",	"Texture_Entropy_intensity_3_03_256",                   "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",								"-radj",                                        "HaralickTextures()[8]",	"ENT 135"],	# Entropy
    ["GLCM_ENTROPY_AVE",	"-cp",                                                  "-imea",    "-matlab",              "-mitk",                        "Feature2DJava_TEntropy_Average",       "-pyr",								"-radj",                                        "-wc",	                    "E|ENT"],	# Entropy
    
    ["GLCM_HOM1_0",			"-cp",                                                  "-imea",    "-matlab",    "-mitk",                        "-nist",                                "-pyr",								"-radj",                                        "-wc",	                    "H1 0"],		# Homogeneity-1 (PyR)
    ["mockmatlab_"+"GLCM_HOM1_0",			"-cp",                                      "-imea",    "GlcmHomogeneity_0",    "-mitk",                        "-nist",                                "-pyr",								"-radj",                                        "-wc",	                    "H1 0/matl"],		# Homogeneity-1 (PyR)
    ["GLCM_HOM1_45",		"-cp",                                                  "-imea",    "-matlab",   "-mitk",                        "-nist",                                "-pyr",								"-radj",                                        "-wc",	                    "H1 45"],		# Homogeneity-1 (PyR)
    ["mockmatlab_"+"GLCM_HOM1_45",		"-cp",                                          "-imea",    "GlcmHomogeneity_45",   "-mitk",                        "-nist",                                "-pyr",								"-radj",                                        "-wc",	                    "H1 45/matl"],		# Homogeneity-1 (PyR)
    ["GLCM_HOM1_90",		"-cp",                                                  "-imea",    "-matlab",   "-mitk",                        "-nist",                                "-pyr",								"-radj",                                        "-wc",	                    "H1 90"],		# Homogeneity-1 (PyR)
    ["mockmatlab_"+"GLCM_HOM1_90",		"-cp",                                          "-imea",    "GlcmHomogeneity_90",   "-mitk",                        "-nist",                                "-pyr",								"-radj",                                        "-wc",	                    "H1 90/matl"],		# Homogeneity-1 (PyR)
    ["GLCM_HOM1_135",		"-cp",                                                  "-imea",    "-matlab",  "-mitk",                        "-nist",                                "-pyr",								"-radj",                                        "-wc",	                    "H1 135"],		# Homogeneity-1 (PyR)
    ["mockmatlab_"+"GLCM_HOM1_135",		"-cp",                                      "-imea",    "GlcmHomogeneity_135",  "-mitk",                        "-nist",                                "-pyr",								"-radj",                                        "-wc",	                    "H1 135/matl"],		# Homogeneity-1 (PyR)
    ["GLCM_HOM1_AVE",		"-cp",                                                  "-imea",    "-matlab",				"-mitk",                        "Feature2DJava_THomogeneity_Average",   "-pyr",	                            "-radj",                                        "-wc",	                    "E|H1"],		# Homogeneity-1 (PyR)
    
    ["GLCM_HOM2_0",		    "-cp",                                                  "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",								"-radj",                                        "-wc",	                    "H2 0"],		# Homogeneity-2 (PyR)
    
    ["-GLCM_ID_0",			"-cp",                                                  "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",					            "-radj",                                        "-wc",	                    "ID 0"],		# Inv diff, IBSI # IB1Z
    ["GLCM_ID_AVE",			"-cp",                                                  "-imea",    "-matlab",              mitk_GLCM_ID_AVE,               "-nist",                                "original_glcm_Id",					"GLCM_InverseDifference",                       "-wc",	                    "E|ID"],		# Inv diff, IBSI # IB1Z
    
    ["GLCM_IDN_0",		    "-cp",                                                  "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",				                "-radj",                                        "-wc",	                    "IDN 0"],	# Inv diff normalized, IBSI # NDRX
    ["GLCM_IDN_AVE",		"-cp",                                                  "-imea",    "-matlab",              mitk_GLCM_IDN_AVE,              "-nist",                                "original_glcm_Idn",				"GLCM_NormalizedInverseDifference",             "-wc",	                    "E|IDN"],	# Inv diff normalized, IBSI # NDRX
    
    ["GLCM_IDM_0",		    "Texture_InverseDifferenceMoment_intensity_3_00_256",   "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",				                "-radj",                                        "-wc",	                    "IDM 0"],	# Inv diff mom, IBSI # WF0Z
    ["GLCM_IDM_45",		    "Texture_InverseDifferenceMoment_intensity_3_01_256",   "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",				                "-radj",                                        "-wc",	                    "IDM 45"],	# Inv diff mom, IBSI # WF0Z
    ["GLCM_IDM_90",		    "Texture_InverseDifferenceMoment_intensity_3_02_256",   "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",				                "-radj",                                        "-wc",	                    "IDM 90"],	# Inv diff mom, IBSI # WF0Z
    ["GLCM_IDM_135",	    "Texture_InverseDifferenceMoment_intensity_3_03_256",   "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",				                "-radj",                                        "-wc",	                    "IDM 135"],	# Inv diff mom, IBSI # WF0Z
    ["GLCM_IDM_AVE",	    "-cp",                                                  "-imea",    "-matlab",              mitk_GLCM_IDM_AVE,              "Feature2DJava_TInvDiffMoment_Average", "original_glcm_Idm",				"GLCM_InverseDifferenceMoment",                 "HaralickTextures()[4]",	"E|IDM"],	# Inv diff mom, IBSI # WF0Z
    
    ["GLCM_IDMN_0",		    "-cp",                                                  "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",				                "-radj",                                        "-wc",	                    "IDMN 0"],	# Inv diff mom normalized, IBSI # 1QCO
    ["GLCM_IDMN_AVE",		"-cp",                                                  "-imea",    "-matlab",              mitk_GLCM_IDMN_AVE,             "-nist",                                "original_glcm_Idmn",				"GLCM_NormalizedInverseDifferenceMoment",       "-wc",	                    "IDMN"],	# Inv diff mom normalized, IBSI # 1QCO
    
    ["GLCM_INFOMEAS1_0",	"Texture_InfoMeas1_intensity_3_00_256",                 "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",				                "-radj",                                        "-wc",	                    "IM1 0"],	# Information measure of correlation 1, IBSI # R8DG
    ["GLCM_INFOMEAS1_45",	"Texture_InfoMeas1_intensity_3_01_256",                 "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",				                "-radj",                                        "-wc",	                    "IM1 45"],	# Information measure of correlation 1, IBSI # R8DG
    ["GLCM_INFOMEAS1_90",	"Texture_InfoMeas1_intensity_3_02_256",                 "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",				                "-radj",                                        "-wc",	                    "IM1 90"],	# Information measure of correlation 1, IBSI # R8DG
    ["GLCM_INFOMEAS1_135",	"Texture_InfoMeas1_intensity_3_03_256",                 "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",				                "-radj",                                        "-wc",	                    "IM1 135"],	# Information measure of correlation 1, IBSI # R8DG
    ["GLCM_INFOMEAS1_AVE",	"-cp",                                                  "-imea",    "-matlab",              mitk_GLCM_INFOMEAS1_AVE,        "-nist",                                "original_glcm_Imc1",				"GLCM_InformationalMeasureOfCorrelation1",      "HaralickTextures()[11]",	"E|IM1"],	# Information measure of correlation 1, IBSI # R8DG
    
    ["GLCM_INFOMEAS2_0",	"Texture_InfoMeas2_intensity_3_00_256",                 "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",				                "-radj",                                        "-wc",	                    "IM2 0"],	# Information measure of correlation 2, IBSI # JN9H
    ["GLCM_INFOMEAS2_45",	"Texture_InfoMeas2_intensity_3_01_256",                 "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",				                "-radj",                                        "-wc",	                    "IM2 45"],	# Information measure of correlation 2, IBSI # JN9H
    ["GLCM_INFOMEAS2_90",	"Texture_InfoMeas2_intensity_3_02_256",                 "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",				                "-radj",                                        "-wc",	                    "IM2 90"],	# Information measure of correlation 2, IBSI # JN9H
    ["GLCM_INFOMEAS2_135",	"Texture_InfoMeas2_intensity_3_03_256",                 "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",				                "-radj",                                        "-wc",	                    "IM2 135"],	# Information measure of correlation 2, IBSI # JN9H
    ["GLCM_INFOMEAS2_AVE",  "-cp",                                                  "-imea",    "-matlab",              mitk_GLCM_INFOMEAS2_AVE,        "-nist",                                "original_glcm_Imc2",				"GLCM_InformationalMeasureOfCorrelation2",      "HaralickTextures()[12]",	"E|IM2"],	# Information measure of correlation 2, IBSI # JN9H
    
    ["GLCM_IV_0",			"-cp",                                                  "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",	                            "-radj",                                        "-wc",	                    "IV 0"],		# Inv variance, IBSI # E8JP
    ["GLCM_IV_AVE",			"-cp",                                                  "-imea",    "-matlab",              mitk_GLCM_IV_AVE,               "-nist",                                "original_glcm_InverseVariance",	"GLCM_InverseVariance",                         "-wc",	                    "E|IV"],		# Inv variance, IBSI # E8JP
    
    ["GLCM_JAVE_0",		    "-cp",                                                  "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",		                        "-radj",                                        "-wc",	                    "JA 0"],		# Joint average, IBSI # 60VM
    ["GLCM_JAVE_AVE",		"-cp",                                                  "-imea",    "-matlab",              mitk_GLCM_JAVE_MEAN,            "-nist",                                "original_glcm_JointAverage",		"GLCM_JointAverage",                            "-wc",	                    "E|JA"],		# mean of Joint average, IBSI # 60VM
    
    ["-nyx",			    "-cp",                                                  "-imea",    "-matlab",              "-mitk",                        "-nist",                                "original_glcm_JointEnergy",		"-radj",                                        "-wc",	                    "JENE"],	# Joint energy
    
    ["GLCM_JE_0",			"-cp",                                                  "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",		                        "-radj",                                        "-wc",	                    "JE 0"],		# Joint entropy, IBSI # TU9B
    ["GLCM_JE_AVE",			"-cp",                                                  "-imea",    "-matlab",              mitk_GLCM_JE_MEAN,              "-nist",                                "original_glcm_JointEntropy",		"GLCM_JointEntropy",                            "-wc",	                    "E|JE"],		# Joint entropy, IBSI # TU9B
    
    ["GLCM_JMAX_0",		    "-cp",                                                  "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",	                            "-radj",                                        "-wc",	                    "JM 0"],		# Joint max (aka PyR max probability), IBSI # GYBY
    ["GLCM_JMAX_AVE",		"-cp",                                                  "-imea",    "-matlab",              mitk_GLCM_JMAX_MEAN,            "-nist",                                "original_glcm_MaximumProbability",	"GLCM_JointMaximum",                            "-wc",	                    "E|JM"],		# mean of Joint max (aka PyR max probability), IBSI # GYBY
    
    ["GLCM_JVAR_0",		    "-cp",                                                  "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",								"-radj",                                        "-wc",	                    "JV 0"],		# Joint var (aka PyR Sum of Squares), IBSI # UR99
    ["GLCM_JVAR_AVE",		"-cp",                                                  "-imea",    "-matlab",              mitk_GLCM_JVAR_MEAN,            "-nist",                                "-pyr",								"GLCM_JointVariance",                           "-wc",	                    "E|JV"],		# mean of Joint var (aka PyR Sum of Squares), IBSI # UR99
    
    ["-nyx",    	        "-cp",                                                  "-imea",    "-matlab",              "-mitk",                        "-nist",                                "original_glcm_MCC",				"-radj",                                        "HaralickTextures()[13]",	"MCC"],	# Max correlation coefficient
    
    ["GLCM_SUMAVERAGE_0",	"Texture_SumAverage_intensity_3_00_256",                "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",			                    "-radj",                                        "-wc",	                    "SUMA 0"],	# Sum average, IBSI # ZGXS
    ["GLCM_SUMAVERAGE_45",	"Texture_SumAverage_intensity_3_01_256",                "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",			                    "-radj",                                        "-wc",	                    "SUMA 45"],	# Sum average, IBSI # ZGXS
    ["GLCM_SUMAVERAGE_90",	"Texture_SumAverage_intensity_3_02_256",                "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",			                    "-radj",                                        "-wc",	                    "SUMA 90"],	# Sum average, IBSI # ZGXS
    ["GLCM_SUMAVERAGE_135",	"Texture_SumAverage_intensity_3_03_256",                "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",			                    "-radj",                                        "-wc",	                    "SUMA 135"],	# Sum average, IBSI # ZGXS
    ["GLCM_SUMAVERAGE_AVE",	"-cp",                                                  "-imea",    "-matlab",              mitk_GLCM_SUMAVERAGE_AVE,       "Feature2DJava_TSumAverage_Average",    "original_glcm_SumAverage",			                    "GLCM_SumAverage",                              "HaralickTextures()[5]",	"E|SUMA"],	# Sum average, IBSI # ZGXS
    
    ["GLCM_SUMENTROPY_0",	"Texture_SumEntropy_intensity_3_00_256",                "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",			                    "-radj",                                        "-wc",	                    "SUME 0"],	# Sum entropy, IBSI # P6QZ
    ["GLCM_SUMENTROPY_45",	"Texture_SumEntropy_intensity_3_01_256",                "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",			                    "-radj",                                        "-wc",	                    "SUME 45"],	# Sum entropy, IBSI # P6QZ
    ["GLCM_SUMENTROPY_90",	"Texture_SumEntropy_intensity_3_02_256",                "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",			                    "-radj",                                        "-wc",	                    "SUME 90"],	# Sum entropy, IBSI # P6QZ
    ["GLCM_SUMENTROPY_135",	"Texture_SumEntropy_intensity_3_03_256",                "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",			                    "-radj",                                        "-wc",	                    "SUME 135"],	# Sum entropy, IBSI # P6QZ
    ["GLCM_SUMENTROPY_AVE",	"-cp",                                                  "-imea",    "-matlab",              mitk_GLCM_SUMENTROPY_AVE,       "Feature2DJava_TSumEntropy_Average",    "original_glcm_SumEntropy",			                    "GLCM_SumEntropy",                              "HaralickTextures()[7]",	"E|SUME "],	# Sum entropy, IBSI # P6QZ
    
    ["GLCM_SUMVARIANCE_0",	"Texture_SumVariance_intensity_3_00_256",               "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",                             "-radj",                                        "-wc",	                    "SUMV 0"],     	
    ["GLCM_SUMVARIANCE_45",	"Texture_SumVariance_intensity_3_01_256",               "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",                             "-radj",                                        "-wc",	                    "SUMV 45"],     	
    ["GLCM_SUMVARIANCE_90",	"Texture_SumVariance_intensity_3_02_256",               "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",                             "-radj",                                        "-wc",	                    "SUMV 90"],     	
    ["GLCM_SUMVARIANCE_135",	"Texture_SumVariance_intensity_3_03_256",           "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",                             "-radj",                                        "-wc",	                    "SUMV 135"],     	
    ["GLCM_SUMVARIANCE_AVE",	"-cp",                                              "-imea",    "-matlab",              mitk_GLCM_SUMVARIANCE_AVE,      "Feature2DJava_TSumVariance_Average",   "-pyr",                             "GLCM_SumVariance",                             "HaralickTextures()[6]",	"E|SUMV"],     	
    
    ["GLCM_VARIANCE_0",	    "Texture_Variance_intensity_3_00_256",                  "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",			                    "-radj",                                        "-wc",	                    "VAR 0"],     # Sum variance, IBSI # OEEB (PyRad: sum of squares)
    ["GLCM_VARIANCE_45",	"Texture_Variance_intensity_3_01_256",                  "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",			                    "-radj",                                        "-wc",	                    "VAR 45"],     # Sum variance, IBSI # OEEB (PyRad: sum of squares)
    ["GLCM_VARIANCE_90",	"Texture_Variance_intensity_3_02_256",                  "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",			                    "-radj",                                        "-wc",	                    "VAR 90"],     # Sum variance, IBSI # OEEB (PyRad: sum of squares)
    ["GLCM_VARIANCE_135",	"Texture_Variance_intensity_3_03_256",                  "-imea",    "-matlab",              "-mitk",                        "-nist",                                "-pyr",			                    "-radj",                                        "-wc",	                    "VAR 135"],     # Sum variance, IBSI # OEEB (PyRad: sum of squares)
    ["GLCM_VARIANCE_AVE",	"-cp",                                                  "-imea",    "-matlab",              "-mitk",                        "Feature2DJava_TVariance_Average",      "original_glcm_SumSquares",			                    "-radj",                                        "HaralickTextures()[3]",	"E|VAR"],     # Sum variance, IBSI # OEEB (PyRad: sum of squares)
    ["-nyx",	            "-cp",                                                  "-imea",    "-matlab",              mitk_GLCM_ROW_MAX_MEAN,	        "-nist",	                            "-pyr",	                            "-radj",	                                    "-wc",	                    "E|RMAX"],	# Mean row maximum
    ["-nyx",	            "-cp",                                                  "-imea",    "-matlab",              mitk_GLCM_ROW_AVE_MEAN,	        "-nist",	                            "-pyr",	                            "-radj",	                                    "-wc",	                    "E|RAVE"],	# Mean row average
    ["-nyx",	            "-cp",                                                  "-imea",    "-matlab",              mitk_GLCM_ROW_VAR_MEAN,	        "-nist",	                            "-pyr",	                            "-radj",	                                    "-wc",	                    "E|RVAR"],	# Mean row variance
    ["-nyx",	            "-cp",                                                  "-imea",    "-matlab",              mitk_GLCM_ROW_ENTRO_MEAN,	    "-nist",	                            "-pyr",	                            "-radj",	                                    "-wc",	                    "E|RENT"],	    # Mean row entropy
    ["-nyx",	            "-cp",                                                  "-imea",    "-matlab",              mitk_GLCM_ROWCOL_ENTRO1_MEAN,	"-nist",	                            "-pyr",	                            "-radj",	                                    "-wc",	                    "E|RCENT1"],	# Mean row-column entropy 1
    ["-nyx",	            "-cp",                                                  "-imea",    "-matlab",              mitk_GLCM_ROWCOL_ENTRO2_MEAN,   "-nist",	                            "-pyr",	                            "-radj",	                                    "-wc",	                    "E|RCENT2"],	# Mean row-column entropy 2
# GLRLM:
    ["---", "---",  "---",  "---",  "---",  "---",  "---",  "---",  "---", "!text=$\\blacktriangledown$GLRLM"], # banner
    ["GLRLM_SRE_0",	        "-cp",  "-imea",    "-matlab",  mitk_GLRLM_SRE_AVE,     "-nist",    "original_glrlm_ShortRunEmphasis",                  "GLRLM_ShortRunEmphasis",                                    "-wc",	"SRE"],     # Short Run Emphasis 
        #["GLRLM_SRE_AVE",	    "-cp",  "-imea",    "-matlab",  mitk_GLRLM_SRE_AVE,     "-nist",    "-pyr",                                             "-radj",                                    "-wc",	"E SRE"],     # Short Run Emphasis 
    ["GLRLM_LRE_0",	        "-cp",  "-imea",    "-matlab",  mitk_GLRLM_LRE_AVE,     "-nist",    "original_glrlm_LongRunEmphasis",                   "GLRLM_LongRunEmphasis",                                    "-wc",	"LRE"],     # Long Run Emphasis 
        #["GLRLM_LRE_AVE",	    "-cp",  "-imea",    "-matlab",  mitk_GLRLM_LRE_AVE,     "-nist",    "-pyr",                                             "-radj",                                    "-wc",	"E LRE"],     # Long Run Emphasis 
    ["GLRLM_GLN_0",	        "-cp",  "-imea",    "-matlab",  mitk_GLRLM_GLN_AVE,     "-nist",    "original_glrlm_GrayLevelNonUniformity",            "GLRLM_GrayLevelNonUniformity",                                    "-wc",	"GLNU"],     # Gray Level Non-Uniformity 
        #["GLRLM_GLN_AVE",	    "-cp",  "-imea",    "-matlab",  mitk_GLRLM_GLN_AVE,     "-nist",    "-pyr",                                             "-radj",             "-wc",	"E GLNU"],     # Gray Level Non-Uniformity 
    ["GLRLM_GLNN_0",	    "-cp",  "-imea",    "-matlab",  mitk_GLRLM_GLNN_AVE,    "-nist",    "original_glrlm_GrayLevelNonUniformityNormalized",  "GLRLM_GrayLevelNonUniformityNormalized",                                    "-wc",	"GLNUN"],     # Gray Level Non-Uniformity Normalized 
        #["GLRLM_GLNN_AVE",	    "-cp",  "-imea",    "-matlab",  mitk_GLRLM_GLNN_AVE,    "-nist",    "-pyr",                                             "GLRLM_GrayLevelNonUniformityNormalized",   "-wc",	"E GLNUN"],     # Gray Level Non-Uniformity Normalized 
    ["GLRLM_RLN_0",	        "-cp",  "-imea",    "-matlab",  mitk_GLRLM_RLN_AVE,     "-nist",    "original_glrlm_RunLengthNonUniformity",            "GLRLM_RunLengthNonUniformity",                                    "-wc",	"RLNU"],     # Run Length Non-Uniformity
        #["GLRLM_RLN_AVE",	    "-cp",  "-imea",    "-matlab",  mitk_GLRLM_RLN_AVE,     "-nist",    "-pyr",                                             "GLRLM_RunLengthNonUniformity",             "-wc",	"E RLNU"],     # Run Length Non-Uniformity
    ["GLRLM_RLNN_0",	    "-cp",  "-imea",    "-matlab",  mitk_GLRLM_RLNN_AVE,                "-nist",    "original_glrlm_RunLengthNonUniformityNormalized",  "GLRLM_RunLengthNonUniformityNormalized",                                    "-wc",	"RLNUN"],     # Run Length Non-Uniformity Normalized 
        #["GLRLM_RLNN_AVE",	    "-cp",  "-imea",    "-matlab",  mitk_GLRLM_RLNN_AVE,    "-nist",    "-pyr",                                             "GLRLM_RunLengthNonUniformityNormalized",   "-wc",	"E RLNUN"],     # Run Length Non-Uniformity Normalized 
    ["GLRLM_RP_0",	        "-cp",  "-imea",    "-matlab",  mitk_GLRLM_RP_AVE,                "-nist",    "original_glrlm_RunPercentage",           "GLRLM_RunPercentage",                                    "-wc",	"RP"],     # Run Percentage
        #["GLRLM_RP_AVE",	    "-cp",  "-imea",    "-matlab",  mitk_GLRLM_RP_AVE,      "-nist",    "-pyr",                                             "GLRLM_RunPercentage",                      "-wc",	"E RP"],     # Run Percentage
    ["-nyx",	            "-cp",  "-imea",    "-matlab",  "Run Length::Number of runs Means",    "-nist", "original_glrlm_RunPercentage",      "-radj",                                    "-wc",	"NR"],     # Number of runs means
    ["GLRLM_GLV_0",	        "-cp",  "-imea",    "-matlab",  mitk_GLRLM_GLV_AVE,                "-nist",    "original_glrlm_GrayLevelVariance",      "GLRLM_GrayLevelVariance",                                    "-wc",	"GLV"],     # Gray Level Variance 
        #["GLRLM_GLV_AVE",	    "-cp",  "-imea",    "-matlab",  mitk_GLRLM_GLV_AVE,     "-nist",    "-pyr",                                             "GLRLM_GrayLevelVariance",                  "-wc",	"E GLV"],     # Gray Level Variance 
    ["GLRLM_RV_0",	        "-cp",  "-imea",    "-matlab",  mitk_GLRLM_RV_AVE,                "-nist",    "original_glrlm_RunVariance",             "GLRLM_RunLengthVariance",                                    "-wc",	"RV"],     # Run Variance 
        #["GLRLM_RV_AVE",	    "-cp",  "-imea",    "-matlab",  mitk_GLRLM_RV_AVE,      "-nist",    "-pyr",                                             "GLRLM_RunLengthVariance",                  "-wc",	"E RV"],     # Run Variance means 
    ["GLRLM_RE_0",	        "-cp",  "-imea",    "-matlab",  mitk_GLRLM_RE_AVE,                "-nist",    "original_glrlm_RunEntropy",              "GLRLM_RunEntropy",                                    "-wc",	"RE"],     # Run Entropy 
        #["GLRLM_RE_AVE",	    "-cp",  "-imea",    "-matlab",  mitk_GLRLM_RE_AVE,      "-nist",    "-pyr",                                             "GLRLM_RunEntropy",                         "-wc",	"E RE"],     # Run Entropy mean
    ["GLRLM_LGLRE_0",	    "-cp",  "-imea",    "-matlab",  mitk_GLRLM_LGLRE_AVE,                "-nist",    "original_glrlm_LowGrayLevelRunEmphasis",           "GLRLM_LowGrayLevelRunEmphasis",                                    "-wc",	"LGLRE"],     # Low Gray Level Run Emphasis 
        #["GLRLM_LGLRE_AVE",	    "-cp",  "-imea",    "-matlab",  mitk_GLRLM_LGLRE_AVE,   "-nist",    "-pyr",                                             "GLRLM_LowGrayLevelRunEmphasis",            "-wc",	"E LGLRE"],     # Low Gray Level Run Emphasis 
    ["GLRLM_HGLRE_0",	    "-cp",  "-imea",    "-matlab",  mitk_GLRLM_HGLRE_AVE,                "-nist",    "original_glrlm_HighGrayLevelRunEmphasis",          "GLRLM_HighGrayLevelRunEmphasis",                                    "-wc",	"HGLRE"],     # High Gray Level Run Emphasis 
        #["GLRLM_HGLRE_AVE",	    "-cp",  "-imea",    "-matlab",  mitk_GLRLM_HGLRE_AVE,   "-nist",    "-pyr",                                             "GLRLM_HighGrayLevelRunEmphasis",           "-wc",	"E HGLRE"],     # High Gray Level Run Emphasis 
    ["GLRLM_SRLGLE_0",	    "-cp",  "-imea",    "-matlab",  mitk_GLRLM_SRLGLE_AVE,                "-nist",    "original_glrlm_ShortRunLowGrayLevelEmphasis",      "GLRLM_ShortRunLowGrayLevelEmphasis",                                    "-wc",	"SRLGLE"],     # Short Run Low Gray Level Emphasis 
        #["GLRLM_SRLGLE_AVE",	"-cp",  "-imea",    "-matlab",  mitk_GLRLM_SRLGLE_AVE,  "-nist",    "-pyr",                                             "GLRLM_ShortRunLowGrayLevelEmphasis",       "-wc",	"E SRLGLE"],     # Short Run Low Gray Level Emphasis 
    ["GLRLM_SRHGLE_0",	    "-cp",  "-imea",    "-matlab",  mitk_GLRLM_SRHGLE_AVE,                "-nist",    "original_glrlm_ShortRunHighGrayLevelEmphasis",     "GLRLM_ShortRunHighGrayLevelEmphasis",                                    "-wc",	"SRHGLE"],     # Short Run High Gray Level Emphasis 
        #["GLRLM_SRHGLE_AVE",    "-cp",  "-imea",    "-matlab",  mitk_GLRLM_SRHGLE_AVE,  "-nist",    "-pyr",                                             "GLRLM_ShortRunHighGrayLevelEmphasis",      "-wc",	"E SRHGLE"],     # Short Run High Gray Level Emphasis 
    ["GLRLM_LRLGLE_0",	    "-cp",  "-imea",    "-matlab",  mitk_GLRLM_LRLGLE_AVE,                "-nist",    "original_glrlm_LongRunLowGrayLevelEmphasis",       "GLRLM_LongRunLowGrayLevelEmphasis",                                    "-wc",	"LRLGLE"],     # Long Run Low Gray Level Emphasis 
        #["GLRLM_LRLGLE_AVE",	"-cp",  "-imea",    "-matlab",  mitk_GLRLM_LRLGLE_AVE,  "-nist",    "-pyr",                                             "GLRLM_LongRunLowGrayLevelEmphasis",        "-wc",	"E LRLGLE"],     # Long Run Low Gray Level Emphasis 
    ["GLRLM_LRHGLE_0",	    "-cp",  "-imea",    "-matlab",  mitk_GLRLM_LRHGLE_AVE,                "-nist",    "original_glrlm_LongRunHighGrayLevelEmphasis",      "GLRLM_LongRunHighGrayLevelEmphasis",                                    "-wc",	"LRHGLE"],     # Long Run High Gray Level Emphasis 
        #["GLRLM_LRHGLE_AVE",	"-cp",  "-imea",    "-matlab",  mitk_GLRLM_LRHGLE_AVE,  "-nist",    "-pyr",                                             "GLRLM_LongRunHighGrayLevelEmphasis",       "-wc",	"E LRHGLE"],     # Long Run High Gray Level Emphasis 
    
# GLDZM:
    ["---", "---",  "---",  "---",  "---",  "---",  "---",  "---",  "---", "!text=$\\blacktriangledown$GLDZM"], # banner
    ["GLDZM_SDE",		"-cp",		"-imea",		"-matlab",		"Grey Level Distance Zone::Small Distance Emphasis",		"-nist",		"-pyr",		"GLDZM_SmallDistanceEmphasis",		"-wc",	"SDE"],		# Small Distance Emphasis
    ["GLDZM_LDE",		"-cp",		"-imea",		"-matlab",		"Grey Level Distance Zone::Large Distance Emphasis",		"-nist",		"-pyr",		"GLDZM_LargeDistanceEmphasis",		"-wc",	"LDE"],		# Large Distance Emphasis
    ["GLDZM_LGLZE",		"-cp",		"-imea",		"-matlab",		"Grey Level Distance Zone::Low Grey Level Emphasis",		"-nist",		"-pyr",		"GLDZM_LowGrayLevelZoneEmphasis",		"-wc",	"LGLZE"],		# Low Grey Level Zone Emphasis
    ["GLDZM_HGLZE",		"-cp",		"-imea",		"-matlab",		"Grey Level Distance Zone::High Grey Level Emphasis",		"-nist",		"-pyr",		"GLDZM_HighGrayLevelZoneEmphasis",		"-wc",	"HGHZE"],		# High Grey Level Zone Emphasis
    ["GLDZM_SDLGLE",	"-cp",		"-imea",		"-matlab",		"Grey Level Distance Zone::Small Distance Low Grey Level Emphasis",		"-nist",		"-pyr",		"GLDZM_SmallDistanceLowGrayLevelEmphasis",		"-wc",	"SDLGLE"],		# Small Distance Low Grey Level Emphasis
    ["GLDZM_SDHGLE",	"-cp",		"-imea",		"-matlab",		"Grey Level Distance Zone::Small Distance High Grey Level Emphasis",		"-nist",		"-pyr",		"GLDZM_SmallDistanceHighGrayLevelEmphasis",		"-wc",	"SDHGLE"],		# Small Distance High Grey Level Emphasis
    ["GLDZM_LDLGLE",	"-cp",		"-imea",		"-matlab",		"Grey Level Distance Zone::Large Distance Low Grey Level Emphasis",		"-nist",		"-pyr",		"GLDZM_LargeDistanceLowGrayLevelEmphasis",		"-wc",	"LDLGLE"],		# Large Distance Low Grey Level Emphasis
    ["GLDZM_LDHGLE",	"-cp",		"-imea",		"-matlab",		"Grey Level Distance Zone::Large Distance High Grey Level Emphasis",		"-nist",		"-pyr",		"GLDZM_LargeDistanceHighGrayLevelEmphasis",		"-wc",	"LDHGLE"],		# Large Distance High Grey Level Emphasis
    ["GLDZM_GLNU",		"-cp",		"-imea",		"-matlab",		"Grey Level Distance Zone::Grey Level Non-Uniformity",		"-nist",		"-pyr",		"GLDZM_GrayLevelNonUniformity",		"-wc",	"GLNU"],		# Grey Level Non Uniformity
    ["GLDZM_GLNUN",		"-cp",		"-imea",		"-matlab",		"Grey Level Distance Zone::Grey Level Non-Uniformity Normalized",		"-nist",		"-pyr",		"GLDZM_GrayLevelNonUniformityNormalized",		"-wc",	"GLNUN"],		# Grey Level Non Uniformity Normalized
    ["GLDZM_ZDNU",		"-cp",		"-imea",		"-matlab",		"Grey Level Distance Zone::Distance Size Non-Uniformity",		"-nist",		"-pyr",		"GLDZM_ZoneDistanceNonUniformity",		"-wc",	"ZDNU"],		# Zone Distance Non Uniformity
    ["GLDZM_ZDNUN",		"-cp",		"-imea",		"-matlab",		"Grey Level Distance Zone::Distance Size Non-Uniformity Normalized",		"-nist",		"-pyr",		"GLDZM_ZoneDistanceNonUniformityNormalized",		"-wc",	"ZDNUN"],		# Zone Distance Non Uniformity Normalized
    ["GLDZM_ZP",		"-cp",		"-imea",		"-matlab",		"Grey Level Distance Zone::Zone Percentage",		"-nist",		"-pyr",		"GLDZM_ZonePercentage",		"-wc",	"ZP"],		# Zone Percentage
    ["GLDZM_GLM",		"-cp",		"-imea",		"-matlab",		"Grey Level Distance Zone::Grey Level Mean",		"-nist",		"-pyr",		"-radj",		"-wc",	"GLM"],		# Grey Level Mean
    ["GLDZM_GLV",		"-cp",		"-imea",		"-matlab",		"Grey Level Distance Zone::Grey Level Variance",		"-nist",		"-pyr",		"GLDZM_GrayLevelVariance",		"-wc",	"GLV"],		# Grey Level Variance
    ["GLDZM_ZDM",		"-cp",		"-imea",		"-matlab",		"Grey Level Distance Zone::Zone Distance Mean",		"-nist",		"-pyr",		"-radj",		"-wc",	"ZDM"],		# Zone Distance Mean
    ["GLDZM_ZDV",		"-cp",		"-imea",		"-matlab",		"Grey Level Distance Zone::Zone Distance Variance",		"-nist",		"-pyr",		"GLDZM_ZoneDistanceVariance",		"-wc",	"ZDV"],		# Zone Distance Variance
    ["GLDZM_ZDE",		"-cp",		"-imea",		"-matlab",		"Grey Level Distance Zone::Zone Distance Entropy",		"-nist",		"-pyr",		"GLDZM_ZoneDistanceEntropy",		"-wc",	"ZDE"],		# Zone Distance Entropy
    ["-nyx",    		"-cp",		"-imea",		"-matlab",		"Grey Level Distance Zone::Grey Level Entropy",		"-nist",		"-pyr",		"-radj",		"-wc",	"GLE"],		# Grey level entropy (MITK)
# GLSZM:
    ["---", "---",  "---",  "---",  "---",  "---",  "---",  "---",  "---", "!text=$\\blacktriangledown$GLSZM"], # banner
    ["GLSZM_SAE",		"-cp",		"-imea",		"-matlab",		"-mitk",		"-nist",		"original_glszm_SmallAreaEmphasis",		            "GLSZM_SmallZoneEmphasis",		"-wc",	"SAE"],		# Small Area Emphasis
    ["GLSZM_LAE",		"-cp",		"-imea",		"-matlab",		"-mitk",		"-nist",		"original_glszm_LargeAreaEmphasis",		            "GLSZM_LargeZoneEmphasis",		"-wc",	"LAE"],		# Large Area Emphasis
    ["GLSZM_GLN",		"-cp",		"-imea",		"-matlab",		"-mitk",		"-nist",		"original_glszm_GrayLevelNonUniformity",            "GLSZM_GrayLevelNonUniformity",		"-wc",	"GLNU"],		# Gray Level Non - Uniformity
    ["GLSZM_GLNN",		"-cp",		"-imea",		"-matlab",		"-mitk",		"-nist",		"original_glszm_GrayLevelNonUniformityNormalized",  "GLSZM_GrayLevelNonUniformityNormalized",		"-wc",	"GLNUN"],		# Gray Level Non - Uniformity Normalized
    ["GLSZM_SZN",		"-cp",		"-imea",		"-matlab",		"-mitk",		"-nist",		"original_glszm_SizeZoneNonUniformity",		        "GLSZM_SizeZoneNonUniformity",		"-wc",	"SZNU"],		# Size - Zone Non - Uniformity
    ["GLSZM_SZNN",		"-cp",		"-imea",		"-matlab",		"-mitk",		"-nist",		"original_glszm_SizeZoneNonUniformityNormalized",	"GLSZM_SizeZoneNonUniformityNormalized",		"-wc",	"SZNUN"],		# Size - Zone Non - Uniformity Normalized
    ["GLSZM_ZP",		"-cp",		"-imea",		"-matlab",		"-mitk",		"-nist",		"original_glszm_ZonePercentage",		            "GLSZM_ZonePercentage",		"-wc",	"ZP"],		# Zone Percentage
    ["GLSZM_GLV",		"-cp",		"-imea",		"-matlab",		"-mitk",		"-nist",		"original_glszm_GrayLevelVariance",		            "GLSZM_GrayLevelVariance",		"-wc",	"GLV"],		# Gray Level Variance
    ["GLSZM_ZV",		"-cp",		"-imea",		"-matlab",		"-mitk",		"-nist",		"original_glszm_ZoneVariance",		                "GLSZM_ZoneSizeVariance",		"-wc",	"ZV"],		# Zone Variance
    ["GLSZM_ZE",		"-cp",		"-imea",		"-matlab",		"-mitk",		"-nist",		"original_glszm_ZoneEntropy",		                "GLSZM_ZoneSizeEntropy",		"-wc",	"ZE"],		# Zone Entropy
    ["GLSZM_LGLZE",		"-cp",		"-imea",		"-matlab",		"-mitk",		"-nist",		"original_glszm_LowGrayLevelZoneEmphasis",		    "GLSZM_LowGrayLevelZoneEmphasis",		"-wc",	"LGLZE"],		# Low Gray Level Zone Emphasis
    ["GLSZM_HGLZE",		"-cp",		"-imea",		"-matlab",		"-mitk",		"-nist",		"original_glszm_HighGrayLevelZoneEmphasis",		    "GLSZM_HighGrayLevelZoneEmphasis",		"-wc",	"HGLZE"],		# High Gray Level Zone Emphasis
    ["GLSZM_SALGLE",	"-cp",		"-imea",		"-matlab",		"-mitk",		"-nist",		"original_glszm_SmallAreaLowGrayLevelEmphasis",		"GLSZM_SmallZoneLowGrayLevelEmphasis",		"-wc",	"SALGLE"],		# Small Area Low Gray Level Emphasis
    ["GLSZM_SAHGLE",	"-cp",		"-imea",		"-matlab",		"-mitk",		"-nist",		"original_glszm_SmallAreaHighGrayLevelEmphasis",    "GLSZM_SmallZoneHighGrayLevelEmphasis",		"-wc",	"SAHGLE"],		# Small Area High Gray Level Emphasis
    ["GLSZM_LALGLE",	"-cp",		"-imea",		"-matlab",		"-mitk",		"-nist",		"original_glszm_LargeAreaLowGrayLevelEmphasis",		"GLSZM_LargeZoneLowGrayLevelEmphasis",		"-wc",	"LALGLE"],		# Large Area Low Gray Level Emphasis
    ["GLSZM_LAHGLE",	"-cp",		"-imea",		"-matlab",		"-mitk",		"-nist",		"original_glszm_LargeAreaHighGrayLevelEmphasis",	"GLSZM_LargeZoneHighGrayLevelEmphasis",		"-wc",	"LAHGLE"],		# Large Area High Gray Level Emphasis
# GLDM:
    ["---", "---",  "---",  "---",  "---",  "---",  "---",  "---",  "---", "!text=$\\blacktriangledown$GLDM"], # banner
    ["GLDM_SDE",			"-cp",		"-imea",		"-matlab",		"-mitk",		"-nist",		"original_gldm_SmallDependenceEmphasis",		"-radj",		"-wc",	"SDE"],		# Small Dependence Emphasis
    ["GLDM_LDE",			"-cp",		"-imea",		"-matlab",		"-mitk",		"-nist",		"original_gldm_LargeDependenceEmphasis",		"-radj",		"-wc",	"LDE"],		# Large Dependence Emphasis
    ["GLDM_GLN",			"-cp",		"-imea",		"-matlab",		"-mitk",		"-nist",		"original_gldm_GrayLevelNonUniformity",		"-radj",		"-wc",	"GLNU"],		# Gray Level Non-Uniformity
    ["GLDM_DN",				"-cp",		"-imea",		"-matlab",		"-mitk",		"-nist",		"original_gldm_DependenceNonUniformity",		"-radj",		"-wc",	"DNU"],		# Dependence Non-Uniformity
    ["GLDM_DNN",			"-cp",		"-imea",		"-matlab",		"-mitk",		"-nist",		"original_gldm_DependenceNonUniformityNormalized",		"-radj",		"-wc",	"DNUN"],		# Dependence Non-Uniformity Normalized
    ["GLDM_GLV",			"-cp",		"-imea",		"-matlab",		"-mitk",		"-nist",		"original_gldm_GrayLevelVariance",		"-radj",		"-wc",	"GLV"],		# Gray Level Variance
    ["GLDM_DV",				"-cp",		"-imea",		"-matlab",		"-mitk",		"-nist",		"original_gldm_DependenceVariance",		"-radj",		"-wc",	"DV"],		# Dependence Variance
    ["GLDM_DE",				"-cp",		"-imea",		"-matlab",		"-mitk",		"-nist",		"original_gldm_DependenceEntropy",		"-radj",		"-wc",	"DE"],		# Dependence Entropy
    ["GLDM_LGLE",			"-cp",		"-imea",		"-matlab",		"-mitk",		"-nist",		"original_gldm_LowGrayLevelEmphasis",		"-radj",		"-wc",	"LGLE"],		# Low Gray Level Emphasis
    ["GLDM_HGLE",			"-cp",		"-imea",		"-matlab",		"-mitk",		"-nist",		"original_gldm_HighGrayLevelEmphasis",		"-radj",		"-wc",	"GHLE"],		# High Gray Level Emphasis
    ["GLDM_SDLGLE",			"-cp",		"-imea",		"-matlab",		"-mitk",		"-nist",		"original_gldm_SmallDependenceLowGrayLevelEmphasis",		"-radj",		"-wc",	"SDLGLE"],		# Small Dependence Low Gray Level Emphasis
    ["GLDM_SDHGLE",			"-cp",		"-imea",		"-matlab",		"-mitk",		"-nist",		"original_gldm_SmallDependenceHighGrayLevelEmphasis",		"-radj",		"-wc",	"SDHGLE"],		# Small Dependence High Gray Level Emphasis
    ["GLDM_LDLGLE",			"-cp",		"-imea",		"-matlab",		"-mitk",		"-nist",		"original_gldm_LargeDependenceLowGrayLevelEmphasis",		"-radj",		"-wc",	"LDLGLE"],		# Large Dependence Low Gray Level Emphasis
    ["GLDM_LDHGLE",			"-cp",		"-imea",		"-matlab",		"-mitk",		"-nist",		"original_gldm_LargeDependenceHighGrayLevelEmphasis",		"-radj",		"-wc",	"LDHGLE"],		# Large Dependence High Gray Level Emphasis
# NGLDM:
    ["---", "---",  "---",  "---",  "---",  "---",  "---",  "---",  "---", "!text=$\\blacktriangledown$NGLDM"], # banner
    ["NGLDM_LDE",		"-cp",		"-imea",	"-matlab",		"Neighbouring Grey Level Dependence::Low Dependence Emphasis",		"-nist",		"-pyr",		"NGLDM_LowDependenceEmphasis",		"-wc",	"LDE"],		# Low Dependence Emphasis (IBSI # SODN)
    ["NGLDM_HDE",		"-cp",		"-imea",	"-matlab",		"Neighbouring Grey Level Dependence::High Dependence Emphasis",		"-nist",		"-pyr",		"NGLDM_HighDependenceEmphasis",		"-wc",	"HDE"],		# High Dependence Emphasis (IBSI # IMOQ)
    ["NGLDM_LGLCE",		"-cp",		"-imea",	"-matlab",		"Neighbouring Grey Level Dependence::Low Grey Level Count Emphasis",		"-nist",		"-pyr",		"NGLDM_LowGrayLevelCountEmphasis",		"-wc",	"LGLCE"],		# Low Grey Level Count Emphasis (IBSI # TL9H)
    ["NGLDM_HGLCE",		"-cp",		"-imea",	"-matlab",		"Neighbouring Grey Level Dependence::High Grey Level Count Emphasis",		"-nist",		"-pyr",		"NGLDM_HighGrayLevelCountEmphasis",		"-wc",	"HGLCE"],		# High Grey Level Count Emphasis (IBSI # OAE7)
    ["NGLDM_LDLGLE",	"-cp",		"-imea",	"-matlab",		"Neighbouring Grey Level Dependence::Low Dependence Low Grey Level Emphasis",		"-nist",		"-pyr",		"NGLDM_LowDependenceLowGrayLevelEmphasis",		"-wc",	"LDLGLE"],		# Low Dependence Low Grey Level Emphasis (IBSI # EQ3F)
    ["NGLDM_LDHGLE",	"-cp",		"-imea",	"-matlab",		"Neighbouring Grey Level Dependence::Low Dependence High Grey Level Emphasis",		"-nist",		"-pyr",		"NGLDM_LowDependenceHighGrayLevelEmphasis",		"-wc",	"LDHGLE"],		# Low Dependence High Grey Level Emphasis (IBSI # JA6D)
    ["NGLDM_HDLGLE",	"-cp",		"-imea",	"-matlab",		"Neighbouring Grey Level Dependence::High Dependence Low Grey Level Emphasis",		"-nist",		"-pyr",		"NGLDM_HighDependenceLowGrayLevelEmphasis",		"-wc",	"HDLGLE"],		# High Dependence Low Grey Level Emphasis (IBSI # NBZI)
    ["NGLDM_HDHGLE",	"-cp",		"-imea",	"-matlab",		"Neighbouring Grey Level Dependence::High Dependence High Grey Level Emphasis",		"-nist",		"-pyr",		"NGLDM_HighDependenceHighGrayLevelEmphasis",		"-wc",	"HDHGLE"],		# High Dependence High Grey Level Emphasis (IBSI # 9QMG)
    ["NGLDM_GLNU",		"-cp",		"-imea",	"-matlab",		"Neighbouring Grey Level Dependence::Grey Level Non-Uniformity",		"-nist",		"-pyr",		"NGLDM_GrayLevelNonUniformity",		"-wc",	"GLNU"],		# Grey Level Non-Uniformity (IBSI # FP8K)
    ["NGLDM_GLNUN",		"-cp",		"-imea",	"-matlab",		"Neighbouring Grey Level Dependence::Grey Level Non-Uniformity Normalised",		"-nist",		"-pyr",		"NGLDM_GrayLevelNonUniformityNormalized",		"-wc",	"GLNUN"],		# Grey Level Non-Uniformity Normalised (IBSI # 5SPA)
    ["NGLDM_DCNU",		"-cp",		"-imea",	"-matlab",		"Neighbouring Grey Level Dependence::Dependence Count Non-Uniformity",		"-nist",		"-pyr",		"NGLDM_DependenceCountNonUniformity",		"-wc",	"DCNU"],		# Dependence Count Non-Uniformity (IBSI # Z87G)
    ["NGLDM_DCNUN",		"-cp",		"-imea",	"-matlab",		"Neighbouring Grey Level Dependence::Dependence Count Non-Uniformity Normalised",		"-nist",		"-pyr",		"NGLDM_DependenceCountNonUniformityNormalized",		"-wc",	"DCNUN"],		# Dependence Count Non-Uniformity Normalised (IBSI # OKJI)
    ["NGLDM_DCP",		"-cp",		"-imea",	"-matlab",		"Neighbouring Grey Level Dependence::Dependence Count Percentage",		"-nist",		"-pyr",		"-radj",		"-wc",	"DCP"],		# Dependence Count Percentage (IBSI # 6XV8)
    ["NGLDM_GLM",		"-cp",		"-imea",	"-matlab",		"Neighbouring Grey Level Dependence::Grey Level Mean",		"-nist",		"-pyr",		"-radj",		"-wc",	"GLM"],		# Grey Level Mean
    ["NGLDM_GLV",		"-cp",		"-imea",	"-matlab",		"Neighbouring Grey Level Dependence::Grey Level Variance",		"-nist",		"-pyr",		"NGLDM_GrayLevelVariance",		"-wc",	"GLV"],		# Grey Level Variance (IBSI # 1PFV)
    ["NGLDM_DCM",		"-cp",		"-imea",	"-matlab",		"Neighbouring Grey Level Dependence::Dependence Count Mean",		"-nist",		"-pyr",		"-radj",		"-wc",	"DCM"],		# Dependence Count Mean
    ["NGLDM_DCV",		"-cp",		"-imea",	"-matlab",		"Neighbouring Grey Level Dependence::Dependence Count Variance",		"-nist",		"-pyr",		"NGLDM_DependenceCountVariance",		"-wc",	"DCV"],		# Dependence Count Variance (IBSI # DNX2)
    ["NGLDM_DCENT",		"-cp",		"-imea",	"-matlab",		"Neighbouring Grey Level Dependence::Dependence Count Entropy",		"-nist",		"-pyr",		"NGLDM_DependenceCountEntropy",		"-wc",	"DCENT"],		# Dependence Count Entropy (IBSI # FCBV)
    ["NGLDM_DCENE",		"-cp",		"-imea",	"-matlab",		"Neighbouring Grey Level Dependence::Dependence Count Energy",		"-nist",		"-pyr",		"NGLDM_DependenceCountEnergy",		"-wc",	"DCE"],		# Dependence Count Energy (IBSI # CAS9)
    ["-nyx",		"-cp",		"-imea",	"-matlab",		"Neighbouring Grey Level Dependence::Expected Neighbourhood Size",		            "-nist",		"-pyr",		"-radj",		"-wc",	"ENS"],		# Expected Neighbourhood Size
    ["-nyx",		"-cp",		"-imea",	"-matlab",		"Neighbouring Grey Level Dependence::Average Neighbourhood Size",		            "-nist",		"-pyr",		"-radj",		"-wc",	"ANS"],		# Average Neighbourhood Size
    ["-nyx",		"-cp",		"-imea",	"-matlab",		"Neighbouring Grey Level Dependence::Average Incomplete Neighbourhood Size",		"-nist",		"-pyr",		"-radj",		"-wc",	"AINS"],		# Average Incomplete Neighbourhood Size
    ["-nyx",		"-cp",		"-imea",	"-matlab",		"Neighbouring Grey Level Dependence::Percentage of complete Neighbourhoods",		"-nist",		"-pyr",		"-radj",		"-wc",	"PCN"],		# Percentage of complete Neighbourhoods
    ["-nyx",		"-cp",		"-imea",	"-matlab",		"Neighbouring Grey Level Dependence::Percentage of Dependence Neighbour Voxels",    "-nist",		"-pyr",		"-radj",		"-wc",	"PDNV"],		# Percentage of Dependence Neighbour Voxels
# NGTDM:
    ["---",                 "---",      "---",          "---",          "---",                                              "---",          "---",                          "---",                  "---",  "!text=$\\blacktriangledown$NGTDM"], # banner
    ["NGTDM_COARSENESS",	"-cp",		"-imea",		"-matlab",		"Neighbourhood Grey Tone Difference::Coarsness",	"-nist",		"original_ngtdm_Coarseness",	"NGTDM_Coarseness",		"-wc",	"COAR"],		# Coarseness
    ["NGTDM_CONTRAST",		"-cp",		"-imea",		"-matlab",		"Neighbourhood Grey Tone Difference::Contrast",		"-nist",		"original_ngtdm_Contrast",		"NGTDM_Contrast",		"-wc",	"CONTR"],		# Contrast
    ["NGTDM_BUSYNESS",		"-cp",		"-imea",		"-matlab",		"Neighbourhood Grey Tone Difference::Busyness",		"-nist",		"original_ngtdm_Busyness",		"NGTDM_Busyness",		"-wc",	"BUSYN"],		# Busyness
    ["NGTDM_COMPLEXITY",	"-cp",		"-imea",		"-matlab",		"Neighbourhood Grey Tone Difference::Complexity",	"-nist",		"original_ngtdm_Complexity",	"NGTDM_Complexity",		"-wc",	"COMPL"],		# Complexity
    ["NGTDM_STRENGTH",		"-cp",		"-imea",		"-matlab",		"Neighbourhood Grey Tone Difference::Strength",		"-nist",		"original_ngtdm_Strength",		"NGTDM_Strength",		"-wc",	"STREN"]		# Strength
	])    

Fmap_shape = np.array([
    ["---0", "---1",  "---2",  "---3",  "---4",  "---5",  "---6",  "---7",  "---8", "!image=banner_shape.png"], # banner
    # [0]nyxus                          [1]cellprofiler                         [2]imea             [3]matlab   [4]mitk     [5]nist                         [6]pyr      [7]radj     [8]wc   [9]uffn
    ["-nyx",                            "Intensity_MassDisplacement_intensity", "-imea",            "-matlab",  "-mitk",    "-nist",                        "-pyr",     "-radj",    "-wc", "MD"], # Mass displacement
    ["AREA_PIXELS_COUNT",               "AreaShape_Area",                       "area_filled",            "area",     "-mitk",    "Feature2DJava_Area",           "diagnostics_Mask-original_VoxelNum",   "Morphology_VolumeVoxelCounting", "original-filled_area_pixels", "area"],	# Area
    ["-nyx",                            "-cp",                                  "area_projection",  "-matlab", "-mitk", "-nist", "-pyr", "-radj", "-wc", "area proj"], # Area projection
    ["-nyx",                            "-cp",                                  "-imea",            "-matlab",  "-mitk",    "Feature2DJava_Aspect_Ratio_BB",                "-pyr",     "-radj",    "-wc",  "aspR"], # Aspect Ratio
    ["-nyx",                            "AreaShape_BoundingBoxArea",            "-imea",            "-matlab", "-mitk", "-nist", "-pyr", "-radj", "-wc",   "BB area"], # in cellprofiler: Bounding box area
    ["-nyx",                            "-cp",                                  "-imea",            "-matlab",  "-mitk",    "Feature2DJava_Center_BB_X",    "-pyr", "-radj", "-wc", "BB cx"], # BB center X
    ["-nyx",                            "-cp",                                  "-imea",            "-matlab",  "-mitk",    "Feature2DJava_Center_BB_Y",    "-pyr", "-radj", "-wc", "BB cy"], # BB center Y
    ["BBOX_HEIGHT",                     "-cp",                                  "y_max",            "bb4",      "-mitk",    "Feature2DJava_BB_Height",      "-pyr", "-radj", "original-bbox_height", "BB h"], 	# BB Height
    ["BBOX_WIDTH",                      "-cp",                                  "x_max",            "bb3",      "-mitk",    "Feature2DJava_BB_Width",       "-pyr", "-radj", "original-bbox_width", "BB w"], 	# BB Width 
    ["-nyx",                            "-cp",                                  "-imea",            "-matlab",  "-mitk",    "-nist",       "-pyr", "-radj", "original-rotated_bounding_box_width", "RBB w"], 	# rotated BB Width 
    ["-nyx",                            "-cp",                                  "-imea",            "-matlab",  "-mitk",    "-nist",       "-pyr", "-radj", "original-rotated_bounding_box_width", "RBB w"], 	# rotated BB Width 
    ["-nyx",                            "AreaShape_BoundingBoxMaximum_X",       "-imea",            "-matlab", "-mitk", "-nist", "-pyr", "-radj", "-wc", "BB max x"], # Bounding Box Maximum X
    ["-nyx",                            "AreaShape_BoundingBoxMaximum_Y",       "-imea",            "-matlab", "-mitk", "-nist", "-pyr", "-radj", "-wc", "BB max Y"], # Bounding Box Maximum Y
    ["-nyx",                            "AreaShape_BoundingBoxMinimum_X",       "length_min_bb",    "-matlab",  "-mitk",    "Feature2DJava_BB_Xmin",    "-pyr",     "-radj", "-wc", "BB min x"], # Bounding Box Min X (fuzzy for Imea)
    ["-nyx",                            "AreaShape_BoundingBoxMinimum_Y",       "-width_min_bb",    "-matlab",  "-mitk",    "Feature2DJava_BB_Ymin",    "-pyr",     "-radj", "-wc", "BB min y"], # Bounding Box Min Y (fuzzy for Imea)
    ["BBOX_XMIN",                       "-cp",                                  "-imea",            "bb1", "-mitk", "-nist", "-pyr", "-radj", "original-bbox_xmin", "BB x"], 	# Bounding Box X
    ["BBOX_YMIN",                       "-cp",                                  "-imea",            "bb2", "-mitk", "-nist", "-pyr", "-radj", "original-bbox_ymin", "BB y"], 	# Bounding Box Y
    ["-BBOX_EXTEND",                    "-cp",                                  "-imea",            "-matlab", "-mitk", "Feature2DJava_ExtendBB", "-pyr", "-radj", "-wc", "ext BB"], 	# Extend Bounding Box isg.nist.gov/deepzoomweb/stemcellfeatures#eccentricity
    ["CENTROID_X",                      "AreaShape_Center_X",                   "-imea",            "centroidX",    "-mitk",    "Feature2DJava_Centroid_X",     "-PYR-diagnostics_Mask-original_CenterOfMass",     "-radj", "original-centroid_x", "cx"], 	# Centroid X
    ["CENTROID_Y",                      "AreaShape_Center_Y",                   "-imea",            "centroidY",    "-mitk",    "Feature2DJava_Centroid_Y",     "-PYR-diagnostics_Mask-original_CenterOfMass",     "-radj", "original-centroid_y", "cy"], 	# Centroid Y
    ["CIRCULARITY",                     "AreaShape_FormFactor",                 "-imea",                            "-matlab",  "-mitk",    "Feature2DJava_Circularity",    "-pyr",     "Shape2D_Circularity", "original-circularity", "circ/ff"], 	# Circularity, formfactor
    ["COMPACTNESS",                     "AreaShape_Compactness",                "-imea",            "-matlab", "-mitk", "-nist", "-pyr", "-radj", "-wc", "comp"], 	# Compactness
    ["CONVEX_HULL_AREA",                "AreaShape_ConvexArea",                 "area_convex",      "convexArea",   "-mitk", "-nist", "-pyr", "-radj", "original-convex_area", "CH area"], 	# Convex hull area
    ["-nyx",                            "-cp",                                  "convex_perimeter", "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-convex_hull_perimeter", "CHP"], # Convex perimeter
    ["-nyx",                            "-cp",                                  "diameter_max_inclosing_circle",    "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-max_inclosing_circle_diameter", "D max enc cir"], # D max enc circle
    ["DIAMETER_MIN_ENCLOSING_CIRCLE",   "-cp",                                  "diameter_min_enclosing_circle",    "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-diameter_min_enclosing_circle", "D min encl cir"], 	# D min enc circle
    ["DIAMETER_CIRCUMSCRIBING_CIRCLE",  "-cp",                                  "diameter_circumscribing_circle",   "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-diameter_circumscribing_circle", "D circum cir"], 	# D circum circle
    ["DIAMETER_INSCRIBING_CIRCLE",      "-cp",                                  "diameter_inscribing_circle",       "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-diameter_inscribing_circle", "D inscr cir"], 	# D insc circle
    ["DIAMETER_EQUAL_AREA",             "-cp",                                  "diameter_equal_area",              "-matlab", "-mitk", "-nist", "-pyr", "-radj", "-wc", "D equal area"], 	# \diameter equal area
    ["DIAMETER_EQUAL_PERIMETER",        "-cp",                                  "diameter_equal_perimeter",         "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-diameter_equal_perimeter", "D equal P"], 	# \diameter equal perimeter
    ["-nyx",                            "-cp",                                  "-imea",    "-matlab",  "-mitk",    "Feature2DJava_Distance_From_Border",   "-pyr",     "-radj", "-wc", "dist f bord"], # Dist from border
    ["ECCENTRICITY",                    "AreaShape_Eccentricity",               "-imea",            "eccentricity", "-mitk", "Feature2DJava_Eccentricity", "-pyr", "-radj", "original-eccentricity", "eccentri"], 	# Eccentricity
    ["ELONGATION",                      "-cp",                                  "-imea", "-matlab", "-mitk", "-nist", "original_shape_Elongation", "-radj", "-wc", "elong"], 	# Elongation
    ["DIAMETER_EQUAL_AREA",             "AreaShape_EquivalentDiameter",         "-imea", "equivD", "-mitk", "-nist", "-pyr", "-radj", "original-equivalent_diameter", "equiv D"], # Equiv \diameter
    ["EXTENT",                          "AreaShape_Extent",                     "-imea", "extent", "-mitk", "-nist", "-pyr", "-radj", "original-extent", "extent"], 	# Extent
    ["-skipped-EXTREMA_P1_X",                    "-cp",                                  "-imea", "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-extremap1_x", "extr p1X"], 	# Extrema
    ["-skipped-EXTREMA_P1_Y",                    "-cp",                                  "-imea", "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-extremap1_y", "extr pY"], 	# Extrema
    ["-skipped-EXTREMA_P2_X",                    "-cp",                                  "-imea", "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-extremap2_x", "extr p2X"], 	# Extrema
    ["-skipped-EXTREMA_P2_Y",                    "-cp",                                  "-imea", "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-extremap2_y", "extr p2Y"], 	# Extrema
    ["-skipped-EXTREMA_P3_X",                    "-cp",                                  "-imea", "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-extremap3_x", "extr p3X"], 	# Extrema
    ["-skipped-EXTREMA_P3_Y",                    "-cp",                                  "-imea", "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-extremap3_y", "extr p3Y"], 	# Extrema
    ["-skipped-EXTREMA_P4_X",                    "-cp",                                  "-imea", "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-extremap4_x", "extr p4X"], 	# Extrema
    ["-skipped-EXTREMA_P4_Y",                    "-cp",                                  "-imea", "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-extremap4_y", "extr p4Y"], 	# Extrema
    ["-skipped-EXTREMA_P5_X",                    "-cp",                                  "-imea", "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-extremap5_x", "extr p5X"], 	# Extrema
    ["-skipped-EXTREMA_P5_Y",                    "-cp",                                  "-imea", "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-extremap5_y", "extr p5Y"], 	# Extrema
    ["-skipped-EXTREMA_P6_X",                    "-cp",                                  "-imea", "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-extremap6_x", "extr p6X"], 	# Extrema
    ["-skipped-EXTREMA_P6_Y",                    "-cp",                                  "-imea", "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-extremap6_y", "extr p6Y"], 	# Extrema
    ["-skipped-EXTREMA_P7_X",                    "-cp",                                  "-imea", "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-extremap7_x", "extr p7X"], 	# Extrema
    ["-skipped-EXTREMA_P7_Y",                    "-cp",                                  "-imea", "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-extremap7_y", "extr p7Y"], 	# Extrema
    ["EXTREMA_P8_X",                    "-cp",                                  "-imea", "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-extremap8_x", "extr p8X"], 	# Extrema
    ["EXTREMA_P8_Y",                    "-cp",                                  "-imea", "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-extremap8_y", "extr p8Y"], 	# Extrema
	["POLYGONALITY_AVE",                "-cp",                                  "-imea", "-matlab", "-mitk", "-nist", "-pyr", "-radj",  "original-polygonality_score",  "polyg ave"],
	["HEXAGONALITY_AVE",                "-cp",                                  "-imea", "-matlab", "-mitk", "-nist", "-pyr", "-radj",  "original-hexagonality_score",  "hexag ave"],
	["HEXAGONALITY_STDDEV",             "-cp",                                  "-imea", "-matlab", "-mitk", "-nist", "-pyr", "-radj",  "original-hexagonality_sd",     "hexag std"],
    ["EULER_NUMBER",                    "AreaShape_EulerNumber",                "-imea", "eulerNumber", "-mitk", "-nist", "-pyr", "-radj", "original-euler_number", "euler n"], 	# Euler number
    ["GEODETIC_LENGTH",                 "-cp",                                  "geodeticlength",   "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-geodetic_length", "geod len"], 	# Geodetic length
    ["THICKNESS",                       "-cp",                                  "thickness",        "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-thickness", "geod thick"], 	# Geodetic thickness
    ["MAJOR_AXIS_LENGTH",               "AreaShape_MajorAxisLength",            "major_axis_length",    "majorAxisLen", "-mitk", "-nist", "original_shape_MajorAxisLength", "-radj", "original-major_axis_length", "maj AL"], 	# Major axis length/min BB length
    ["MASS_DISPLACEMENT",               "-cp",                                  "-imea", "-matlab", "-mitk", "-nist", "-pyr", "-radj", "-wc", "mass displ"], 	# Mass displacement
    ["ROI_RADIUS_MAX",                  "AreaShape_MaximumRadius",              "-imea", "-matlab", "-mitk", "-nist", "-pyr", "-radj", "-wc", "max R"], 	# Max radius
    ["ROI_RADIUS_MEDIAN",               "AreaShape_MedianRadius",               "-imea", "-matlab", "-mitk", "-nist", "-pyr", "-radj", "-wc", "med R"], 	# Median radius
    ["ROI_RADIUS_MEAN",                 "AreaShape_MeanRadius",                 "-imea", "-matlab", "-mitk", "-nist", "-pyr", "-radj", "-wc", "mean R"], 	# Mean radius
    ["-nyx",                            "-cp",                                  "-imea", "-matlab", "-mitk", "-nist", "-pyr", "-radj", "-wc", "mesh surf"],  # Mesh surface
    ["MINOR_AXIS_LENGTH",               "AreaShape_MinorAxisLength",            "minor_axis_length",    "minorAxisLen", "-mitk", "-nist", "original_shape_MinorAxisLength", "-radj", "original-minor_axis_length", "minr AL"], 	# Minor axis length/Min BB width
    ["ORIENTATION",                     "AreaShape_Orientation",                "-imea", "orientation", "-mitk", "Feature2DJava_Mode", "-pyr", "-radj", "original-orientation", "orient"], 	# Orientation
    ["PERIMETER",                       "AreaShape_Perimeter",                  "perimeter",    "perimeter", "-mitk", "Feature2DJava_Perimeter", "-pyr", "Shape2D_Perimeter", "original-perimeter", "P"], 	# Perimeter
    ["-PERIMETER_OVER_AREA",           "-cp",                  "-imea",    "-matlab", "-mitk", "-nist", "-pyr", "Shape2D_PerimeterToPixelSurfaceRatio", "-wc", "POA"], 	# Perimeter to pixel area ratio
    ["SOLIDITY",                        "AreaShape_Solidity",                   "-imea", "solidity", "-mitk", "-nist", "-pyr", "-radj", "original-solidity", "solid"], 	# Solidity
    ["-nyx",                            "AreaShape_InertiaTensorEigenvalues_0", "-imea", "-matlab", "-mitk", "-nist", "-pyr", "-radj", "-wc", "ITEV0"], # Inertia tensor eigenvalue features
    ["-nyx",                            "AreaShape_InertiaTensorEigenvalues_1", "-imea", "-matlab", "-mitk", "-nist", "-pyr", "-radj", "-wc", "ITEV1"], # Inertia tensor eigenvalue features
    ["-nyx",                            "AreaShape_InertiaTensor_0_0",          "-imea", "-matlab", "-mitk", "-nist", "-pyr", "-radj", "-wc", "ITEV00"], # Inertia tensor eigenvalue features
    ["-nyx",                            "AreaShape_InertiaTensor_0_1",          "-imea", "-matlab", "-mitk", "-nist", "-pyr", "-radj", "-wc", "IT01"], # Inertia tensor eigenvalue features
    ["-nyx",                            "AreaShape_InertiaTensor_1_0",          "-imea", "-matlab", "-mitk", "-nist", "-pyr", "-radj", "-wc", "IT10"], # Inertia tensor eigenvalue features
    ["-nyx",                            "AreaShape_InertiaTensor_1_1",          "-imea", "-matlab", "-mitk", "-nist", "-pyr", "-radj", "-wc", "IT11"], # Inertia tensor eigenvalue features
    ["-nyx",                            "-cp",                                  "-imea", "-matlab", "-mitk", "-nist", "-pyr", "-radj", "-wc", "Zern SF"], # Zernike shape features

# caliper
    ["STAT_FERET_DIAM_MAX",              "AreaShape_MaxFeretDiameter",           "feret_max",        "-matlab", "-mitk", "-nist", "-pyr", "-radj",               "original-feret_diameter_max", "fer max"], 	# Feret max \diameter
    ["STAT_FERET_DIAM_MEAN",            "-cp",                                  "feret_mean",       "-matlab", "-mitk", "-nist", "-pyr", "-radj",               "original-feret_diameter_mean", "fer mean"], 	# Feret mean \diameter
    ["STAT_FERET_DIAM_MEDIAN",          "-cp",                                  "feret_median",     "-matlab", "-mitk", "-nist", "-pyr", "-radj",               "original-feret_diameter_median", "fer med"], 	# Feret median \diameter
    ["STAT_FERET_DIAM_STDDEV",          "-cp",                                  "feret_std",        "-matlab", "-mitk", "-nist", "-pyr", "-radj",               "original-feret_diameter_std", "fer std"], 	# Feret \diameter STD
    ["-nyx",                            "-cp",                                  "feret_mode",       "-matlab", "-mitk", "-nist", "-pyr", "-radj",               "original-feret_diameter_mode", "fer mode"], 	# Feret \diameter mode
    ["-nyx",                            "-cp",                                  "-imea",            "-matlab", "-mitk", "-nist", "-pyr", "Shape2D_FerretAngle", "original-max_feret_angle", "fer max ang"], 	# Feret max angle
    ["MIN_FERET_ANGLE",                 "-cp",                                  "-imea",            "-matlab", "-mitk", "-nist", "-pyr", "Shape2D_FerretAngle", "original-min_feret_angle", "fer min ang"], 	# Feret min angle
    ["-nyx",                            "-cp",                                  "-imea",            "-matlab", "-mitk", "-nist", "-pyr", "-radj",               "-wc", "fer min coord"], # Feret min coordinates
    ["STAT_FERET_DIAM_MIN",              "AreaShape_MinFeretDiameter",           "feret_min",        "-matlab", "-mitk", "-nist", "-pyr", "-radj",               "original-feret_diameter_min", "fer min"], 	# Feret min \diameter

    ["STAT_MARTIN_DIAM_MAX",            "-cp",                                  "-imea",            "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-martin_length_max", "mar max"], 	# Martin max \diameter
    ["STAT_MARTIN_DIAM_MEAN",           "-cp",                                  "martin_mean",      "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-martin_length_mean", "mar mean"], 	# Martin mean \diameter
    ["STAT_MARTIN_DIAM_MEDIAN",         "-cp",                                  "martin_median",    "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-martin_length_median", "mar med"], 	# Martin median \diameter
    ["STAT_MARTIN_DIAM_MIN",            "-cp",                                  "martin_min",       "-matlab", "-mitk", "-nist", "-pyr", "-radj", " original-martin_length_min", "mar min"], 	# Martin min \diameter
    ["STAT_MARTIN_DIAM_MODE",           "-cp",                                  "martin_mode",      "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-martin_length_mode", "mar mode"], 	# Martin \diameter mode
    ["STAT_MARTIN_DIAM_STDDEV",         "-cp",                                  "martin_std",       "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-martin_length_std", "mar std"], 	# Martin \diameter stddev

    ["STAT_NASSENSTEIN_DIAM_MAX",       "-cp",                                  "nassenstein_max",  "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-nassenstein_diameter_max", "nas max"], 	# Nassenstein max \diameter
    ["STAT_NASSENSTEIN_DIAM_MEAN",      "-cp",                                  "nassenstein_mean", "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-nassenstein_diameter_mean", "nas mean"], 	# Nassenstein mean \diameter
    ["STAT_NASSENSTEIN_DIAM_MEDIAN",    "-cp",                                  "nassenstein_median", "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-nassenstein_diameter_median", "nas med"], 	# Nassenstein median \diameter
    ["STAT_NASSENSTEIN_DIAM_MIN",       "-cp",                                  "nassenstein_min",  "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-nassenstein_diameter_min", "nas min"], 	# Nassenstein min \diameter
    ["STAT_NASSENSTEIN_DIAM_MODE",      "-cp",                                  "nassenstein_mode", "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-nassenstein_diameter_mode", "nas mode"], 	# Nassenstein \diameter mode
    ["STAT_NASSENSTEIN_DIAM_STDDEV",    "-cp",                                  "-imea",            "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-nassenstein_diameter_std", "nas std"], 	# Nassenstein \diameter stddev
   
    ["MAXCHORDS_MAX",                   "-cp",                                  "maxchords_max",    "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-maxchords_max", "maxch"], 	# Maxchords max
    ["MAXCHORDS_MEAN",                  "-cp",                                  "maxchords_mean",   "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-maxchords_mean", "maxch mean"], 	# Maxchords mean
    ["MAXCHORDS_MEDIAN",                "-cp",                                  "maxchords_median", "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-maxchords_median", "maxch med"], 	# Maxchords median
    ["MAXCHORDS_MIN",                   "-cp",                                  "maxchords_min",    "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-maxchords_min", "maxch min"], 	# Maxchords min
    ["MAXCHORDS_MODE",                  "-cp",                                  "maxchords_mode",   "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-maxchords_mode", "maxch mode"], 	# Maxchords mode
    ["MAXCHORDS_STDDEV",                "-cp",                                  "maxchords_std",    "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-maxchords_std", "maxch std"], 	# Maxchords stddev
   
    ["ALLCHORDS_MAX",                   "-cp",                                  "allchords_max",    "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-allchords_max", "alch max"], 	# Allchords max
    ["ALLCHORDS_MAX_ANG",               "-cp",                                  "-imea",            "-matlab", "-mitk", "-nist", "-pyr", "-radj", "-wc", "alch max ang"], 	# Allchords max angle
    ["ALLCHORDS_MEAN",                  "-cp",                                  "allchords_mean",   "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-allchords_mean", "alch mean"], 	# Allchords mean
    ["ALLCHORDS_MEDIAN",                "-cp",                                  "allchords_median", "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-allchords_median", "alch med"], 	# Allchords median
    ["ALLCHORDS_MIN",                   "-cp",                                  "allchords_min",    "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-allchords_min", "alch min"], 	# Allchords min
    ["ALLCHORDS_MIN_ANG",               "-cp",                                  "-imea",            "-matlab", "-mitk", "-nist", "-pyr", "-radj", "-wc", "alch min ang"], 	# Allchords min angle
    ["ALLCHORDS_MODE",                  "-cp",                                  "allchords_mode",   "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-allchords_mode", "alch mode"], 	# Allchords mode
    ["ALLCHORDS_STDDEV",                "-cp",                                  "allchords_std",    "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-allchords_std", "alch std"], 	# Allchords stddev

    # \bf Mesodescriptors \rm
    ["EROSIONS_2_VANISH",               "-cp",                                  "n_erosions",               "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-erosion_pixels", "E2V"], 	# Erosions to vanish
    ["EROSIONS_2_VANISH_COMPLEMENT",    "-cp",                                  "n_erosions_complement",    "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-erosion_complement_pixels", "E2VC"], 	# Eros to vanish compl

    # \bf Microdescriptors \rm
    ["FRACT_DIM_BOXCOUNT",              "-cp",                                  "fractal_dimension_boxcounting_method",     "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-fractal_dimension_box_counting", "FD boxc"], 	# Fractal dim boxcounting
    ["FRACT_DIM_PERIMETER",             "-cp",                                  "fractal_dimension_perimeter_method",       "-matlab", "-mitk", "-nist", "-pyr", "-radj", "original-fractal_dimension_perimeter", "FD P"], 	# Fractal dim perimeter

    #\bf Skeleton features \rm
    ["-nyx",                            "-cp",                                  "-imea", "-matlab", "-mitk", "-nist", "-pyr", "-radj", "-wc", "num T"], # Number of trunks
    ["-nyx",                            "-cp",                                  "-imea", "-matlab", "-mitk", "-nist", "-pyr", "-radj", "-wc", "num NT"], # Num non-trunk objs
    ["-nyx",                            "-cp",                                  "-imea", "-matlab", "-mitk", "-nist", "-pyr", "-radj", "-wc", "bym BE"], # Num branch ends
    ["-nyx",                            "-cp",                                  "-imea", "-matlab", "-mitk", "-nist", "-pyr", "-radj", "-wc", "TSL"], # Total skeleton length

     #\bf 3D shape features \rm
    ["-nyx",                            "-cp",                                  "-imea", "-matlab", "-mitk", "-nist", "-pyr", "Shape2D_SphericalDisproportion", "-wc", "num T"], # Number of trunks   
    ["-nyx",                            "-cp",                                  "-imea", "-matlab", "-mitk", "-nist", "-pyr", "Shape2D_Sphericity", "-wc", "num T"] # Number of trunks   
    ])

Fmap_misc = np.array([
    ["---0", "---1",  "---2",  "---3",  "---4",  "---5",  "---6",  "---7",  "---8", "!image=banner_misc.png"], # banner
    
    # Neighbor features
    ["NUM_NEIGHBORS",               "Neighbors_NumberOfNeighbors_5",        "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "neig N"], # neighbors, number of
    ["PERCENT_TOUCHING",            "Neighbors_PercentTouching_5",          "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "neig PCT"], # neighbors, % touching
    ["CLOSEST_NEIGHBOR1_DIST",      "Neighbors_FirstClosestDistance_5",     "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "neig dst 1"], # neighbors, distance to closest 1st neighbor
    ["CLOSEST_NEIGHBOR1_ANG",       "-cp",                                  "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "neig ang 1"], # neighbors, angle of closest 1st neighbor
    ["CLOSEST_NEIGHBOR2_DIST",      "Neighbors_SecondClosestDistance_5",    "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "neig dst 2"], # neighbors, distance to closest 2nd neighbor
    ["CLOSEST_NEIGHBOR2_ANG",       "Neighbors_AngleBetweenNeighbors_5",    "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "neig ang 2"], # neighbors, angle of closest 2nd neighbor (!)
    ["ANG_BW_NEIGHBORS_MEAN",       "-cp",                                  "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "neig ang mean"], # neighbors, angle between neighbors (mean)
    ["ANG_BW_NEIGHBORS_STDDEV",     "-cp",                                  "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "neig ang std"], # neighbors, angle between neighbors (std)
    ["ANG_BW_NEIGHBORS_MODE",       "-cp",                                  "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "neig ang mode"], # neighbors, angle between neighbors (mode)
    
    # Intensity distribution:
    ["FRAC_AT_D_0",                 "RadialDistribution_FracAtD_intensity_1of4", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "frac@D 1"], # Frac at D
    ["FRAC_AT_D_1",                 "RadialDistribution_FracAtD_intensity_2of4", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "frac@D 2"], # Frac at D
    ["FRAC_AT_D_2",                 "RadialDistribution_FracAtD_intensity_3of4", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "frac@D 3"], # Frac at D
    ["FRAC_AT_D_3",                 "RadialDistribution_FracAtD_intensity_4of4", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "frac@D 4"], # Frac at D
    ["MEAN_FRAC_0",                 "RadialDistribution_MeanFrac_intensity_1of4", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "Mfrac 1"], # Mean frac
    ["MEAN_FRAC_1",                 "RadialDistribution_MeanFrac_intensity_1of4", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "Mfrac 2"], # Mean frac
    ["MEAN_FRAC_2",                 "RadialDistribution_MeanFrac_intensity_1of4", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "Mfrac 3"], # Mean frac
    ["MEAN_FRAC_3",                 "RadialDistribution_MeanFrac_intensity_1of4", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "Mfrac 4"], # Mean frac
    ["RADIAL_CV_0",                 "RadialDistribution_RadialCV_intensity_1of4", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "rad CV 1"], # Radial CV
    ["RADIAL_CV_1",                 "RadialDistribution_RadialCV_intensity_2of4", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "rad CV 2"], # Radial CV
    ["RADIAL_CV_2",                 "RadialDistribution_RadialCV_intensity_3of4", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "rad CV 3"], # Radial CV
    ["RADIAL_CV_3",                 "RadialDistribution_RadialCV_intensity_4of4", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "rad CV 4"], # Radial CV
    ["ZERNIKE2D_Z0",                "RadialDistribution_ZernikeMagnitude_intensity_0_0", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "ZernikeCoefficients()[0]", "ZI 00"], # Zernike 2D, first 10 (!) Also, CP shows magnitude and phase (!)
    ["ZERNIKE2D_Z1",                "RadialDistribution_ZernikeMagnitude_intensity_1_1", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "ZernikeCoefficients()[1]", "ZI 01"], # Zernike 2D
    ["ZERNIKE2D_Z2",                "RadialDistribution_ZernikeMagnitude_intensity_2_0", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "ZernikeCoefficients()[2]", "ZI 02"], # Zernike 2D
    ["ZERNIKE2D_Z3",                "RadialDistribution_ZernikeMagnitude_intensity_2_2", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "ZernikeCoefficients()[3]", "ZI 03"], # Zernike 2D
    ["ZERNIKE2D_Z4",                "RadialDistribution_ZernikeMagnitude_intensity_3_1", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "ZernikeCoefficients()[4]", "ZI 04"], # Zernike 2D
    ["ZERNIKE2D_Z5",                "RadialDistribution_ZernikeMagnitude_intensity_3_3", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "ZernikeCoefficients()[5]", "ZI 05"], # Zernike 2D
    ["ZERNIKE2D_Z6",                "RadialDistribution_ZernikeMagnitude_intensity_4_0", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "ZernikeCoefficients()[6]", "ZI 06"], # Zernike 2D
    ["ZERNIKE2D_Z7",                "RadialDistribution_ZernikeMagnitude_intensity_4_2", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "ZernikeCoefficients()[7]", "ZI 07"], # Zernike 2D
    ["ZERNIKE2D_Z8",                "RadialDistribution_ZernikeMagnitude_intensity_4_4", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "ZernikeCoefficients()[8]", "ZI 08"], # Zernike 2D
    ["ZERNIKE2D_Z9",                "RadialDistribution_ZernikeMagnitude_intensity_5_1", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "ZernikeCoefficients()[9]", "ZI 09"], # Zernike 2D
    ["ZERNIKE2D_Z10",               "RadialDistribution_ZernikeMagnitude_intensity_5_3", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "ZernikeCoefficients()[10]", "ZI 10"], # Zernike 2D	
    ["ZERNIKE2D_Z11",               "RadialDistribution_ZernikeMagnitude_intensity_5_5", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "ZernikeCoefficients()[11]", "ZI 11"], # Zernike 2D		
    ["ZERNIKE2D_Z12",               "RadialDistribution_ZernikeMagnitude_intensity_6_0", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "ZernikeCoefficients()[12]", "ZI 12"], # Zernike 2D		
    ["ZERNIKE2D_Z13",               "RadialDistribution_ZernikeMagnitude_intensity_6_2", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "ZernikeCoefficients()[13]", "ZI 13"], # Zernike 2D		
    ["ZERNIKE2D_Z14",               "RadialDistribution_ZernikeMagnitude_intensity_6_4", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "ZernikeCoefficients()[14]", "ZI 14"], # Zernike 2D		
    ["ZERNIKE2D_Z15",               "RadialDistribution_ZernikeMagnitude_intensity_6_6", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "ZernikeCoefficients()[15]", "ZI 15"], # Zernike 2D		
    ["ZERNIKE2D_Z16",               "RadialDistribution_ZernikeMagnitude_intensity_7_1", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "ZernikeCoefficients()[16]", "ZI 16"], # Zernike 2D		
    ["ZERNIKE2D_Z17",               "RadialDistribution_ZernikeMagnitude_intensity_7_3", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "ZernikeCoefficients()[17]", "ZI 17"], # Zernike 2D		
    ["ZERNIKE2D_Z18",               "RadialDistribution_ZernikeMagnitude_intensity_7_5", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "ZernikeCoefficients()[18]", "ZI 18"], # Zernike 2D		
    ["ZERNIKE2D_Z19",               "RadialDistribution_ZernikeMagnitude_intensity_7_7", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "ZernikeCoefficients()[19]", "ZI 19"], # Zernike 2D		
    ["ZERNIKE2D_Z20",               "RadialDistribution_ZernikeMagnitude_intensity_8_0", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "ZernikeCoefficients()[20]", "ZI 20"], # Zernike 2D		
    ["ZERNIKE2D_Z21",               "RadialDistribution_ZernikeMagnitude_intensity_8_2", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "ZernikeCoefficients()[21]", "ZI 21"], # Zernike 2D		
    ["ZERNIKE2D_Z22",               "RadialDistribution_ZernikeMagnitude_intensity_8_4", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "ZernikeCoefficients()[22]", "ZI 22"], # Zernike 2D		
    ["ZERNIKE2D_Z23",               "RadialDistribution_ZernikeMagnitude_intensity_8_6", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "ZernikeCoefficients()[23]", "ZI 23"], # Zernike 2D		
    ["ZERNIKE2D_Z24",               "RadialDistribution_ZernikeMagnitude_intensity_8_8", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "ZernikeCoefficients()[24]", "ZI 24"], # Zernike 2D		
    ["ZERNIKE2D_Z25",               "RadialDistribution_ZernikeMagnitude_intensity_9_1", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "ZernikeCoefficients()[25]", "ZI 25"], # Zernike 2D		
    ["ZERNIKE2D_Z26",               "RadialDistribution_ZernikeMagnitude_intensity_9_3", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "ZernikeCoefficients()[26]", "ZI 26"], # Zernike 2D		
    ["ZERNIKE2D_Z27",               "RadialDistribution_ZernikeMagnitude_intensity_9_5", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "ZernikeCoefficients()[27]", "ZI 27"], # Zernike 2D		
    ["ZERNIKE2D_Z28",               "RadialDistribution_ZernikeMagnitude_intensity_9_7", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "ZernikeCoefficients()[28]", "ZI 28"], # Zernike 2D		
    ["ZERNIKE2D_Z29",               "RadialDistribution_ZernikeMagnitude_intensity_9_9", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "ZernikeCoefficients()[29]", "ZI 29"], # Zernike 2D	

    ["ZERNIKE2D_Z0",                "-AreaShape_Zernike_0_0", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "SZ 00"], # Zernike 2D, first 10 (!) Also, CP shows magnitude and phase (!)
    ["ZERNIKE2D_Z1",                "-AreaShape_Zernike_1_1", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "SZ 01"], # Zernike 2D
    ["ZERNIKE2D_Z2",                "-AreaShape_Zernike_2_0", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "SZ 02"], # Zernike 2D
    ["ZERNIKE2D_Z3",                "-AreaShape_Zernike_2_2", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "SZ 03"], # Zernike 2D
    ["ZERNIKE2D_Z4",                "-AreaShape_Zernike_3_1", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "SZ 04"], # Zernike 2D
    ["ZERNIKE2D_Z5",                "-AreaShape_Zernike_3_3", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "SZ 05"], # Zernike 2D
    ["ZERNIKE2D_Z6",                "-AreaShape_Zernike_4_0", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "SZ 06"], # Zernike 2D
    ["ZERNIKE2D_Z7",                "-AreaShape_Zernike_4_2", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "SZ 07"], # Zernike 2D
    ["ZERNIKE2D_Z8",                "-AreaShape_Zernike_4_4", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "SZ 08"], # Zernike 2D
    ["ZERNIKE2D_Z9",                "-AreaShape_Zernike_5_1", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "SZ 09"], # Zernike 2D
    ["ZERNIKE2D_Z10",               "-AreaShape_Zernike_5_3", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "SZ 10"], # Zernike 2D	
    ["ZERNIKE2D_Z11",               "-AreaShape_Zernike_5_5", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "SZ 11"], # Zernike 2D		
    ["ZERNIKE2D_Z12",               "-AreaShape_Zernike_6_0", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "SZ 12"], # Zernike 2D		
    ["ZERNIKE2D_Z13",               "-AreaShape_Zernike_6_2", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "SZ 13"], # Zernike 2D		
    ["ZERNIKE2D_Z14",               "-AreaShape_Zernike_6_4", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "SZ 14"], # Zernike 2D		
    ["ZERNIKE2D_Z15",               "-AreaShape_Zernike_6_6", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "SZ 15"], # Zernike 2D		
    ["ZERNIKE2D_Z16",               "-AreaShape_Zernike_7_1", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "SZ 16"], # Zernike 2D		
    ["ZERNIKE2D_Z17",               "-AreaShape_Zernike_7_3", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "SZ 17"], # Zernike 2D		
    ["ZERNIKE2D_Z18",               "-AreaShape_Zernike_7_5", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "SZ 18"], # Zernike 2D		
    ["ZERNIKE2D_Z19",               "-AreaShape_Zernike_7_7", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "SZ 19"], # Zernike 2D		
    ["ZERNIKE2D_Z20",               "-AreaShape_Zernike_8_0", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "SZ 20"], # Zernike 2D		
    ["ZERNIKE2D_Z21",               "-AreaShape_Zernike_8_2", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "SZ 21"], # Zernike 2D		
    ["ZERNIKE2D_Z22",               "-AreaShape_Zernike_8_4", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "SZ 22"], # Zernike 2D		
    ["ZERNIKE2D_Z23",               "-AreaShape_Zernike_8_6", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "SZ 23"], # Zernike 2D		
    ["ZERNIKE2D_Z24",               "-AreaShape_Zernike_8_8", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "SZ 24"], # Zernike 2D		
    ["ZERNIKE2D_Z25",               "-AreaShape_Zernike_9_1", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "SZ 25"], # Zernike 2D		
    ["ZERNIKE2D_Z26",               "-AreaShape_Zernike_9_3", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "SZ 26"], # Zernike 2D		
    ["ZERNIKE2D_Z27",               "-AreaShape_Zernike_9_5", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "SZ 27"], # Zernike 2D		
    ["ZERNIKE2D_Z28",               "-AreaShape_Zernike_9_7", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "SZ 28"], # Zernike 2D		
    ["ZERNIKE2D_Z29",               "-AreaShape_Zernike_9_9", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "SZ 29"], # Zernike 2D	



    ["mockwc_GABOR_0",                     "-cp", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "GaborTextures()[0]", "Gab 1"], # Gabor filter bank
    ["mockwc_GABOR_1",                     "-cp", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "GaborTextures()[1]", "Gab 2"], # Gabor filter bank
    ["mockwc_GABOR_2",                     "-cp", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "GaborTextures()[2]", "Gab 3"], # Gabor filter bank
    ["mockwc_GABOR_3",                     "-cp", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "GaborTextures()[3]", "Gab 4"], # Gabor filter bank
    ["mockwc_GABOR_4",                     "-cp", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "GaborTextures()[4]", "Gab 5"], # Gabor filter bank
    ["mockwc_GABOR_5",                     "-cp", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "GaborTextures()[5]", "Gab 6"], # Gabor filter bank
    ["mockwc_GABOR_6",                     "-cp", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "GaborTextures()[6]", "Gab 7"], # Gabor filter bank
    
    # Spatial (raw) moments
    ["SPAT_MOMENT_00",              "AreaShape_SpatialMoment_0_0", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D rm00"], # 
    ["SPAT_MOMENT_01",              "AreaShape_SpatialMoment_0_1", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D rm01"], # 
    ["SPAT_MOMENT_02",              "AreaShape_SpatialMoment_0_2", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D rm02"], # 
    ["SPAT_MOMENT_03",              "AreaShape_SpatialMoment_0_3", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D rm03"], # 
    ["SPAT_MOMENT_10",              "AreaShape_SpatialMoment_1_0", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D rm10"], # 
    ["SPAT_MOMENT_11",              "AreaShape_SpatialMoment_1_1", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D rm11"], # 
    ["SPAT_MOMENT_12",              "AreaShape_SpatialMoment_1_2", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D rm12"], # 
    ["SPAT_MOMENT_13",              "AreaShape_SpatialMoment_1_3", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D rm13"], # 
    ["SPAT_MOMENT_20",              "AreaShape_SpatialMoment_2_0", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D rm20"], # 
    ["SPAT_MOMENT_21",              "AreaShape_SpatialMoment_2_1", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D rm21"], # 
    ["SPAT_MOMENT_22",              "AreaShape_SpatialMoment_2_2", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D rm22"], # 
    ["SPAT_MOMENT_23",              "AreaShape_SpatialMoment_2_3", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D rm23"], # 
    ["SPAT_MOMENT_30",              "-cp", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D raw m30"], # 

    # Central moments
    ["CENTRAL_MOMENT_00",           "AreaShape_CentralMoment_0_0", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D cm00"], # 
    ["CENTRAL_MOMENT_01",           "AreaShape_CentralMoment_0_1", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D cm01"], # 
    ["CENTRAL_MOMENT_02",           "AreaShape_CentralMoment_0_2", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D cm02"], # 
    ["CENTRAL_MOMENT_03",           "AreaShape_CentralMoment_0_3", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D cm03"], # 
    ["CENTRAL_MOMENT_10",           "AreaShape_CentralMoment_1_0", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D cm10"], # 
    ["CENTRAL_MOMENT_11",           "AreaShape_CentralMoment_1_1", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D cm11"], # 
    ["CENTRAL_MOMENT_12",           "AreaShape_CentralMoment_1_2", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D cm12"], # 
    ["CENTRAL_MOMENT_13",           "AreaShape_CentralMoment_1_3", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D cm13"], # 
    ["CENTRAL_MOMENT_20",           "AreaShape_CentralMoment_2_0", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D cm20"], # 
    ["CENTRAL_MOMENT_21",           "AreaShape_CentralMoment_2_1", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D cm21"], # 
    ["CENTRAL_MOMENT_22",           "AreaShape_CentralMoment_2_2", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D cm22"], # 
    ["CENTRAL_MOMENT_23",           "AreaShape_CentralMoment_2_3", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D cm23"], # 
    ["CENTRAL_MOMENT_30",           "-cp", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D cm30"], # 
    ["CENTRAL_MOMENT_31",           "-cp", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D cm31"], # 
    ["CENTRAL_MOMENT_32",           "-cp", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D cm32"], # 
    ["CENTRAL_MOMENT_33",           "-cp", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D cm33"], # 

    # Normalized (standardized) spatial moments
    ["NORM_SPAT_MOMENT_00",         "AreaShape_NormalizedMoment_0_0", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D nrm00"], # 
    ["NORM_SPAT_MOMENT_01",         "AreaShape_NormalizedMoment_0_1", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D nrm01"], # 
    ["NORM_SPAT_MOMENT_02",         "AreaShape_NormalizedMoment_0_2", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D nrm02"], # 
    ["NORM_SPAT_MOMENT_03",         "AreaShape_NormalizedMoment_0_3", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D nrm03"], # 
    ["NORM_SPAT_MOMENT_10",         "AreaShape_NormalizedMoment_1_0", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D nrm10"], # 
    ["NORM_SPAT_MOMENT_11",         "AreaShape_NormalizedMoment_1_1", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D nrm11"], # 
    ["NORM_SPAT_MOMENT_12",         "AreaShape_NormalizedMoment_1_2", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D nrm12"], # 
    ["NORM_SPAT_MOMENT_13",         "AreaShape_NormalizedMoment_1_3", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D nrm13"], # 
    ["NORM_SPAT_MOMENT_20",         "AreaShape_NormalizedMoment_2_0", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D nrm20"], # 
    ["NORM_SPAT_MOMENT_21",         "AreaShape_NormalizedMoment_2_1", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D nrm21"], # 
    ["NORM_SPAT_MOMENT_22",         "AreaShape_NormalizedMoment_2_2", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D nrm22"], # 
    ["NORM_SPAT_MOMENT_23",         "AreaShape_NormalizedMoment_2_3", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D nrm23"], # 
    ["NORM_SPAT_MOMENT_30",         "AreaShape_NormalizedMoment_3_0", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D nrm30"], # 
    ["NORM_SPAT_MOMENT_31",         "AreaShape_NormalizedMoment_3_1", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D nrm31"], # 
    ["NORM_SPAT_MOMENT_32",         "AreaShape_NormalizedMoment_3_2", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D nrm32"], # 
    ["NORM_SPAT_MOMENT_33",         "AreaShape_NormalizedMoment_3_3", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D nrm33"], # 

    # Normalized central moments
    ["NORM_CENTRAL_MOMENT_02",      "-cp", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D ncm02"], # 
    ["NORM_CENTRAL_MOMENT_03",      "-cp", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D ncm03"], # 
    ["NORM_CENTRAL_MOMENT_11",      "-cp", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D ncm11"], # 
    ["NORM_CENTRAL_MOMENT_12",      "-cp", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D ncm12"], # 
    ["NORM_CENTRAL_MOMENT_20",      "-cp", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D ncm20"], # 
    ["NORM_CENTRAL_MOMENT_21",      "-cp", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D ncm21"], # 
    ["NORM_CENTRAL_MOMENT_30",      "-cp", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D ncm30"], # 

    # Hu's moments 1-7 
    ["HU_M1",                       "AreaShape_HuMoment_0", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "Hu 1"], # 
    ["HU_M2",                       "AreaShape_HuMoment_1", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "Hu 2"], # 
    ["HU_M3",                       "AreaShape_HuMoment_2", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "Hu 3"], # 
    ["HU_M4",                       "AreaShape_HuMoment_3", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "Hu 4"], # 
    ["HU_M5",                       "AreaShape_HuMoment_4", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "Hu 5"], # 
    ["HU_M6",                       "AreaShape_HuMoment_5", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "Hu 6"], # 
    ["HU_M7",                       "AreaShape_HuMoment_6", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "Hu 7"], # 

    # Weighted spatial moments
    ["WEIGHTED_SPAT_MOMENT_00",     "-cp", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D wrm00"], # 
    ["WEIGHTED_SPAT_MOMENT_01",     "-cp", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D wrm01"], # 
    ["WEIGHTED_SPAT_MOMENT_02",     "-cp", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D wrm02"], # 
    ["WEIGHTED_SPAT_MOMENT_03",     "-cp", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D wrm03"], # 
    ["WEIGHTED_SPAT_MOMENT_10",     "-cp", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D wrm10"], # 
    ["WEIGHTED_SPAT_MOMENT_11",     "-cp", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D wrm11"], # 
    ["WEIGHTED_SPAT_MOMENT_12",     "-cp", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D wrm12"], # 
    ["WEIGHTED_SPAT_MOMENT_20",     "-cp", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D wrm20"], # 
    ["WEIGHTED_SPAT_MOMENT_21",     "-cp", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D wrm21"], # 
    ["WEIGHTED_SPAT_MOMENT_30",     "-cp", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D wrm30"], # 

    # Weighted central moments
    ["WEIGHTED_CENTRAL_MOMENT_02",  "-cp", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D wcm02"], # 
    ["WEIGHTED_CENTRAL_MOMENT_03",  "-cp", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D wcm03"], # 
    ["WEIGHTED_CENTRAL_MOMENT_11",  "-cp", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D wcm11"], # 
    ["WEIGHTED_CENTRAL_MOMENT_12",  "-cp", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D wcm12"], # 
    ["WEIGHTED_CENTRAL_MOMENT_20",  "-cp", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D wcm20"], # 
    ["WEIGHTED_CENTRAL_MOMENT_21",  "-cp", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D wcm21"], # 
    ["WEIGHTED_CENTRAL_MOMENT_30",  "-cp", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "2D wcm30"], # 

    # Weighted Hu's moments 1-7 
    ["WEIGHTED_HU_M1",  "-cp", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "WHu 1"], # 
    ["WEIGHTED_HU_M2",  "-cp", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "WHu 2"], # 
    ["WEIGHTED_HU_M3",  "-cp", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "WHu 3"], # 
    ["WEIGHTED_HU_M4",  "-cp", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "WHu 4"], # 
    ["WEIGHTED_HU_M5",  "-cp", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "WHu 5"], # 
    ["WEIGHTED_HU_M6",  "-cp", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "WHu 6"], # 
    ["WEIGHTED_HU_M7",  "-cp", "-imea",            "-matlab",  "-mitk",    "-nist",     "-pyr",     "-radj",    "-wc", "WHu 7"] # 
    ])
    

def ingest (Stats, Rnyx, Rother1, Rother2, Rother3, Rother4, Rother5, Rother6, Rother7, Rother8, Fmap, corrMethod):
    h, w = Fmap.shape

    # header
    print (f"{'FEATURE':>40}\t{'CP'}\t{'IMEA'}\t{'MATL'}\t{'MITK'}\t{'NIST'}\t{'PYR'}\t{'RADJ'}\t{'WC'}\t{'USR facing'}")

    # rows are features, columns are software
    for row in range (0,h): 

        # user-facing feature name field. It can be a feature group divider image name - in that case it needs to be output as a dummy statistics line
        altName = Fmap [row, 9]
        if '!' in altName :
            sList = [SPACER, SPACER, SPACER, SPACER, SPACER, SPACER, SPACER, SPACER, altName]
            Stats.loc[len(Stats)] = sList
            print (f"debug\t{altName}")
            continue

        # feature name in ------ Nyxus ------
        f_nyx = Fmap [row, 0]
        if f_nyx[0]=='-':
            continue

        # Nyxus feature is available, so get its vector of feature values
        vNyx = Rnyx [f_nyx]

        # calculate agreement statistics
        r1 = NOTAVAILABLE if Fmap [row, 1][0] == '-' else vNyx.corr (Rother1[Fmap [row, 1]], method=corrMethod) # cp
        r2 = NOTAVAILABLE if Fmap [row, 2][0] == '-' else vNyx.corr (Rother2[Fmap [row, 2]], method=corrMethod) # imea
        r3 = NOTAVAILABLE if Fmap [row, 3][0] == '-' else vNyx.corr (Rother3[Fmap [row, 3]], method=corrMethod) # matlab
        r4 = NOTAVAILABLE if Fmap [row, 4][0] == '-' else vNyx.corr (Rother4[Fmap [row, 4]], method=corrMethod) # mitk
        r5 = NOTAVAILABLE if Fmap [row, 5][0] == '-' else vNyx.corr (Rother5[Fmap [row, 5]], method=corrMethod) # nist
        r6 = NOTAVAILABLE if Fmap [row, 6][0] == '-' else vNyx.corr (Rother6[Fmap [row, 6]], method=corrMethod) # pyr
        r7 = NOTAVAILABLE if Fmap [row, 7][0] == '-' else vNyx.corr (Rother7[Fmap [row, 7]], method=corrMethod) # radj
        r8 = NOTAVAILABLE if Fmap [row, 8][0] == '-' else vNyx.corr (Rother8[Fmap [row, 8]], method=corrMethod) # wc

        # round
        NRO = 4
        r1 = round(r1,NRO); r2 = round(r2,NRO); r3 = round(r3,NRO); r4 = round(r4, NRO); r5 = round(r5,NRO); r6 = round(r6,NRO); r7 = round(r7,NRO); r8=round(r8,NRO)
        if math.isnan(r1) or math.isnan(r2) or math.isnan(r3) or math.isnan(r4) or math.isnan(r5) or math.isnan(r6) or math.isnan(r7) or math.isnan(r8) :
            print (f"---NANs---{f_nyx:>30}\t{r1:g}\t{r2:g}\t{r3:g}\t{r4:g}\t{r5:g}\t{r6:g}\t{r7:g}\t{r8:g}\t{altName}")

            # treat NAN as 0 (unsupported feature by the corresponding software)
            r1 = 0 if math.isnan(r1) else r1
            r2 = 0 if math.isnan(r2) else r2
            r3 = 0 if math.isnan(r3) else r3
            r4 = 0 if math.isnan(r4) else r4
            r5 = 0 if math.isnan(r5) else r5
            r6 = 0 if math.isnan(r6) else r6
            r7 = 0 if math.isnan(r7) else r7
            r8 = 0 if math.isnan(r8) else r8

        # TEMPORARILY discard negatively correlating cells
        discTh = .1
        #???---cp--- r1 = NOTAVAILABLE if r1 <discTh else r1
        #   r2 = NOTAVAILABLE if r2 <discTh else r2
        #   r3 = NOTAVAILABLE if r3 <discTh else r3
        #   r4 = NOTAVAILABLE if r4 <discTh else r4
        #   r5 = NOTAVAILABLE if r5 <discTh else r5
        #???---PyR--- r6 = NOTAVAILABLE if r6 <discTh else r6
        #???---RJ--- r7 = NOTAVAILABLE if r7 <discTh else r7
        #   r8 = NOTAVAILABLE if r8 <discTh else r8

        # discard rows of all missing correlation (for compactness)
        if r1==NOTAVAILABLE and r2==NOTAVAILABLE and r3==NOTAVAILABLE and r4==NOTAVAILABLE and r5==NOTAVAILABLE and r6==NOTAVAILABLE and r7==NOTAVAILABLE and r8==NOTAVAILABLE:
            continue

        # save
        sList = [r1, r2, r3, r4, r5, r6, r7, r8, altName]
        Stats.loc[len(Stats)] = sList

        print (f"{f_nyx:>40}\t{r1:g}\t{r2:g}\t{r3:g}\t{r4:g}\t{r5:g}\t{r6:g}\t{r7:g}\t{r8:g}\t{altName}")


Result = pd.DataFrame(columns=['cp', 'imea', 'matlab', 'mitk', 'nist', 'pyr', 'radj', 'wc', 'altname'])

ingest (Result, R_nyx, R_cp, R_imea, R_matlab, R_mitk_texture, R_nist, R_pyr, R_radj, R_wc, Fmap_texture, CORRMETHOD)
ingest (Result, R_nyx, R_cp, R_imea, R_matlab, R_mitk_inten, R_nist, R_pyr, R_radj, R_wc, Fmap_intensity, CORRMETHOD)
ingest (Result, R_nyx, R_cp, R_imea, R_matlab, R_mitk_inten, R_nist, R_pyr, R_radj, R_wc, Fmap_shape, CORRMETHOD)
ingest (Result, R_nyx, R_cp, R_imea, R_matlab, R_mitk_inten, R_nist, R_pyr, R_radj, R_wc, Fmap_misc, CORRMETHOD)

Result.to_csv (RESULTFILE, sep=',')
print ("\nnyxus input file", NYXUS_INPUT)
print ("\nresult written to file", RESULTFILE)


