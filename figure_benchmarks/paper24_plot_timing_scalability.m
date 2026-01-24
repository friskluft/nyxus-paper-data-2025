%% === Restricted memory 

thickn = 5; % line width

X = [1 5 10 20 30];
Ytn_ec2 = [11734	9250	8919	8740	8683];	% S = 10K
Ytn_mbp = [25127	19189	18364	17978	17900];	% S = 20K

figure(1);
plot (X(1:length(Ytn_ec2)), Ytn_ec2, 'LineStyle','-', 'LineWidth', thickn, 'Marker', 'o', 'MarkerSize', 9, 'Color', 'blue', 'MarkerEdgeColor', 'black', 'MarkerFaceColor', 'white', 'Displayname', 'time at S=10k');
hold on;
plot (X(1:length(Ytn_mbp)), Ytn_mbp, 'LineStyle','-', 'LineWidth', thickn, 'Marker', 'o', 'MarkerSize', 9, 'Color', 'black', 'MarkerEdgeColor', 'black', 'MarkerFaceColor', 'white', 'Displayname', 'time at S=20k');

xlim ([0 31]);

lgnd = legend ('$ROI \: area \: 10K$','$ROI \: area \: 20K$', 'Location','northeast');
%title(lgnd,'ROI area');
set (lgnd, 'Interpreter','latex', 'FontSize', 30);

%---optional--- set (gca,'TickLabelInterpreter','latex');

axis('square');

grid on;

xlabel ('Available memory, $\times 10^3$ Mb', 'Interpreter','latex', 'FontSize', 30, 'FontName', 'Arsenal')
ylabel ('Time (s)', 'Interpreter','latex', 'FontSize', 30, 'FontName', 'Arsenal')
%????????? set(gca,'FontSize',14);
%set(gcf, 'Position', get(0, 'Screensize'));

%% === Multicore   (timing_multicore.PNG)

thickn = 5; % line width

%#X =		[1		2	3	4	5	6	7	8	9	10	11	12	13	14	15	16];
%#Y1 =	[170	93	89	85	85	85	85	85	85	84	85	85	85	85	85	85];	% N=1k, S=10k
%#Y2 =	[1717	931	896	862	854	853	853	854	856	852	854	854	857	856	860	852];	% N=10k, S=10k

X =			[1		2		4		6		8		10		12		14		16];
Ytn_ec2 =	[1888	1610	1558	1596	1568	1584	1604	1591	1601];
Ytn_mbp =	[2296	2746	475		412		382		377		415		429		436];	% MBP
Ytn_nbhub =	[3836	2432	1755	1659	1440	1347	1338	1367	1274];	% Notebook Hub
Ytn_ec2sa =	[3432	1931	1690	1687	1675	1683	1689	1701	1718];	% EC2 (Samee)
Ysyn1_n10k_s10k = [1717		931		862		853		854		852		854		856		852];	% EC2
Ysyn1_n10k_s1k =	[182	94	50	35	28	25	26	27	28];
n1k_s10k =	[170	93		85		85		85		84		85		85		85];	% EC2
Yn1k_s20k = [670	344	179	128	96	91	85	86	87];
Yn20k_s1k = [361	189	100	69	55	51	52	53	52];

