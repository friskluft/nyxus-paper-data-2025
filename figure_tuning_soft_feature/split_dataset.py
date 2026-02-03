import os
import pathlib
import shutil
import splitfolders


def copy_dir_files (taskDir:str, stockDir:str, dstDir:str):
    for root, dirs, files in os.walk (taskDir):   # traverse root directory, and list directories as dirs and files as files
        path = root.split(os.sep)
        print((len(path) - 1) * '---', os.path.basename(root))
        for file in files:
            srcPath = os.path.join (stockDir, file)
            dstPath = os.path.join (dstDir, file)   # *
            print (srcPath, ' => ', dstPath)
            shutil.copyfile (srcPath, dstPath)

# Settings
SRC_INTEN_CABINET =     "/data/tissuenet_v1_split/step0_tissuenet_v1_train_int_fullcabinet"
DST_INTEN_CABINET =     "/data/tissuenet_v1_split/step1_tissuenet_v1_train_int_splitcabinet"

DST_INTEN_FLAT_TRAIN =  "/data/tissuenet_v1_split/step2_tissuenet_v1_train_int_flat_train"
DST_INTEN_FLAT_TEST =   "/data/tissuenet_v1_split/step2_tissuenet_v1_train_int_flat_test"

STOCK_INTEN =         "/data/tissuenet_v1.0.tar/tissuenet_v1.0/v1.0/standard/train/intensity"
STOCK_MASK =         "/data/tissuenet_v1.0.tar/tissuenet_v1.0/v1.0/standard/train/label"

DST_MASK_FLAT_TRAIN =   "/data/tissuenet_v1_split/step3_tissuenet_v1_train_mask_flat_train"
DST_MASK_FLAT_TEST =    "/data/tissuenet_v1_split/step3_tissuenet_v1_train_mask_flat_test"

# Split a dataset (intensities)

if not os.path.isdir(DST_INTEN_CABINET):
    print ("\nDirectory " + DST_INTEN_CABINET + " should exist")
    exit(1)
p1 = pathlib.Path(DST_INTEN_CABINET).glob("*")
files = [f for f in p1 if f.is_file()]
p2 = pathlib.Path(DST_INTEN_CABINET).glob("*")
dirs = [d for d in p2 if d.is_dir()]
if len(files) != 0 or len(dirs) != 0:
    print ("\nDirectory " + DST_INTEN_CABINET + " must be empty")
    exit(1)

splitfolders.ratio(
    SRC_INTEN_CABINET, 
    output=DST_INTEN_CABINET,
    seed=1337, 
    ratio=(.9, 0, .1), 
    group_prefix=None, 
    move=False)

# Flatten the split subsets (intnsities)
# -- DST_INTEN_CABINET+"train" -> DST_INTEN_FLAT_TRAIN
trainRoot = DST_INTEN_CABINET + "/train"
copy_dir_files (taskDir=trainRoot, stockDir=STOCK_INTEN, dstDir=DST_INTEN_FLAT_TRAIN)

# -- DST_INTEN_CABINET+"test" -> DST_INTEN_FLAT_TEST
testRoot = DST_INTEN_CABINET + "/test"
copy_dir_files (taskDir=testRoot, stockDir=STOCK_INTEN, dstDir=DST_INTEN_FLAT_TEST)

# Copy train mask files
copy_dir_files (taskDir=DST_INTEN_FLAT_TRAIN, stockDir=STOCK_MASK, dstDir=DST_MASK_FLAT_TRAIN)

# Copy test mask files
copy_dir_files (taskDir=DST_INTEN_FLAT_TEST, stockDir=STOCK_MASK, dstDir=DST_MASK_FLAT_TEST)
