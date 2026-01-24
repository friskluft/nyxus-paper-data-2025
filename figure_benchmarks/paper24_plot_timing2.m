clear all;

na = 0;	% N/A
watchdog = 0;

%{
%BRA

% +-----------+
% | Decathlon |
% +-----------+

% untargeted (n_greys=100)

Y_raw = [...
% cellprofiler  imea    matlab   mitk   nist   pyrad    radj    wc      nyxus
  25261         na      5720     2577   5657   113150   14790   4541    1317 ;  % intensity
  181418        43047   6764     na     6076   109522   19143   8343    1975 ;  % shape
  638068        na      6436     2618   5680   112865   17123   22139   3218 ;  % texture
  151519        na      na       na		na     na       na      na      2156 ;  % misc
];

YLIM = 25000;	% untargeted

% flag defining verical annotation behavior (1 - vertical, 0 - horizontal)
%		CP		IM			MT			MI		NF		PR		RJ			WC				NY
%----------------------------------------------------------------------------------------------------------------------------------------------
verticality = [...
		1		1			1			1		1		1		1			1				1				;	% intensity
		1		1			1			1		1		1		1			1				1				;	% shape
		1		1			1			1		1		1		1			1				1				;	% texture
		1		1			1			1		1		1		1			1				1				;	% misc
	];

% number of features by group
%		CP		IM			MT			MI		NF		PR		RJ			WC				NY
nf = [	15		0			18			46		11		18		19			25				44				;	% intensity
		17+3	13+4+40		19+6		0		0		1		8+1+6+1		33+4+12			34+4+32+8		;	% shape
		13		0			4			43		7		70		78			6				84				;	% texture
		4+7		0			0			0		0		0		0			1+2+1			4+6+1			;	% misc
	];

variantDescr = 'DECATHLON UN*TARGETED fgroupwise_timing_decathlon_untargeted';
watchdog = watchdog+1;

%KET Decatlon-unt
%}

%{
%BRA

% +-----------+
% | Decathlon |
% +-----------+

% targeted (n_greys=10)

nyxus = [...
	1327
	1982
	1789
	2167];

Y_raw = [...
% cellprofiler  imea    matlab   mitk   nist   pyrad    radj    wc      nyxus
  25261         na      5720     2577   5657   113150   14790   4541    1327 ;  % intensity
  181418        43047   6764     na     6076   109522   19143   8343    1982 ;  % shape
  638068        na      6436     2618   5680   112865   17123   22139   1789 ;  % texture
  151519        na      na       na		na     na       na      na      2167 ;  % misc
];

YLIM = 45000;	% targeted

% flag defining verical annotation behavior (1 - vertical, 0 - horizontal)
%		CP		IM			MT			MI		NF		PR		RJ			WC				NY
%----------------------------------------------------------------------------------------------------------------------------------------------
verticality = [...
		1		1			1			1		1		1		1			1				1				;	% intensity
		1		1			1			1		1		1		1			1				1				;	% shape
		1		1			1			1		1		1		1			1				1				;	% texture
		1		1			1			1		1		1		1			1				1				;	% misc
	];

% number of features by group
%		CP		IM			MT			MI		NF		PR		RJ			WC				NY
nf = [	15		0			18			46		11		18		19			25				44				;	% intensity
		17+3	13+4+40		19+6		0		0		1		8+1+6+1		33+4+12			34+4+32+8		;	% shape
		13		0			4			43		7		70		78			6				84				;	% texture
		4+7		0			0			0		0		0		0			1+2+1			4+6+1			;	% misc
	];

variantDescr = 'DECATHLON TARGETED fgroupwise_timing_decathlon_targeted';
watchdog = watchdog+1;

%KET Decatlon-targ
%}

