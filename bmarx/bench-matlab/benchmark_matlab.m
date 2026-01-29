% timestamp 1/2
tic

% itemized timing
tottimeInten = 0;
tottimeShape = 0;
tottimeTexture = 0;
 
% Constants:
OFS = 1;          % GLCM P-matrix offset
NEW_NUM_LVL = 100;
 
intDir = '/home/kharchenkoa2/work/data/decathlon/output/int'; % 'c:\work\axle\data\3D-decathlon-mini\int'; % '/home/ec2-user/work/data/tissuenet/int' ;
segDir = '/home/kharchenkoa2/work/data/decathlon/output/seg'; % 'c:\work\axle\data\3D-decathlon-mini\seg'; % '/home/ec2-user/work/data/tissuenet/seg' ;
outfilepath = '/home/kharchenkoa2/work/data/OUT-decathlon/f_decathlon_matlab.csv'; % 'C:\WORK\AXLE\data\OUTPUT\f_decathlon_matlab.csv'; % '/home/ec2-user/work/benchmarks/matlab/OUT1/matlab_features_tissuenet_accuracy.csv';
SLASH = '/';
% d = uigetdir(pwd, 'Select a folder');

ff = fullfile (intDir);
files = dir(ff);
 
oRow = 1;
Out = zeros(1,1);

% progress
t0 = datetime;
 