figure(2);
plot (X(1:length(Ytn_ec2)), log(Ytn_ec2), 'Color', 'blue', 'LineStyle','-', 'LineWidth', thickn, 'Marker', 's', 'MarkerSize', 9, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', 'white', 'Displayname', 'time at N=1k, S=10k');
hold on;
plot (X(1:length(Ytn_mbp)), log(Ytn_mbp), 'Color', 'black', 'LineStyle','-', 'LineWidth', thickn, 'Marker', 's', 'MarkerSize', 9, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', 'white', 'Displayname', 'time at N=10k, S=10k');
hold on;
plot (X(1:length(Ytn_nbhub)), log(Ytn_nbhub), 'Color', [.9 .8 .7], 'LineStyle','-', 'LineWidth', thickn, 'Marker', 's', 'MarkerSize', 9, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', 'white', 'Displayname', 'time at N=10k, S=10k');
hold on;
plot (X(1:length(Ytn_ec2sa)), log(Ytn_ec2sa), 'Color', [.6 .7 .8], 'LineStyle','-', 'LineWidth', thickn, 'Marker', 's', 'MarkerSize', 9, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', 'white', 'Displayname', 'time at N=10k, S=10k');
hold on;
plot (X(1:length(Ysyn1_n10k_s10k)), log(Ysyn1_n10k_s10k), 'Color', 'red', 'LineStyle','-', 'LineWidth', thickn, 'Marker', 's', 'MarkerSize', 9, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', 'white', 'Displayname', 'time at N=10k, S=10k');
hold on;
plot (X(1:length(Ysyn1_n10k_s1k)), log(Ysyn1_n10k_s1k), 'Color', [.7 .7 .7], 'LineStyle','-', 'LineWidth', thickn, 'Marker', 's', 'MarkerSize', 9, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', 'white', 'Displayname', 'time at N=10k, S=10k');
hold on;
plot (X(1:length(n1k_s10k)), log(n1k_s10k), 'Color', 'green', 'LineStyle','-', 'LineWidth', thickn, 'Marker', 's', 'MarkerSize', 9, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', 'white', 'Displayname', 'time at N=10k, S=10k');
hold on;
plot (X(1:length(Yn1k_s20k)), log(Yn1k_s20k), 'Color', [1. .674 0], 'LineStyle','-', 'LineWidth', thickn, 'Marker', 's', 'MarkerSize', 9, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', 'white', 'Displayname', 'time at N=10k, S=10k');
hold on;
plot (X(1:length(Yn20k_s1k)), log(Yn20k_s1k), 'Color', 'cyan', 'LineStyle','-', 'LineWidth', thickn, 'Marker', 's', 'MarkerSize', 9, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', 'white', 'Displayname', 'time at N=10k, S=10k');

%xlim ([0 17]);
set(gca,'XLim',[0 17],'XTick',[0:1:17]);	% https://www.mathworks.com/matlabcentral/answers/344984-how-to-change-number-of-ticks-tick-position-and-value-on-plot

% {
%on EC2: lgnd = legend('$N=1K, S=10K$','$N=10K, S=10K$', 'Location','northeast');
lgnd2 = legend ('EC2/8CPU Tissuenet', ...
    'MBP Tissuenet', ...
    'Notebook Hub Tissuenet', ...
    'EC2/4CPU Tissuenet', ...
    'EC2 synthetic $^{N10k}_{S10k}$', ...
    'MBP synthetic $^{N10k}_{S1k}$', ...
    'EC2 synthetic $^{N=1k}_{S=10k}$', ...
    'MBP synthetic $^{N1k}_{S20k}$', ...
    'MBP synthetic $^{N=20k}_{S=1k}$', ...
    'Location','bestoutside');
% }

%??? 3 ???????????    set (gca,'TickLabelInterpreter','latex');

%--opt-- axis('square');

grid on;

FONT = 'AvantGarde';
FONTSIZE = 10;
FONTSIZE_LEGEND = FONTSIZE * 1.5; 
FONTSIZE_YLABEL = FONTSIZE * 3;
FONTSIZE_AXIS = FONTSIZE * 4; % Xlarge:3, XXlarge:4

set (lgnd2, 'Interpreter','latex', 'FontSize', FONTSIZE_LEGEND);
xlabel ('Number of threads', 'FontSize', FONTSIZE_YLABEL, 'FontName', FONT) % 'Interpreter','latex'
ylabel ('Log time (s)', 'FontSize', FONTSIZE_YLABEL, 'FontName', FONT) % 'Interpreter','latex'
set (gca,'FontSize', FONTSIZE_AXIS, 'FontName', FONT);
%set(gcf, 'Position', get(0, 'Screensize'));


%% === Scalability   (timing_scalability.PNG)

thickn = 5; 

S = [1 2 3 4 5 6 7 8 9]; 

% ROI S >	100				10^3		10^4		10^5
% n_ROIs V
%----------------------------------------------------------
T_n1E3 =	[2				4			28			341];
T_n1E3G =	[1.4			2.5			15.3		195];	% GPU

%T_n5E3 =	[4				13			112			1783];	% NON
%T_n5E3G =	[25				36			130			1204];	% GPU

T_n1E4 =	[66				46			475			5740];
T_n1E4G =	[71.6			86.13		190.8		2270.61];	% GPU

%T_n5E4 =	[45				136			1178			--];	% NON
%T_n5E4G =	[--			--		--		--];	% GPU

T_n1E5 =	[320			664			5053		33651];	
T_n1E5G =	[1658.1			1254.1		1894.72		11736.0];	% GPU

%---whim--- T_n5E5 =	[1296			3793		29078];

T_TN = [1]; % 83 ROIs
T_D = [0.6]; % 13 ROIs

figure(3);

plot (S(1:length(T_n1E3)), log(T_n1E3), 'Color', [.7 .7 .7], 'LineStyle','-', 'LineWidth', thickn ,...
    'Marker', 'o', 'MarkerSize', 9, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', 'white' );
%plot (S(1:length(T_n1E3)), log(T_n1E3), 'Color', [.7 .7 .7], 'LineStyle','-', 'LineWidth', thickn);
hold on;

%s1 = scatter (S(1:length(T_n1E3)), log(T_n1E3), 50, 'k', '+', 'LineWidth', 2, 'HandleVisibility','off');
%plot (S(1:length(T_n1E3)), log(T_n1E3), 'LineStyle', 'none', 'Marker', 'o', ...
%    'LineWidth', 1, 'MarkerSize', 8, ...
%    'MarkerEdgeColor', 'k', 'MarkerFaceColor', 'r', 'HandleVisibility','off');
hold on;

plot (S(1:length(T_n1E3G)), log(T_n1E3G), 'LineStyle','-', 'LineWidth', thickn, 'Color', [.0 .5 .9] ,...
    'Marker', '+', 'MarkerSize', 9, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', 'white');
hold on;
%s1G = scatter (S(1:length(T_n1E3G)), log(T_n1E3G), 50, 'b', '+', 'LineWidth', 2);
%hold on;

plot (S(1:length(T_n1E4)), log(T_n1E4), 'LineStyle','-', 'LineWidth', thickn,  'Color', [.7 .7 .7] ,...
    'Marker', 'x', 'MarkerSize', 9, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', 'white');
hold on;
%s2 = scatter (S(1:length(T_n1E4)), log(T_n1E4), 50, 'k', 'o', 'LineWidth', 2);
%hold on;

plot (S(1:length(T_n1E4G)), log(T_n1E4G), 'LineStyle','-', 'LineWidth', thickn,  'Color', [.0 .5 .9] ,...
    'Marker', 's', 'MarkerSize', 9, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', 'white');
hold on;
%s2G = scatter (S(1:length(T_n1E4G)), log(T_n1E4G), 50, 'b', 'o', 'LineWidth', 2);
%hold on;

plot (S(1:length(T_n1E5)), log(T_n1E5), 'LineStyle','-', 'LineWidth', thickn,  'Color', [.7 .7 .7] ,...
    'Marker', '^', 'MarkerSize', 9, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', 'white');
hold on;
%s3 = scatter (S(1:length(T_n1E5)), log(T_n1E5), 50, 'k', '>', 'LineWidth', 2);
%hold on;

plot (S(1:length(T_n1E5G)), log(T_n1E5G), 'LineStyle','-', 'LineWidth', thickn,  'Color', [.0 .5 .9] ,...
    'Marker', '*', 'MarkerSize', 9, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', 'white');
hold on;
%s3G = scatter (S(1:length(T_n1E5G)), log(T_n1E5G), 50, 'b', '>', 'LineWidth', 2);
%hold on;


%---whim--- plot (S(1:length(T_n5E5)), log(T_n5E5), 'LineStyle','-', 'LineWidth', thickn,  'Color', [.7 .7 .7]);
%---whim--- hold on;
%---whim--- s4 = scatter (S(1:length(T_n5E5)), log(T_n5E5), 50, 'k', '*', 'LineWidth', 2);

%---Tissuenet
%	plot (S(1:length(T_TN)), log(T_TN), 'LineStyle','-', 'LineWidth', thickn,  'Color', [.7 .7 .7]);
%	hold on;
%	sTN = scatter (S(1:length(T_TN)), log(T_TN), 50, 'k', 'd', 'LineWidth', 2);
%	text(1, log(T_TN), 'Tissuenet')
%
%	T_decathlon13 = ...
%----------

%--- xlim ([0 10^6+10^5]);
%daspect([2 8 1]); %---axis('square');

grid on;

ylim ([0 12]);

% Categorical X-ticks
ax = gca; % important!
ax.XLim = [.9 4.1];
ax.XAxis.TickLabels = {'0', '100', '', '10E3', '', '10E4', '', '10E5', '', '1M', '', '10M'};
%----- ax.YAxis.TickLabels = {'y100', 'y500', 'y1,000', 'y10,000', 'y100,000', 'y1000,000'};

FONT = 'AvantGarde';
FONTSIZE = 10;
FONTSIZE_LEGEND = FONTSIZE * 1.5; 
FONTSIZE_YLABEL = FONTSIZE * 3;
FONTSIZE_AXIS = FONTSIZE * 4; % Xlarge:3, XXlarge:4

set (ax, 'FontSize', FONTSIZE_AXIS, 'fontname', FONT);

%---whim--- legend([s1, s2, s3, s4], {'1K ROI', '10K ROI', '100K ROI', '500K ROI'}, 'Location','southeast');	% BGND https://www.mathworks.com/matlabcentral/answers/489069-creating-a-legend-that-is-unrelated-to-the-plotted-data
%lgnd3 = legend ([s1, s1G, s2, s2G, s3, s3G], {'1K ROI', '2', '10K ROI', '4', '100K ROI', '6'}, 'Location','southeast');	% BGND https://www.mathworks.com/matlabcentral/answers/489069-creating-a-legend-that-is-unrelated-to-the-plotted-data
lgnd3 = legend ('1K ROI', '1K ROI (GPU)', '10K ROI', '1K ROI (GPU)', '100K ROI', '100K ROI (GPU)', 'Location','southeast');	% BGND https://www.mathworks.com/matlabcentral/answers/489069-creating-a-legend-that-is-unrelated-to-the-plotted-data
%set (lgnd3, 'Interpreter','latex');
set (lgnd3, 'Interpreter','latex', 'FontSize', FONTSIZE_LEGEND);

%set(gca,'Interpreter','latex');
%set(gca,'TickLabelInterpreter','latex');

xlabel('ROI area [px]', 'FontSize', FONTSIZE_YLABEL, 'FontName', FONT) % 'Interpreter','latex')
ylabel('Log-time [s]', 'FontSize', FONTSIZE_YLABEL, 'FontName', FONT) % 'Interpreter','latex')

%--- set (gcf, 'units', 'centimeters', 'position', [50, 50, 800, 800])
%set (gca,'FontSize', FONTSIZE, 'FontName', FONT); %set(gca,'FontSize', 16, 'fontname','arsenal');



%% === Groupwise comparison

na = 0; 

%{
Tissuenet-2500, untargeted Nyxus
--------------------
Total time of all feature groups [sec] = 939.713
Break-down:
--------------------
GPU-Gabor/GPU-Gabor/Gabor/#f58231	13.87%	1.3032e+08
GPU-Moments/GPU-Moments/2D moms/#FFFACD	52.16%	4.90183e+08
Intensity/Intensity/Int/#FFFF00	1.05%	9.82906e+06
Morphology/Basic/E/#4aaaea	0.66%	6.21041e+06
Morphology/Chords/Ch/#4aaaea	1.65%	1.55483e+07
Morphology/Contour/C/#4aaaea	0.76%	7.12884e+06
Morphology/Ellipticity/E/#4aaaea	0.64%	6.05348e+06
Morphology/Erosion/Er/#4aaaea	1.45%	1.36561e+07
Morphology/Euler/Eu/#4aaaea	0.67%	6.2801e+06
Morphology/Extrema/Ex/#4aaaea	0.64%	5.9729e+06
Morphology/Feret/F/#4aaaea	0.9%	8.48618e+06
Morphology/Fractal dimension/Fd/#4aaaea	0.65%	6.15142e+06
Morphology/HexPolygEncloInsCircleGeodetLenThickness/HP/#4aaaea	1.99%	1.8697e+07
Morphology/Hull/H/#4aaaea	0.65%	6.12548e+06
Morphology/Martin/M/#4aaaea	0.86%	8.05103e+06
Morphology/Nassenstein/N/#4aaaea	0.86%	8.04416e+06
Morphology/RoiR/R/#4aaaea	1.01%	9.52879e+06
Neighbors/Neighbors/N/#FF69B4	0.36%	3.40102e+06
RDistribution/Rdist/Rd/#00FFFF	1.25%	1.17798e+07
RDistribution/Zernike/Rz/#00FFFF	1.01%	9.47474e+06
Texture/GLCM/GLCM/#bbbbbb	0.98%	9.23099e+06
Texture/GLDM/D/#bbbbbb	1%	9.38752e+06
Texture/GLDZM/DZ/#bbbbbb	1.23%	1.15858e+07
Texture/GLRLM/RL/#bbbbbb	2.12%	1.99007e+07
Texture/GLSZM/SZ/#bbbbbb	7.21%	6.77527e+07
Texture/NGLDM/NG/#bbbbbb	0.91%	8.58404e+06
Texture/NGTDM/NG/#bbbbbb	1.36%	1.27882e+07
scan1/ImgScan1/S1/lightsteelblue	0.01%	50352.7
scan2A/ImgScan2a/S2a/lightsteelblue	1.73%	1.62279e+07
scan2B/ImgScan2b/S2b/lightsteelblue	0.34%	3.23818e+06
scan3/ImgScan3/S3/lightsteelblue	0%	44575.8
--------------------

>>> STARTED >>> 2024-02-01 03:38:37
%}
Y_raw = [211.16	,	na		,	109.9		,	446725.7	,	116		,	151.7		,	41841.5		,	82.4	,	65		% intensity
		1516.47	,	5891.5	,	612			,	na			,	54		,	na			,	15612.5		,	106.4	,	86		% shape
		5333.61	,	na		,	740.3		,	450056.3	,	96		,	875.3		,	62033.7		,	58.3	,	153		% texture
		1266.55	,	15408.5	,	na 			,	na			,	na		,	na			,	na			,	62.5	,	160];	% misc
YLIM = 400;

%{
Tissuenet-2500, targeted Nyxus
--------------------
Total time of all feature groups [sec] = 557.342
Break-down:
--------------------
GPU-Gabor/GPU-Gabor/Gabor/#f58231       20.82%  1.16022e+08
GPU-Moments/GPU-Moments/2D moms/#FFFACD 59.32%  3.30636e+08
Image scan1/ImgScan1/Scan1/lightsteelblue       0.02%   89896.1
Image scan2a/ImgScan2a/Scan2a/lightsteelblue    2.74%   1.52753e+07
Image scan2b/ImgScan2b/Scan2b/lightsteelblue    0.62%   3.47886e+06
Image scan3/ImgScan3/Scan3/lightsteelblue       0%      23022.1
Intensity/Intensity/Int/#FFFF00 0.65%   3.62049e+06
Morphology/Basic/E/#4aaaea      0.15%   819947
Morphology/Chords/Ch/#4aaaea    1.54%   8.55854e+06
Morphology/Contour/C/#4aaaea    0.32%   1.78572e+06
Morphology/Ellipticity/E/#4aaaea        0.11%   590645
Morphology/Erosion/Er/#4aaaea   1.34%   7.44661e+06
Morphology/Euler/Eu/#4aaaea     0.15%   819995
Morphology/Extrema/Ex/#4aaaea   0.11%   604912
Morphology/Feret/F/#4aaaea      0.15%   828720
Morphology/Fractal dimension/Fd/#4aaaea 0.19%   1.04009e+06
Morphology/HexPolygEncloInsCircleGeodetLenThickness/HP/#4aaaea  0.54%   3.03196e+06
Morphology/Hull/H/#4aaaea       0.15%   856001
Morphology/Martin/M/#4aaaea     0.44%   2.45272e+06
Morphology/Nassenstein/N/#4aaaea        0.43%   2.38642e+06
Morphology/RoiR/R/#4aaaea       0.6%    3.33012e+06
Neighbors/Neighbors/N/#FF69B4   0.59%   3.2932e+06
RDistribution/Rdist/Rd/#00FFFF  1.05%   5.86048e+06
RDistribution/Zernike/Rz/#00FFFF        0.69%   3.86109e+06
Texture/GLCM/GLCM/#bbbbbb       0.53%   2.9472e+06
Texture/GLDM/D/#bbbbbb  0.54%   3.02504e+06
Texture/GLDZM/DZ/#bbbbbb        1.17%   6.5318e+06
Texture/GLRLM/RL/#bbbbbb        0.81%   4.51818e+06
Texture/GLSZM/SZ/#bbbbbb        0.86%   4.80405e+06
Texture/NGLDM/NG/#bbbbbb        0.28%   1.57586e+06
Texture/NGTDM/NG/#bbbbbb        3.09%   1.72273e+07
--------------------

>>> STARTED >>> 2024-03-27 18:35:56
>>> FINISHED >>>        2024-03-27 18:46:40
++ date +%s
+ end=1711579600
+ echo 'Experiment:  Elapsed Time: 644 seconds'
Experiment:  Elapsed Time: 644 seconds
+ printf 'JARPATH:  \nDATADIR: /home/kharchenkoa2/work/data/tissuenet \nOUTDIR: /home/kharchenkoa2/work/data/OUT-tissuenet \nSETTINGSFILE:  \nElapsed Time: 644 seconds \n'
%}
		
Y_raw = [...
		211.16	,	na		,	109.9		,	446725.7	,	116		,	151.7		,	41841.5		,	82.4	,	3.62		% intensity
		1516.47	,	5891.5	,	612			,	na			,	54		,	na			,	15612.5		,	106.4	,	34.55		% shape
		5333.61	,	na		,	740.3		,	450056.3	,	96		,	875.3		,	62033.7		,	58.3	,	40.64		% texture
		1266.55	,	15408.5	,	na 			,	na			,	na		,	na			,	na			,	62.5	,	129.04];	% misc
YLIM = 1300;

%{
Decathlon, untargeted Nyxus
%}

cellprofiler = [...
25261		% intensity
181418		% shape
638068		% texture
151519];	% misc

imea = [...
na
43047
na
na];

matlab = [...
5720
6764
6436
na];

mitk = [...
2577
na
2618
na];

nist = [...
5657
6076
5680
na];

pyrad = [...
113150
109522
112865
na];

radj = [...
14790
19143
17123
na];

wc = [...
4541
8343
22139
na];

%{
% untargeted (n_greys=100)
nyxus = [...
1317
1975
3218
2156];
%}

% targeted (n_greys=10)
nyxus = [...
	1327
	1982
	1789
	2167];

Y_raw = [cellprofiler imea matlab mitk nist pyrad radj wc nyxus];
	
% ****** figure ******

% unfortunately
Y = Y_raw; %???????   Y = log(Y_raw) ./ log(2);

% refN is Nyxus[9] in each feature category
ref1 = Y (1,9); 
ref2 = Y (2,9); 
ref3 = Y (3,9); 
ref4 = Y (4,9); 

%?????	Y(1,:) = Y(1,:) ./ ref1 .* 100;
%Y(2,:) = Y(2,:) ./ ref2 .* 100;
%Y(3,:) = Y(3,:) ./ ref3 .* 100;
%Y(4,:) = Y(4,:) ./ ref4 .* 100;
P(1,:) = Y(1,:) ./ ref1 .* 100;
P(2,:) = Y(2,:) ./ ref2 .* 100;
P(3,:) = Y(3,:) ./ ref3 .* 100;
P(4,:) = Y(4,:) ./ ref4 .* 100;
Z = log(P);

YLIM = 10;

TEXTCOLOR = '#000000'; %---blue--->'#2743f6';	% more colors at https://icolorpalette.com 
TEXTCOLOR_ = sscanf(TEXTCOLOR(2:end),'%2x%2x%2x',[1 3])/255; % Convert color code to 1-by-3 RGB array (0~1 each) [https://www.mathworks.com/matlabcentral/answers/458086-how-to-specify-line-color-using-a-hexadecimal-color-code#answer_371931]
FONT = 'AvantGarde';
FONTSIZE = 10;
SW = {'CP' 'IM' 'MT' 'MI' 'NF' 'PR' 'RJ' 'WC' 'NY'};
Clrs = hsv(numel(SW));

figure(4)
bar(Z);
colormap ('acton');

vgap = 2;
for r=1:4
	for c = 1:9
		hold on; 
		x = r + (c - ceil(9/2)) * (1/11);
		if abs(Y(r,c)) ~= Inf
			% software is not N/A
			ht = text(x, Z(r,c) + vgap, [' ' SW{c} ' ' num2str(floor(P(r,c)))], 'VerticalAlignment', 'middle', 'HorizontalAlignment', 'left', 'Color', TEXTCOLOR_, 'fontname', FONT, 'FontSize', FONTSIZE, 'fontweight', 'bold'); 
		else
			% N/A
			ht = text(x, 0 + vgap, [' ' SW{c} ' N/A'], 'VerticalAlignment', 'middle', 'HorizontalAlignment', 'left', 'Color', TEXTCOLOR_, 'fontname', FONT, 'FontSize', FONTSIZE, 'fontweight', 'bold');
		end
		set(ht,'Rotation', 90); 
		set(ht,'FontSize', 14);			
	end
end

%--log T-- daspect([2 10 1]); %--- axis('square');
%grid on;

ylim ([0 YLIM]); %--log T-- ylim ([-2 15]);
ylabel('Relative log-time, %', 'FontSize', FONTSIZE*2, 'fontname', FONT) % 'Interpreter','latex', 
xlabel('Feature group', 'FontSize', FONTSIZE*2, 'fontname', FONT) % 'Interpreter','latex', 

ax = gca; % important!
ax.XAxis.TickLabels = {'intensity', 'shape', 'texture', 'misc'};

%---optional--- set(legend('CellProfiler', 'Imea', 'MATLAB', 'MITK', 'NIST', 'PyRadiomics', 'RadiomicsJ', 'WND-CHARM', 'Nyxus'), 'Interpreter','latex', 'Location', 'bestoutside');

set(ax,'FontSize', FONTSIZE*2, 'fontname', FONT);