%{
%BRA
% +-------------------------+
% | Tissuenet                   |
% |   (UN-targeted Nyxus) |
% +-------------------------+
%		CP			IM			MT				MI				NF			PR				RJ				WC			NY
%----------------------------------------------------------------------------------------------------------------------------------------------
Y_raw = [211.16	,   na		,	109.9		,	147771 		,	116		,	151.7		,	41841.5		,	82.4	,	65		% intensity
         1516.47 ,  5891.5	,	612			,	na			,	54		,	na			,	15612.5		,	106.4	,	86		% shape
         5333.61 ,  na		,	740.3		,	137333		,	96		,	875.3		,	62033.7		,	58.3	,	153		% texture
         1266.55 ,  15408.5	,	na 			,	na			,	na		,	na			,	na			,	62.5	,	160];	% misc
YLIM = 125000;

% flag defining verical annotation behavior (1 - vertical, 0 - horizontal)
%		CP		IM			MT			MI		NF		PR		RJ			WC				NY
%----------------------------------------------------------------------------------------------------------------------------------------------
verticality = [...
		1		1			1			0		1		1		1			1				1				;	% intensity
		1		1			1			1		1		1		1			1				1				;	% shape
		1		1			1			1		1		1		1			1				1				;	% texture
		1		1			1			1		1		1		1			1				1				;	% misc
	];

variantDescr = 'TISSUENET UN*TARGETED fgroupwise_timing_tissuenet_untargeted';
watchdog = watchdog+1;
%KET Tissuenet-targ
%}

% {
%BRA
% +---------------------+
% | Tissuenet              |
% |   (targeted Nyxus) |
% +---------------------+

%		CP			IM			MT				MI				NF			PR				RJ				WC			NY
%----------------------------------------------------------------------------------------------------------------------------------------------
Y_raw = [...
		211.16	,	na		,	109.9		,	147771		,	116		,	151.7		,	41841.5		,	82.4	,	3.62		% intensity
		1516.47	,	5891.5	,	612			,	na			,	54		,	na			,	15612.5		,	106.4	,	34.55		% shape
		5333.61	,	na		,	740.3		,	137333		,	96		,	875.3		,	62033.7		,	58.3	,	40.64		% texture
		1266.55	,	15408.5	,	na 			,	na			,	na		,	na			,	na			,	62.5	,	129.04];	% misc
YLIM = 1250000;

% flag defining verical annotation behavior (1 - vertical, 0 - horizontal)
%		CP		IM			MT			MI		NF		PR		RJ			WC				NY
%----------------------------------------------------------------------------------------------------------------------------------------------
verticality = [...
		1		1			1			0		1		1		0			1				1				;	% intensity
		1		1			1			1		1		1		1			1				1				;	% shape
		1		1			1			1		1		1		1			1				1				;	% texture
		1		1			1			1		1		1		1			1				1				;	% misc
	];

variantDescr = 'TISSUENET TARGETED fgroupwise_timing_tissuenet_targeted';
watchdog = watchdog+1;
%KET Tissuenet-targ
% }
	
% *-*-*-*-*-*-*-*-*-*-*-* figure *-*-*-*-*-*-*-*-*-*-*-*

% linear or log
Y = Y_raw;

% refN is Nyxus[9] in each feature category
ref1 = Y (1,9); 
ref2 = Y (2,9); 
ref3 = Y (3,9); 
ref4 = Y (4,9); 

hgap = 2;

%{
% linear
YLBL = 'Relative time, %';
P(1,:) = Y(1,:) ./ ref1 .* 100;
P(2,:) = Y(2,:) ./ ref2 .* 100;
P(3,:) = Y(3,:) ./ ref3 .* 100;
P(4,:) = Y(4,:) ./ ref4 .* 100;
Z = P;
vgap = 2;
%}