nf = length(files)
for i=1:nf
	% skip special files
	if strcmp(files(i).name,'.') || strcmp(files(i).name,'..')
		continue;
	end
	
	% slide intensity and segmentation
	I = imread ([intDir SLASH files(i).name]);
	S = imread ([segDir SLASH files(i).name]);
	
	% progress
	t000 = datetime;
	fprintf (1, '%f s\t %f %%\t%s\n', etime(datevec(t000),datevec(t0)), 100*i/nf, [intDir '\' files(i).name]);
	
	% We have enough information to extract shape features
	t1 = datetime; % ~~~itemized time~~~
	Rp = regionprops ('table', S, 'all');
	t2 = datetime; % ~~~itemized time~~~
	tottimeShape = tottimeShape + etime(datevec(t2) , datevec(t1));

	% ROI labels plus zero (intensity representing the background)
	L = unique (S);

	% Kill zero as it's not a valid label
	L(find(L==0)) = [];
	
	for iL=1:length(L)
	   label = L(iL);
	   
	   % progress
	   %	fprintf (1, '\t%d\n', label);
	   	   
	   % Find ROI [il]
	   ROI = S;
	   ROI(find(S~=label)) = 0;

	   % Clip the ROI
	   sz = size(S);
	   [roiRows, roiCols] = ind2sub (sz, find(ROI>0));
	   bbMinY = min (roiRows);
	   bbMaxY = max (roiRows);
	   bbMinX = min (roiCols);
	   bbMaxX = max (roiCols);
	   roiS = ROI (bbMinY : bbMaxY , bbMinX : bbMaxX);
	   roiI = I (bbMinY : bbMaxY , bbMinX : bbMaxX);

	   % 'roiInt' could be clipped from an all-nonzero image. So suppress pixels outside the ROI's mask
	   roiI (find(roiS==0)) = 0;
	   
	   % debug
	   if strcmp(files(i).name , 'BRATS_002_z076_t000.ome.tif') && label==2
		   debugbreak = 1;
	   end

	   %>>>>>> Extract features >>>>>>

	   % 1st column is ROI label
	   oCol = 1;
	   Out (oRow, oCol) = label;
	   oCol = oCol + 1;

	   % grey binning info
	   Out (oRow, oCol) = NEW_NUM_LVL;
	   oCol = oCol + 1;
	   
	   %==== Texture

	   t1 = datetime; % ~~~itemized time~~~
	   
	   % check feasibility to analyze texture
	   U = unique(roiI);
	   if length(U) == 1
		   fprintf (1, '\t\tcannot analyze texture of const intensity ROI\n');
		   continue;
	   end

	   % 0 deg
	   [glcm, SI] = graycomatrix (roiI,'Offset',[0 OFS], 'NumLevels', NEW_NUM_LVL,'GrayLimits',[]);	
	   
	   % display glcm as https://stackoverflow.com/questions/30366208/displaying-gridlines-in-matlab-imagesc-function
	   % figure(1); pcolor(1./glcm); axis image; axis ij; colormap 'gnbu'
	   
	   glcm_dg_0 = graycoprops (glcm,{'all'});
	   % -- save
	   Out (oRow, oCol) = glcm_dg_0.Contrast;
	   Out (oRow, oCol+1) = glcm_dg_0.Correlation;
	   Out (oRow, oCol+2) = glcm_dg_0.Energy;
	   Out (oRow, oCol+3) = glcm_dg_0.Homogeneity;
	   oCol = oCol + 4;

	   % 45 deg
	   [glcm, SI] = graycomatrix (roiI,'Offset',[OFS OFS], 'NumLevels', NEW_NUM_LVL,'GrayLimits',[]);
	   glcm_dg_45 = graycoprops (glcm,{'all'});
	   % -- save
	   Out (oRow, oCol) = glcm_dg_45.Contrast;
	   Out (oRow, oCol+1) = glcm_dg_45.Correlation;
	   Out (oRow, oCol+2) = glcm_dg_45.Energy;
	   Out (oRow, oCol+3) = glcm_dg_45.Homogeneity;
	   oCol = oCol + 4;

	   % 90 deg
	   [glcm, SI] = graycomatrix (roiI,'Offset',[OFS 0], 'NumLevels', NEW_NUM_LVL,'GrayLimits',[]);
	   glcm_dg_90 = graycoprops (glcm,{'all'});
	   % -- save
	   Out (oRow, oCol) = glcm_dg_90.Contrast;
	   Out (oRow, oCol+1) = glcm_dg_90.Correlation;
	   Out (oRow, oCol+2) = glcm_dg_90.Energy;
	   Out (oRow, oCol+3) = glcm_dg_90.Homogeneity;
	   oCol = oCol + 4;

	   % 135 deg
	   [glcm, SI] = graycomatrix (roiI,'Offset',[OFS -OFS], 'NumLevels', NEW_NUM_LVL,'GrayLimits',[]);
	   glcm_dg_135 = graycoprops (glcm,{'all'});
	   % -- save
	   Out (oRow, oCol) = glcm_dg_135.Contrast;
	   Out (oRow, oCol+1) = glcm_dg_135.Correlation;
	   Out (oRow, oCol+2) = glcm_dg_135.Energy;
	   Out (oRow, oCol+3) = glcm_dg_135.Homogeneity;
	   oCol = oCol + 4;

	   % ~~~itemized time~~~
	   t2 = datetime;
	   tottimeTexture = tottimeTexture + etime(datevec(t2) , datevec(t1));

	   %==== Intensity

	   t1 = datetime; % ~~~itemized time~~~

	   % get ahold of the nonzero intensity pixel cloud
	   [Rows, Cols, PixClo] = find (roiI);

	   % entropy
	   f_entro = entropy(PixClo);
	   Out (oRow, oCol) = f_entro;
	   oCol = oCol + 1;

	   % IQR
	   f_iqr = iqr(double(PixClo));
	   Out (oRow, oCol) = f_iqr;
	   oCol = oCol + 1;       

	   % kurtosis
	   f_kurt = kurtosis(double(PixClo));
	   Out (oRow, oCol) = f_kurt;
	   oCol = oCol + 1;

	   % max
	   f_max = max(PixClo);
	   Out (oRow, oCol) = f_max;
	   oCol = oCol + 1;

	   % mean
	   f_mean = mean(PixClo);
	   Out (oRow, oCol) = f_mean;
	   oCol = oCol + 1;

	   % MAD
	   f_mad = mad(double(PixClo));
	   Out (oRow, oCol) = f_mad;
	   oCol = oCol + 1;

	   % median
	   f_median = median(PixClo);
	   Out (oRow, oCol) = f_median;
	   oCol = oCol + 1;

	   % min
	   f_min = min(PixClo);
	   Out (oRow, oCol) = f_min;
	   oCol = oCol + 1;

	   % mode
	   f_mode = mode(PixClo);
	   Out (oRow, oCol) = f_mode;
	   oCol = oCol + 1;

	   % percentiles
	   f_p1 = prctile (PixClo, 1);
	   f_p10 = prctile (PixClo, 10);
	   f_p25 = prctile (PixClo, 25);
	   f_p75 = prctile (PixClo, 75);
	   f_p90 = prctile (PixClo, 90);
	   f_p99 = prctile (PixClo, 99);
	   Out (oRow, oCol) = f_p1;
	   Out (oRow, oCol+1) = f_p10;
	   Out (oRow, oCol+2) = f_p25;
	   Out (oRow, oCol+3) = f_p75;
	   Out (oRow, oCol+4) = f_p90;
	   Out (oRow, oCol+5) = f_p99;
	   oCol = oCol + 6;

	   % range
	   f_range = range(PixClo);
	   Out (oRow, oCol) = f_range;
	   oCol = oCol + 1;

	   % RMS
	   f_rms = rms(PixClo);
	   Out (oRow, oCol) = f_rms;
	   oCol = oCol + 1;

	   % skewness
	   f_skew = skewness(double(PixClo));
	   Out (oRow, oCol) = f_skew;
	   oCol = oCol + 1;                  

	   % stddev
	   f_stddev = std(double(PixClo));
	   Out (oRow, oCol) = f_stddev;
	   oCol = oCol + 1;

	   % std error
	   f_stder = std( double(PixClo) ) / sqrt( length( PixClo ));
	   Out (oRow, oCol) = f_stder;
	   oCol = oCol + 1;       

	   % variance
	   f_var = var(double(PixClo));
	   Out (oRow, oCol) = f_var;
	   oCol = oCol + 1;

	   % ~~~itemized time~~~
	   t2 = datetime;
	   tottimeInten = tottimeInten + etime(datevec(t2) , datevec(t1));

	   %==== Shape
		Out (oRow, oCol) = Rp.Area (iL); 
			oCol = oCol +1;
		Out (oRow, oCol) = Rp.BoundingBox (iL, 1);
			oCol = oCol +1;
		Out (oRow, oCol) = Rp.BoundingBox (iL, 2);
			oCol = oCol +1;
		Out (oRow, oCol) = Rp.BoundingBox (iL, 3);
			oCol = oCol +1;
		Out (oRow, oCol) = Rp.BoundingBox (iL, 4);
			oCol = oCol +1;
		Out (oRow, oCol) = Rp.Centroid (iL, 1);
			oCol = oCol +1;
		Out (oRow, oCol) = Rp.Centroid (iL, 2);
			oCol = oCol +1;
		Out (oRow, oCol) = Rp.ConvexArea (iL);
			oCol = oCol +1;
		Out (oRow, oCol) = Rp.Eccentricity (iL);
			oCol = oCol +1;
		Out (oRow, oCol) = Rp.EquivDiameter (iL);
			oCol = oCol +1;
		Out (oRow, oCol) = Rp.EulerNumber (iL);
			oCol = oCol +1;
		Out (oRow, oCol) = Rp.Extent (iL);
			oCol = oCol +1;
%		Out (oRow, oCol) = Rp.Extrema (iL);
%			oCol = oCol +1;
		Out (oRow, oCol) = Rp.FilledArea (iL);
			oCol = oCol +1;
		Out (oRow, oCol) = Rp.MajorAxisLength (iL);
			oCol = oCol +1;
		Out (oRow, oCol) = Rp.MinorAxisLength (iL);
			oCol = oCol +1;
		Out (oRow, oCol) = Rp.Orientation (iL);
			oCol = oCol +1;
		Out (oRow, oCol) = Rp.Perimeter (iL);
			oCol = oCol +1;
		Out (oRow, oCol) = Rp.PerimeterOld (iL);
			oCol = oCol +1;
		Out (oRow, oCol) = Rp.Solidity (iL);
			oCol = oCol +1;
		
	   %==== save: advance row counter
	   oRow = oRow + 1;

	end
end
 
% save the result
%---No header :( --- csvwrite (outfilepath, Out);
T = array2table (Out) ;
T.Properties.VariableNames = { ...
	'label', 'n_grey_bins', 'GlcmContrast_0', 'GlcmCorrelation_0', 'GlcmEnergy_0', 'GlcmHomogeneity_0',	...
	'GlcmContrast_45', 'GlcmCorrelation_45', 'GlcmEnergy_45', 'GlcmHomogeneity_45',			...
	'GlcmContrast_90', 'GlcmCorrelation_90', 'GlcmEnergy_90', 'GlcmHomogeneity_90',			...
	'GlcmContrast_135', 'GlcmCorrelation_135', 'GlcmEnergy_135', 'GlcmHomogeneity_135',		...
	'entropy', 'IQR', 'kurtosis', 'max', 'mean', 'MAD', 'median', 'min', 'mode', 'P1', 'P10', 'P25', 'P75', 'P90', 'P99', 'range', 'RMS', 'skewness', 'STD', 'stder', 'var', ...
	'area', 'bb1', 'bb2', 'bb3', 'bb4', 'centroidX', 'centroidY', 'convexArea', 'eccentricity', 'equivD', 'eulerNumber', 'extent', 'filledArea', 'majorAxisLen', 'minorAxisLen', 'orientation', 'perimeter', 'perimeterOld', 'solidity' ...
};

writetable (T, outfilepath);

% itemized timing
fprintf (1, 'itemized timing (sec)\tintensity %f\tshape %f\ttexture %f\n', tottimeInten, tottimeShape, tottimeTexture);
 
% timestamp 2/2
toc
 