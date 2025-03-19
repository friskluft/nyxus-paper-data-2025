#
# Prerequisite: NRRD dataset produced by accuracy_mitk.m
#

def isnum (x):
    try:
        float(x)
        return True
    except:
        return False

import os
import subprocess
import pandas as pd
import pathlib
import datetime

#Timing
t_a = datetime.datetime.now()

# settings
SDIR = "/home/kharchenkoa2/work/data/decathlon-splitroi-nrrd/seg"	# strongly required: ROIs of a single image there! No other slides!
IDIR = "/home/kharchenkoa2/work/data/decathlon-splitroi-nrrd/int"
MITK_EXE_PATH = "/home/kharchenkoa2/work/mitk/MITK-2016.11.99_r5cccf9-linux64/bin/MitkCLGlobalImageFeatures"
outpath = "/home/kharchenkoa2/work/data/OUT-mitk/mitk-output-INTEN.txt"
resultpath = "/home/kharchenkoa2/work/data/OUT-mitk/mitk_accuracy_fo-fon-foh.csv" # Attention! File name must match the features request in 'cline' below

# initialize
AllResult = pd.DataFrame();
Result = pd.DataFrame() #--- (columns=['label'])

# iterate slides
p1 = pathlib.Path (SDIR).glob("*")
files = [f for f in p1 if f.is_file()]

# progress
n_digestedFslides = 0
n_slides = len(files)

for f in files:	

	# progress
	# (slide no.)
	n_digestedFslides = n_digestedFslides + 1
	perc = float(n_digestedFslides) / float(n_slides) * 100.
	# (time)
	t_elapRunning = datetime.datetime.now() - t_a
	#
	print (f'{perc} %\t{t_elapRunning.seconds} s\tfile {f}')

	# get ahold of the ROI file
	chards = os.path.split (f)
	slideName = chards[len(chards) -1]	# the last charde is the slide image name that contains ROI label info
	print ("processing slide", slideName)

	# get ROI's numeric label
	imFnameSplit1 = slideName.split (".")
	imFnameSplit2 = imFnameSplit1[0].split ("_roi")
	label = int (imFnameSplit2[1])
	rowDic = dict (ROI_label=label)

	# extract features from this ROI
	cline = [
		MITK_EXE_PATH,
		"-o"
		, "c:\\work\\axle\\data\\OUTPUT\\mitk-output.txt"
		, "-i", IDIR + "/" + slideName
		, "-m", SDIR + "/" + slideName
		#, "-cooc2"
		#,"-rl"
		#, "-ngld"
		#, "-ngtd"
		#, "-gldz"
		#, "-glsz"	#--- MITK produces no output ---
		,"-fo", "-fon", "-foh"	# matches resultpath="c:\\work\\axle\\data\\OUTPUT\\mitk_accuracy_fo-fon-foh.csv"
	]

	try:
		# BGND: https://stackoverflow.com/questions/13398261/how-to-run-a-subprocess-with-python-wait-for-it-to-exit-and-get-the-full-stdout
		process = subprocess.Popen (cline, shell=True,
							stdout=subprocess.PIPE, 
							stderr=subprocess.PIPE)

		# wait for the process to terminate
		out, err = process.communicate()
		errcode = process.returncode

		# digest the output
		outLines = out.splitlines()
		for bytes_l in outLines:
			l = bytes_l.decode()
			if "::" in l:
				parts = l.split (" - ")
				if len(parts) == 2:
					fName = parts[0].strip()
					fVal = parts[1].strip()

					if len(fName) > 0 and isnum(fVal):

						# get float
						if "." not in fVal:
							fVal = fVal + ".0"
						fFloat = float(fVal)

						# save
						rowDic[fName] = fFloat

						#---DEBUG--- print ("good", fName, fFloat)
					else:
						print ("empty fName or non-numeric fVal=", fVal)
				#---DEBUG--- else:
				#	print ("---weird record---", l)
	except subprocess.CalledProcessError:
		print ("Exception performing feature extraction \nSkipping slide", slideName)
		continue

	# append this dictionary to the d.f.
	Result = pd.DataFrame([rowDic])
	AllResult = pd.concat ([AllResult, Result]);

# sort by numeric ROI label
AllResult.sort_values (by=['ROI_label'], inplace=True)

# finalize
AllResult.to_csv (resultpath, sep=',')

# Timing
t_b = datetime.datetime.now()
t_elap = t_b - t_a
print (t_elap.seconds, 'seconds')
print (t_elap.microseconds, 'microseconds')