% {
% log
P(1,:) = Y(1,:) ./ ref1 ;
P(2,:) = Y(2,:) ./ ref2 ;
P(3,:) = Y(3,:) ./ ref3 ;
P(4,:) = Y(4,:) ./ ref4 ;
P = P .* 100;
Z = log(P) ./ log(10); % P = log(P) ./ log(10);
YLIM = max(max(Z)) * 1.35;  % * 120; % Y-limit is set to 110% to accommodate all the annotations
vgap = 0.1;
verticality = ones(size(verticality));	% Fix verticality flag to be all-vertical (it's not needed in log mode)
% }

TEXTCOLOR = '#000000'; %---blue--->'#2743f6';	% more colors at https://icolorpalette.com 
TEXTCOLOR_ = sscanf(TEXTCOLOR(2:end),'%2x%2x%2x',[1 3])/255; % Convert color code to 1-by-3 RGB array (0~1 each) [https://www.mathworks.com/matlabcentral/answers/458086-how-to-specify-line-color-using-a-hexadecimal-color-code#answer_371931]
FONT = 'AvantGarde';
FONTSIZE = 10;
FONTSIZE_ANNOT = 20;
FONTSIZE_YLABEL = FONTSIZE * 3;
FONTSIZE_AXIS = FONTSIZE * 3; % 4
FNT_WEIGHT = 'normal';
SW = {'CP' 'IM' 'MT' 'MI' 'NF' 'PR' 'RJ' 'WC' 'NY'};
Clrs = hsv(numel(SW));

figure(4)
bar(Z);
colormap ('acton');

%------ BGND: https://se.mathworks.com/matlabcentral/answers/272805-tick-labels-in-matlab-2015a
% This is log10 scale in which, for example, Nyxus' 100% is equal to 2 :
yt = [0 1 2 3 4 5 6 7 8 9 10];
% But acc to Nathan's suggestion we need to indicate times of Nyxus timing :
ytl = {'0'; '0.1?'; '1?'; '10?'; '100?'; '1,000?'; '10,000?'; '100,000?'; '1,000,000?'; '10,000,000?'; '100,000,000?'} ;
set (gca, 'YTick',yt, 'YTickLabel',ytl);
%------

for r=1:4
	for c = 1:9
		hold on; 
		x = r + (c - ceil(9/hgap)) * (1/11);
		
		rotang = 90;
		if verticality(r,c) == 0
			rotang = 0;
			x = x + 0.05;
		end
		
		if Y(r,c) ~= 0
			annot = [' ' SW{c} ' ' num2str(sprintf('%0.2f',P(r,c)/100.))]; %-- idea: numbers should show times relative to Nyxus which is 100%, therefore "P/100." ||| This was before Nathan --> num2str(floor(P(r,c)))
			
			% truncated (horizontal) bar's annotation is placed lower 
			z = Z(r,c);
			if z > YLIM
				z = YLIM * 0.98;
				annot = [annot ' (truncated)'];
			end
			
			ht = text(x, z + vgap, annot, 'VerticalAlignment', 'middle', 'HorizontalAlignment', 'left', 'Color', TEXTCOLOR_, 'fontname', FONT, 'FontSize', FONTSIZE_ANNOT, 'fontweight', FNT_WEIGHT); 
		else
			% feature group 'r' is N/A for software 'c'
			ht = text(x, 0 + vgap, [' ' SW{c} ' N/A'], 'VerticalAlignment', 'middle', 'HorizontalAlignment', 'left', 'Color', TEXTCOLOR_, 'fontname', FONT, 'FontSize', FONTSIZE_ANNOT, 'fontweight', FNT_WEIGHT);
		end
		
		set(ht,'Rotation', rotang);
	end
end

%--log T-- daspect([2 10 1]); %--- axis('square');
%grid on;

ylim ([min(yt) YLIM]); %--not using hard minimum like--> ylim ([0 YLIM]) 

% *-*-*-*-*-*-*-*-*-*-*-* FONT SIZE AND NAME *-*-*-*-*-*-*-*-*-*-*-*

ax = gca; % important!
ax.XAxis.TickLabels = {'intensity', 'shape', 'texture', 'misc'};

%---optional--- set(legend('CellProfiler', 'Imea', 'MATLAB', 'MITK', 'NIST', 'PyRadiomics', 'RadiomicsJ', 'WND-CHARM', 'Nyxus'), 'Interpreter','latex', 'Location', 'bestoutside');

set (ax, 'FontSize', FONTSIZE_AXIS, 'fontname', FONT);

% set Y-label font specs AFTER setting up the axes
ty = ylabel ({'fold change slower'}, 'FontSize', FONTSIZE_YLABEL, 'FontName', FONT) % 'Interpreter','latex', 

%---DISABLED---	xlabel('Feature group', 'FontSize', FONTSIZE*2, 'fontname', FONT) % 'Interpreter','latex', 

fprintf (1, '\n\t\twe have just plotted: %s\n\n', variantDescr);
if (watchdog ~= 1)
    fprintf (1, '\n\t\terror: watchdog==%d\n\n', watchdog);
end

