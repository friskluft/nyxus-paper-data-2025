import numpy as np
from bfio import BioWriter
with BioWriter("dummyimage.tif", max_workers=4, backend='python', X=2000, Y=2000, Z=1, C=1, T=1, dtype=np.uint32) as bw:
	bw[0:2000,0:2000] = np.random.random((2000, 2000))

print ("success")

