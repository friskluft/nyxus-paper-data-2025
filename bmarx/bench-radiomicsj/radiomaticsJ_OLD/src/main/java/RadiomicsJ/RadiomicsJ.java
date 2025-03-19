package RadiomicsJ;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashSet;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.Properties;
import java.util.Set;

import javax.swing.JOptionPane;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.ParseException;

import ij.IJ;
import ij.ImagePlus;
import ij.ImageStack;
import ij.WindowManager;
import ij.measure.ResultsTable;
import ij.process.ImageProcessor;
import ij.text.TextPanel;
import ij.text.TextWindow;
import ij.util.DicomTools;

import loci.plugins.BF;

import java.util.Map;
import java.util.List;

import ij.*;

import java.io.*;


public class RadiomicsJ {
	public static void main(String[] args) throws Exception {

		org.apache.commons.cli.Options options = new org.apache.commons.cli.Options();
		options.addOption("i","images",true, "path to images dir(folder)");
		options.addOption("m","masks",true, "path to masks dir(folder)");
		options.addOption("o","output",true, "path to save result location dir(not file). default is user folder.");
		options.addOption("h","help",false, "print usage information.");
		options.addOption("d","debug",false, "debug mode");
		options.addOption("t","test",false, "test mode");
		options.addOption("tdt","test-data-type",true, "test data type, 0:digital_phantom1, 1:ct_sample1");
		options.addOption("f", "features", true, "features to calculate");

		

		CommandLineParser parser = new DefaultParser();
		CommandLine cmd = null;
		try {
			cmd = parser.parse(options, args);
		} catch (ParseException e1) {
			e1.printStackTrace();
			System.exit(0);
		}

		String imgFolderPath = null;
		String maskFolderPath = null;
		String outputDestPath = null;//System.getProperty("user.dir");//default
		String propsPath = "Properties.properties";

		String features;
		
		if(cmd.hasOption("i") || cmd.hasOption("images")){
			imgFolderPath = cmd.getOptionValue("images");
		}
		if(cmd.hasOption("m") || cmd.hasOption("masks")){
			maskFolderPath = cmd.getOptionValue("masks");
		}
		if(cmd.hasOption("o") || cmd.hasOption("output")){
			outputDestPath = cmd.getOptionValue("output");
			if(outputDestPath == null || outputDestPath.replace("　","").trim().length()==0) {
				outputDestPath = System.getProperty("user.dir");
			}
		}

		File imgDir = null;
		File maskDir = null;
		
		imgDir = new File(imgFolderPath);
		maskDir = new File(maskFolderPath);
		if(imgDir.isDirectory() && maskDir.isDirectory()) {
			if (imgDir.listFiles().length != maskDir.listFiles().length) {
				System.out.println("Sorry, can not read correctly image and mask file pairs.");
				System.out.println(
						"Please check input images and masks, Are these same size(same number of slices) ?? (or, contained no need files ?)");
				System.out.println(
						imgDir.listFiles().length + " images, " + maskDir.listFiles().length + " masks found.");
				System.exit(0);
			}
		} else {
			System.out.println("-m and -i must both be directories");
		}


		if (cmd.hasOption("f") || cmd.hasOption("features")) {

			features = cmd.getOptionValue("features");

		} else {
			features = "ALL";
		}
		
		FileReader reader = null;
		FileWriter writer = null;

		File props = new File(propsPath);
		
		try {
			props.createNewFile();

			reader = new FileReader(propsPath);
			writer = new FileWriter(propsPath);

			Properties p = new Properties();

			p.load(reader);

			p.setProperty("BOOL_force2D", "1");

			p.setProperty("BOOL_enableGLRLM", "0");
			p.setProperty("BOOL_enableMorphological", "0");
			p.setProperty("BOOL_enableGLDZM", "0");
			p.setProperty("BOOL_enableNGLDM", "0");
			p.setProperty("BOOL_enableGLCM", "0");
			p.setProperty("BOOL_enableShape2D", "0");
			p.setProperty("BOOL_enableIntensityBasedStatistics", "0");
			p.setProperty("BOOL_enableGLSZM", "0");
			p.setProperty("BOOL_enableIntensityHistogram", "0");
			p.setProperty("BOOL_enableIntensityVolumeHistogram", "0");
			p.setProperty("BOOL_enableOperationalInfo", "0");
			p.setProperty("BOOL_enableDiagnostics", "0");
			p.setProperty("BOOL_enableFractal", "0");
			p.setProperty("BOOL_enableNGTDM", "0");
			p.setProperty("BOOL_enableLocalIntensityFeatures", "0");

			List<String> featuresList = Arrays.asList(features.split(","));

			for (String feature: featuresList) {

				if (feature.equals("ALL") || feature.equals("*ALL*")) {
					p.setProperty("BOOL_enableGLCM", "1");
					p.setProperty("BOOL_enableGLRLM", "1");
					p.setProperty("BOOL_enableMorphological", "1");
					p.setProperty("BOOL_enableGLDZM", "1");
					p.setProperty("BOOL_enableNGLDM", "1");
					p.setProperty("BOOL_enableShape2D", "1");
					p.setProperty("BOOL_enableIntensityBasedStatistics", "1");
					p.setProperty("BOOL_enableGLSZM", "1");
					p.setProperty("BOOL_enableIntensityHistogram", "1");
					//p.setProperty("BOOL_enableIntensityVolumeHistogram", "1");
					//p.setProperty("BOOL_enableOperationalInfo", "1");
					p.setProperty("BOOL_enableDiagnostics", "1");
					p.setProperty("BOOL_enableFractal", "1");
					p.setProperty("BOOL_enableNGTDM", "1");
					p.setProperty("BOOL_enableLocalIntensityFeatures", "1");

				} else if (feature.equals("GLCM") || feature.equals("*GLCM*")) {

					p.setProperty("BOOL_enableGLCM", "1");

				} else if (feature.equals("GLRLM") || feature.equals("*GLRLM*")) {

					p.setProperty("BOOL_enableGLRLM", "1");

				} else if (feature.equals("Morphological") || feature.equals("*Morphological*")) {

					p.setProperty("BOOL_enableMorphological", "1");

				} else if (feature.equals("GLDZM") || feature.equals("*GLDZM*")) {

					p.setProperty("BOOL_enableGLDZM", "1");

				} else if (feature.equals("NGLDM") || feature.equals("*NGLDM*")) {

					p.setProperty("BOOL_enableNGLDM", "1");

				} else if (feature.equals("Shape2D") || feature.equals("*Shape2D*")) {

					p.setProperty("BOOL_enableShape2D", "1");

				} else if (feature.equals("IntensityBasedStatistics") || feature.equals("*IntensityBasedStatistics*")) {

					p.setProperty("BOOL_enableIntensityBasedStatistics", "1");

				} else if (feature.equals("GLSZM") || feature.equals("*GLSZM*")) {

					p.setProperty("BOOL_enableGLSZM", "1");

				} else if (feature.equals("IntensityHistogram") || feature.equals("*IntensityHistogram*")) {

					p.setProperty("BOOL_enableIntensityHistogram", "1");

				} else if (feature.equals("IntensityVolumeHistogram") || feature.equals("*IntensityVolumeHistogram*")) {

					p.setProperty("BOOL_enableIntensityVolumeHistogram", "1");

				} else if (feature.equals("OperationalInfo") || feature.equals("*OperationalInfo*")) {

					p.setProperty("BOOL_enableOperationalInfo", "1");
 
				} else if (feature.equals("Diagnostics") || feature.equals("*Diagnostics*")) {

					p.setProperty("BOOL_enableDiagnostics", "1");

				} else if (feature.equals("Fractal") || feature.equals("*Fractal*")) {

					p.setProperty("BOOL_enableFractal", "1");

				} else if (feature.equals("NGTDM") || feature.equals("*NGTDM*")) {

					p.setProperty("BOOL_enableNGTDM", "1");

				} else if (feature.equals("LocalIntensityFeatures") || feature.equals("*LocalIntensityFeatures*")) {

					p.setProperty("BOOL_enableLocalIntensityFeatures", "1");

				} else {

					throw new Exception("Invalid feature group " + feature + ".");

				}

			}

			p.store(writer, "write file");

			writer.close();

		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		} 
		int i = 0;

		File[] imgFiles = imgDir.listFiles();
		for(File file: maskDir.listFiles()) {

			ImagePlus mask = BF.openImagePlus(file.getAbsolutePath())[0];

			float[][] arr = mask.getProcessor().getFloatArray();

			Integer[] ROIs = getUnique(arr);
			


			for(Integer ROI: ROIs){
				if(ROI == 0) continue;
				//System.out.print("ROI: ");
				//System.out.println(ROI);
				FileInputStream in = new FileInputStream("Properties.properties");
				Properties props2 = new Properties();
				props2.load(in);
				in.close();

				FileOutputStream out = new FileOutputStream("Properties.properties");
				props2.setProperty("INT_label", Integer.toString(ROI));
				props2.store(out, null);
				out.close();

				String maskPath = file.getAbsolutePath();
				String imgPath = imgFiles[i].getAbsolutePath();

				String[] arguments = {"-s", propsPath, "-m", maskPath, "-i", imgPath, "-o", outputDestPath}; 

				_main(arguments);

			}

			++i;
		}
		System.exit(0);

		/* 
		System.out.println("");
		for(String str: args){
			System.out.print(str);
			System.out.print(" ");
		}
		System.out.println("");
		*/

		

		//_main(args);
	}
	/**
	 * 
	 * @param args
	 */
	public static void _main(String[] args) {
		
		org.apache.commons.cli.Options options = new org.apache.commons.cli.Options();
		options.addOption("i","images",true, "path to images dir(folder)");
		options.addOption("m","masks",true, "path to masks dir(folder)");
		options.addOption("o","output",true, "path to save result location dir(not file). default is user folder.");
		options.addOption("s","settings",true, "path to setting file(.properties)");
		options.addOption("h","help",false, "print usage information.");
		options.addOption("d","debug",false, "debug mode");
		options.addOption("t","test",false, "test mode");
		options.addOption("tdt","test-data-type",true, "test data type, 0:digital_phantom1, 1:ct_sample1");
		
		CommandLineParser parser = new DefaultParser();
		CommandLine cmd = null;
		try {
			cmd = parser.parse(options, args);
		} catch (ParseException e1) {
			e1.printStackTrace();
			System.exit(0);
		}
		
		boolean debug = false;
		boolean testMode = false;
		String imgFolderPath = null;
		String maskFolderPath = null;
		String outputDestPath = null;//System.getProperty("user.dir");//default
		String propFilePath = null;//settings file
		
		if(cmd.hasOption("h") || cmd.hasOption("help")) {
			HelpFormatter formatter = new HelpFormatter();
			formatter.printHelp("RadiomicsJ", options);
			System.exit(0);
		}
		if(cmd.hasOption("i") || cmd.hasOption("images")){
			imgFolderPath = cmd.getOptionValue("images");
		}
		if(cmd.hasOption("m") || cmd.hasOption("masks")){
			maskFolderPath = cmd.getOptionValue("masks");
		}
		if(cmd.hasOption("o") || cmd.hasOption("output")){
			outputDestPath = cmd.getOptionValue("output");
			if(outputDestPath == null || outputDestPath.replace("　","").trim().length()==0) {
				outputDestPath = System.getProperty("user.dir");
			}
		}
		if(cmd.hasOption("s") || cmd.hasOption("settings")){
			propFilePath = cmd.getOptionValue("settings");
		}
		if(cmd.hasOption("d") || cmd.hasOption("debug")){
			debug = true;
		}
		if(cmd.hasOption("t") || cmd.hasOption("test")){
			testMode = true;
		}
		if(cmd.hasOption("tdt") || cmd.hasOption("test-data-type")){
			String tdt = cmd.getOptionValue("tdt");
			tdt = tdt.replace(" ", "").replace("　", "");
			if(tdt != null && tdt.length()!=0) {
				try {
					testDataType = Integer.parseInt(tdt);
				}catch(NumberFormatException e) {
					//do nothing
				}
			}
		}
		
		if(imgFolderPath == null || maskFolderPath == null) {
			if(!testMode) {
				System.out.println("Sorry, can not read image or mask folders.");
				System.out.println("Please check input paths,");
				System.exit(0);
			}
		}
		
		File imgDir = null;
		File maskDir = null;
		if(!testMode) {
			imgDir = new File(imgFolderPath);
			maskDir = new File(maskFolderPath);
			if(imgDir.isDirectory() && maskDir.isDirectory()) {
				if (imgDir.listFiles().length != maskDir.listFiles().length) {
					System.out.println("Sorry, can not read correctly image and mask file pairs.");
					System.out.println(
							"Please check input images and masks, Are these same size(same number of slices) ?? (or, contained no need files ?)");
					System.out.println(
							imgDir.listFiles().length + " images, " + maskDir.listFiles().length + " masks found.");
					System.exit(0);
				}
			}
		}
		
		RadiomicsJ radiomics = new RadiomicsJ();
		radiomics.setDebug(debug);
		radiomics.loadSettings(propFilePath);
		
		if(!testMode) {
			try {

				ResultsTable res = radiomics.execute(imgDir, maskDir, RadiomicsJ.targetLabel);
				if (res != null) {
					//System.out.println(RadiomicsJ.resultWindowTitle);
					mimicShow(res, RadiomicsJ.resultWindowTitle);
					
					if(outputDestPath !=null) {
						if(outputDestPath.endsWith(".csv")) {
							//appendSave(outputDestPath, res);
							res.save(outputDestPath);
							System.out.println("finish calculation, result save to " + outputDestPath);
						}else {
							DateTimeFormatter dtf = DateTimeFormatter.ofPattern("yyyyMMddHHmmssSSS");  
							LocalDateTime now = LocalDateTime.now();  
							String timeStamp = dtf.format(now);
							File outDest = new File(outputDestPath);
							if(!outDest.exists()) {
								outDest.mkdirs();
							}
							res.save(outDest.getAbsolutePath() + File.separator + "RadiomicsFeatures-"+timeStamp+".csv");
							System.out.println("finish calculation, result save to " + outDest.getAbsolutePath() + File.separator + "RadiomicsFeatures-"+timeStamp+".csv");
						}
					}
				}else {
					JOptionPane.showMessageDialog(null, "RadiomicsJ can not perform feature extraction. Please check image, mask and settings.");
				}
			} catch (Exception e) {
				e.printStackTrace();
				System.exit(0);
			}
		}else {
			ImagePlus imp = null;
			ImagePlus mask = null;
			if(testDataType == 0) {
				ImagePlus[] ds = TestDataLoader.digital_phantom1();
				imp = ds[0];
				mask = ds[1];
			}else if(testDataType == 1) {
				ImagePlus[] ds = TestDataLoader.sample_ct1();
				imp = ds[0];
				mask = ds[1];
			}else if(testDataType == 2) {
				ImagePlus[] ds = TestDataLoader.validationDataAt("001", "PET");
				imp = ds[0];
				mask = ds[1];
			}
			try {
				ResultsTable res = radiomics.execute(imp, mask, RadiomicsJ.targetLabel);
				if(res != null) {
					//res.show(resultWindowTitle);
				}
				if (res != null && outputDestPath != null && outputDestPath.length()!=0) {
					res.save(outputDestPath + File.separator + "RadiomicsFeatures.csv");
				}
			} catch (Exception e) {
				e.printStackTrace();
				System.exit(0);
			}
		}
	}

	public static boolean appendSave(String path, ResultsTable res) {
		try {
			saveAs(path, res);
			return true;
		} catch (IOException e) {
			char delimiter = '\t';
			IJ.error("Save As>Results", ""+"Error saving results:\n   "+e.getMessage());
			return false;
		}
	}


	public static void saveAs(String path, ResultsTable res) throws IOException {

		boolean csv = path.endsWith(".csv") || path.endsWith(".CSV");
		char delimiter = csv?',':'\t';
		PrintWriter pw = null;
		FileOutputStream fos = new FileOutputStream(path);
		BufferedOutputStream bos = new BufferedOutputStream(fos);
		pw = new PrintWriter(bos);
		boolean saveShowRowNumbers = res.showRowNumbers();
		if (Prefs.dontSaveRowNumbers)	
			res.showRowNumbers(false);

		boolean quoteCommas = csv?true:false;
		for (int i=0; i<res.size(); i++)
			pw.println(res.getRowAsString(i));
		quoteCommas = false;
		boolean showRowNumbers = saveShowRowNumbers;
		pw.close();
		delimiter = '\t';
	}

	public static void mimicShow(ResultsTable res, String windowTitle) {
		
		String tableHeadings = res.getColumnHeadings();		
		TextPanel tp = null;
		boolean newWindow = false;
		boolean cloneNeeded = false;
		if (windowTitle.equals("Results")) {
			
		} else {
			java.awt.Frame frame = WindowManager.getFrame(windowTitle);
			TextWindow win;
			if (frame!=null && frame instanceof TextWindow) {
				win = (TextWindow)frame;
				if (win!=null) {
					win.toFront();
					WindowManager.setWindow(frame);
				}
			} else {
				int chars = Math.max(res.size()>0?res.getRowAsString(0).length():15, res.getColumnHeadings().length());
				int width = 100 + chars*10;
				if (width<180) width=180;
				if (width>700) width=700;

				int height = 300;
				if (res.size()>15) height = 400;
				if (res.size()>30 && width>300) height = 500;
				win = new TextWindow(windowTitle, "", width, height);
				cloneNeeded = true;
			}
			tp = win.getTextPanel();
			tp.setColumnHeadings(tableHeadings);
			newWindow = tp.getLineCount()==0;
		}
		tp.setResultsTable(cloneNeeded?(ResultsTable)res.clone():res);
		//int n = res.size();
		//if (n>0) {
			//if (tp.getLineCount()>0) tp.clear();
		//	for (int i=0; i<n; i++) {}
				//tp.appendWithoutUpdate(res.getRowAsString(i));
			//tp.updateDisplay();
		//}
		//if (newWindow) tp.scrollToTop();
	}

	public static Integer[] getUnique(float[][] matrix) {
		Map<Float, Integer> map = new LinkedHashMap<>();
	
		for (float[] row : matrix)
			for (float col : row)
				map.put(col, map.getOrDefault(col, 0) + 1);
	
		List<Integer> unique = new ArrayList<>();
	
		for (Map.Entry<Float, Integer> entry : map.entrySet())
			//if (entry.getValue() == 1)
			unique.add(Math.round(entry.getKey()));
	
		return unique.toArray(new Integer[unique.size()]);
	}
	
	/**
	 * radiomicsj version
	 */
	static String version = "0.0.1";
	
	/**
	 * use test data
	 */
	public static boolean debug = false;
	
	/**
	 * result window title
	 */
	public static final String resultWindowTitle = "Radiomics Features";
	
	/**
	 * original input images
	 */
	private ImagePlus originalImp;
	private ImagePlus originalMask;
	
	/**
	 * analysis images using float processor.
	 */
	private ImagePlus currentImp;
	private ImagePlus currentMask;
	
	/**
	 * resampled images
	 */
	private ImagePlus resampledImp;
	private ImagePlus resampledMask;
	
	/**
	 * 1: range filter
	 * 2: remove outliers
	 */
	private ImagePlus resegmentedMask;
	
	/**
	 * after discretised
	 */
	protected static ImagePlus discretisedImp;
	
//	/**
//	 * isovoxelized (1,1,1) mask
//	 * created after resampling and re-segmenting.
//	 */
//	protected static ImagePlus isoMask;
//	
//	/**
//	 * resegmented voxels in Roi.
//	 * if normalized is on, insert normalized voxels
//	 */
//	protected static double[] resegmented_voxels;
//	
//	/**
//	 * resegmented and discretised voxels in Roi.
//	 * if normalized is on, insert normalized voxels
//	 */
//	protected static double[] resegmented_discretised_voxels;
	
	/**
	 * 0 : digital phantom1
	 * 1 : sample ct1
	 */
	static int testDataType = 0;
	
	/**
	 * interpolation for image.
	 * NEAREST_NEIGHBOR=0, NONE=0, BILINEAR=1, BICUBIC=2;
	 */
	public static int interpolation2D = ImageProcessor.BICUBIC;
	
	public static final int TRILINEAR = 100;
	
	/**
	 * Custom simple interpolation.
	 * perform 2 dimentional NearestNeighbour to x,y,z.
	 * This is not the same to 3D NEAREST NEIGHBOUR.
	 *  
	 */
	public static final int NONE_3D_INTERPOLATION = 999;
	
	public static int interpolation3D = TRILINEAR;
	
	public static int interpolation_mask3D = TRILINEAR;
	
	/**
	 * re-identify mask label value in voxles after interploration.
	 * mask label >= mask, and mask < (mask label+PartialVolumeThareshold)
	 */
	public static double mask_PartialVolumeThareshold = 0.5;
	
	/**
	 * 1 - 255 : enable label number.
	 * Target label value.
	 * When preprocess, mask is created by this label.
	 * Then mask pixel value was convert to (1) which is difined by label_.
	 */
	public static Integer targetLabel = 1; //target mask label
	
	//TODO
	/**
	 * When calculate features, label value always to be this value.
	 * Because to deal with partial volume effects from resampling. 
	 */
	public static final Integer label_ = 1;//label for compute
	
	/**
	 * Standardize original images at preprocessing 
	 */
	public static boolean normalize = false;
	
	/**
	 * remove outlier in original image at preprocessing
	 */
	public static boolean removeOutliers = false;
	
	/**
	 * if removeOutliers is true,
	 * normalized(standardized) pixel value is set limited range between,
	 * (mean - z_scre*sd) <= norm_x <= (mean + z_scre*sd).
	 * if norm_x > (mean + z_scre*sd), then norm_x = (mean + z_scre*sd).
	 * if norm_x < (mean - z_scre*sd), then norm_x = (mean - z_scre*sd).
	 * 
	 * z_score means (two-sided tails)...
	 * 80%CI=1.28
	 * 90%CI=1.645
	 * 95%CI=1.96 
	 * 95.45%CI=2.0
	 * 99%CI=2.58
	 * 99.73%CI=3.0(default)
	 */
	public static double zScore = 3d;
	
	/**
	 * scale to normalizeScale * ((X - mean)/sd)
	 */
	public static double normalizeScale = 1.0;
	
	/**
	 * Only used for to calculate energy, total energy, RMS in intensity based statistical features.
	 * No negative value(>=0, in unit value).
	 */
	public static Double densityShift = 0d;
	
	/**
	 * re-segmentation range min pixel value, in unit value(e.g, HU).
	 */
	public static Double rangeMin = null;// in unit value.
	
	/**
	 * re-segmentation range max pixel value, in unit value(e.g, HU).
	 */
	public static Double rangeMax = null;// in unit value.

	/**
	 * if true, binCount discretising is performed (and binWidth is ignored).
	 */
	public static boolean BOOL_USE_FixedBinNumber = true;
	
	/**
	 * fixed bin size
	 * calculate by (Xgl[max]-Xgl[min])+1.
	 * see, Utils.getNumOfBinsByMinMaxRange()
	 */
	public static Integer nBins = 32;
	
	/**
	 * fixed bin width
	 * calculate by ((Xgl - Xgl[min])/binWidth)+1.
	 * Value is should specified in unit.
	 */
	public static Double binWidth = 25d;//in unit.
	
	static double[] resamplingFactorXYZ=null;
	
	/**
	 * be careful, 
	 * IVH have perticluar values both binCount and binWidth.
	 * IVH_mode 0 : no disretise
	 * IVH mode 1 : binWidth discretising and performed on continuous operation.
	 * IVH mode 2 : binCount discretising without continuous operation.
	 */
	public static Integer IVH_binCount = 1000;
	public static Double IVH_binWidth = 2.5;
	public static Integer IVH_mode = 0;
	
	//texture hyper-param
	public static Integer alpha = 0;//NGLDM coarseness
	public static Integer deltaGLCM = 1;//distance
	public static Integer deltaNGToneDM = 1;//distance
	public static Integer deltaNGLevelDM = 1;//distance
	
	public static final String[] weighting_norms = new String[] { "no_weighting", "manhattan", "euclidian", "infinity" };
	public static String weightingNorm = null;
	
	/**
	 * to calculate fractal D.
	 * null-able.
	 */
	public static int[] box_sizes = null;
	
	/**
	 * calculate slice by slice
	 */
	public static boolean force2D = false;
	
	/**
	 * if you want no default features (such as MoransIIndex etc), turn this on. 
	 */
	public static boolean activate_no_default_features = false;
	
	//features
	boolean BOOL_enableOperationalInfo = true;
	boolean BOOL_enableDiagnostics = true;
	boolean BOOL_enableMorphological = true;
	boolean BOOL_enableLocalIntensityFeatures = true;
	boolean BOOL_enableIntensityBasedStatistics = true;
	boolean BOOL_enableIntensityHistogram = true;
	boolean BOOL_enableIntensityVolumeHistogram = true;
	boolean BOOL_enableGLCM = true;
	boolean BOOL_enableGLRLM = true;
	boolean BOOL_enableGLSZM = true;
	boolean BOOL_enableGLDZM = true;
	boolean BOOL_enableNGTDM = true;
	boolean BOOL_enableNGLDM = true;
	boolean BOOL_enableFractal = true;
	boolean BOOL_enableHomological = false;
	
	/**
	 * if force2D is true, can enable to calculate shape2d.
	 * else, ignored.
	 */
	boolean BOOL_enableShape2D = false;
	
	private HashSet<String> excluded;
	
	/**
	 * deprecated features
	 */
	String[] excluded_list = new String[] {
			/*Morphplogical feature*/
			MorphologicalFeatureType.VolumeDensity_OrientedMinimumBoundingBox.name(),
			MorphologicalFeatureType.AreaDensity_OrientedMinimumBoundingBox.name(),
			MorphologicalFeatureType.VolumeDensity_MinimumVolumeEnclosingEllipsoid.name(),
			MorphologicalFeatureType.AreaDensity_MinimumVolumeEnclosingEllipsoid.name(),
			/*IntensityVolumeHistogramFeature*/
			IntensityVolumeHistogramFeatureType.AreaUnderTheIVHCurve.name(),
			/*NGLDM*/
			NGLDMFeatureType.DependenceCountPercentage.name(),
	};
	
	/**
	 * No default features are not included as default.
	 * because calculation cost(time) much high (take too long time to calculate).
	 * if you use these features, turn on activate_include_no_default=true.
	 */
	String[] no_default_list = new String[] {
			MorphologicalFeatureType.MoransIIndex.name(),
			MorphologicalFeatureType.GearysCMeasure.name(),
			MorphologicalFeatureType.VolumeDensity_ConvexHull.name(),//take too long time to calculation
			MorphologicalFeatureType.AreaDensity_ConvexHull.name(),//take too long time to calculation
	};
	
	public RadiomicsJ() {
		initExcludeList();
	}
	
	public void setDebug(boolean debug) {
		RadiomicsJ.debug = debug;
	}
	
	private void initExcludeList() {
		excluded = new HashSet<String>();
		for(String excludedName : excluded_list) {
			excluded.add(excludedName);
		}
		if(!activate_no_default_features) {
			for(String nodefaultName : no_default_list) {
				excluded.add(nodefaultName);
			}
		}
	}
	
	public HashSet<String> getExcludedFeatures(){
		return excluded;
	}
		
	public void removeExcludedFeatures(String name) {
		if(excluded.contains(name)) {
			ArrayList<String> remove = new ArrayList<String>();
			remove.add(name);
			excluded.removeAll(remove);
		}
	}
	
	public void activateNoDefaultFeatures() {
		for(String name:no_default_list) {
			removeExcludedFeatures(name);
		}
	}
	
	public void loadSettings(String propFilePath) {
		if(propFilePath == null) {
			return;
		}
		File propFile = null;
		Properties prop = null;
		if(propFilePath != null) {
			propFile = new File(propFilePath);
			if(propFile==null || !propFile.exists()) {
				System.out.println("Sorry, can not read properties file correctly.");
				System.out.println("Please check input paths.");
				System.exit(0);
			}else {
				try (FileInputStream in = new FileInputStream(propFile);) {
					prop = new Properties();
					prop.load(in);
		        } catch (IOException e) {
		        	System.out.println("Ouch, fail to read properties file...");
		            e.printStackTrace();
		            System.exit(0);
		        }
			}
		}
		loadSettings(prop);
	}
	
	public void loadSettings(Properties prop) {
		if(prop == null) {
			System.out.println("properties file is null. Calculation is performed by using default.");
			return;
		}
		Set<Object> keys = prop.keySet();
		for(Object key : keys) {
			if(key instanceof String) {
				String keyString = (String)key;
				String val = prop.getProperty(keyString);
				if(val == null) {
					continue;
				}
				val = val.replace(" ", "");
				val = val.replace("　", "");
				val = val.replace("\n", "");
				val = val.replace("\t", "");
				if(val != null && val.length()!=0) {
					if(keyString.equals(SettingParams.INT_label.name())) {
						try{
							Integer n = Integer.valueOf(val);
							if(n < 1) {
								n = 1;
							}else if(n>255){
								n=255;
							}
							RadiomicsJ.targetLabel = n;
						}catch(NumberFormatException e) {
							//keep default
							continue;
						}
					}
					if(keyString.equals(SettingParams.INT_binCount.name())) {
						try{
							Integer n = Integer.valueOf(val);
							if(n < 1) {
								n = 1;
							}
							RadiomicsJ.nBins = n;
						}catch(NumberFormatException e) {
							//keep default
							continue;
						}
					}
					if(keyString.equals(SettingParams.INT_interpolation2D.name())) {
						try{
							Integer n = Integer.valueOf(val);
							if(n < 0 || n > 2) {
								n = 0;
							}
							RadiomicsJ.interpolation2D = n;
						}catch(NumberFormatException e) {
							//keep default
							continue;
						}
					}
//					if(keyString.equals(SettingParams.INT_interpolation_mask2D.name())) {
//						try{
//							Integer n = Integer.valueOf(val);
//							if(n < 0 || n > 2) {
//								n = 0;
//							}
//							RadiomicsJ.interpolation_mask2D = n;
//						}catch(NumberFormatException e) {
//							//keep default
//							continue;
//						}
//					}
					if(keyString.equals(SettingParams.INT_interpolation3D.name())) {
						try{
							Integer n = Integer.valueOf(val);
							if(n < 0) {
								n = 0;
							}
							RadiomicsJ.interpolation3D = n;
						}catch(NumberFormatException e) {
							//keep default
							continue;
						}
					}
					if(keyString.equals(SettingParams.INT_interpolation_mask3D.name())) {
						try{
							Integer n = Integer.valueOf(val);
							if(n < 0) {
								n = 0;
							}
							RadiomicsJ.interpolation_mask3D = n;
						}catch(NumberFormatException e) {
							//keep default
							continue;
						}
					}
					if(keyString.equals(SettingParams.DOUBLE_binWidth.name())) {
						try{
							Double n = Double.valueOf(val);
							if(n < 0d) {
								continue;
							}
							RadiomicsJ.binWidth = n;
						}catch(NumberFormatException e) {
							//keep default
							continue;
						}
					}
					if(keyString.equals(SettingParams.DOUBLE_zScore.name())) {
						try{
							Double n = Double.valueOf(val);
							if(n < 0d) {
								continue;
							}
							RadiomicsJ.zScore = n;
						}catch(NumberFormatException e) {
							//keep default
							continue;
						}
					}
					if(keyString.equals(SettingParams.DOUBLE_normalizeScale.name())) {
						try{
							Double n = Double.valueOf(val);
							if(n < 0d) {
								continue;
							}
							RadiomicsJ.normalizeScale = n;
						}catch(NumberFormatException e) {
							//keep default
							continue;
						}
					}
					if(keyString.equals(SettingParams.DOUBLE_densityShift.name())) {
						try{
							Double n = Double.valueOf(val);
							if(n < 0d) {
								continue;
							}
							RadiomicsJ.densityShift = n;
						}catch(NumberFormatException e) {
							//keep default
							continue;
						}
					}
					if(keyString.equals(SettingParams.DOUBLE_rangeMax.name())) {
						try{
							Double n = Double.valueOf(val);
							RadiomicsJ.rangeMax = n;
						}catch(NumberFormatException e) {
							//keep default
							continue;
						}
					}
					if(keyString.equals(SettingParams.DOUBLE_rangeMin.name())) {
						try{
							Double n = Double.valueOf(val);
							RadiomicsJ.rangeMin = n;
						}catch(NumberFormatException e) {
							//keep default
							continue;
						}
					}
					if(keyString.equals(SettingParams.INT_alpha.name())) {
						try{
							Integer n = Integer.valueOf(val);
							if(n < 0) {
								n = 0;
							}
							RadiomicsJ.alpha = n;
						}catch(NumberFormatException e) {
							//keep default
							continue;
						}
					}
					if(keyString.equals(SettingParams.INT_deltaGLCM.name())) {
						try{
							Integer n = Integer.valueOf(val);
							if(n < 1) {
								n = 1;
							}
							RadiomicsJ.deltaGLCM = n;
						}catch(NumberFormatException e) {
							//keep default
							continue;
						}
					}
					if(keyString.equals(SettingParams.INT_deltaNGTDM.name())) {
						try{
							Integer n = Integer.valueOf(val);
							if(n < 1) {
								n = 1;
							}
							RadiomicsJ.deltaNGToneDM = n;
						}catch(NumberFormatException e) {
							//keep default
							continue;
						}
					}
					if(keyString.equals(SettingParams.INT_deltaNGLDM.name())) {
						try{
							Integer n = Integer.valueOf(val);
							if(n < 1) {
								n = 1;
							}
							RadiomicsJ.deltaNGLevelDM = n;
						}catch(NumberFormatException e) {
							//keep default
							continue;
						}
					}
					if(keyString.equals(SettingParams.STRING_weightingNorm.name())) {
						if(val.length()<1) {
							RadiomicsJ.weightingNorm = null;//default
						}else {
							RadiomicsJ.weightingNorm = Utils.isValidWeightingNormName(val) ? val:null;
						}
					}
					//INTARRAY_box_sizes
					if(keyString.equals(SettingParams.INTARRAY_box_sizes.name())) {
						if(val.length()<1) {
							RadiomicsJ.box_sizes = null;//default
						}else {
							//if string parsing was failed, set null automatically.
							RadiomicsJ.box_sizes = Utils.s2ints(val);
						}
					}
					if(keyString.equals(SettingParams.INT_IVH_binCount.name())) {
						try{
							Integer n = Integer.valueOf(val);
							if(n < 1) {
								n = 1;
							}
							RadiomicsJ.IVH_binCount = n;
						}catch(NumberFormatException e) {
							//keep default
							continue;
						}
					}
					if(keyString.equals(SettingParams.DOUBLE_IVH_binWidth.name())) {
						try{
							Double n = Double.valueOf(val);
							if(n < 0) {
								n = Math.abs(n);
							}
							RadiomicsJ.IVH_binWidth = n;
						}catch(NumberFormatException e) {
							//keep default
							continue;
						}
					}
					if(keyString.equals(SettingParams.INT_IVH_MODE.name())) {
						try{
							Integer n = Integer.valueOf(val);
							if(n < 0) {
								n = 0;
							}
							RadiomicsJ.IVH_mode = n;
						}catch(NumberFormatException e) {
							//keep default
							continue;
						}
					}
					if(keyString.equals(SettingParams.BOOL_USE_FixedBinNumber.name())) {
						RadiomicsJ.BOOL_USE_FixedBinNumber = val.equals("1") || val.toLowerCase().equals("true") ? true:false;
					}
					if(keyString.equals(SettingParams.BOOL_normalize.name())) {
						RadiomicsJ.normalize = val.equals("1") || val.toLowerCase().equals("true") ? true:false;
					}
					if(keyString.equals(SettingParams.BOOL_removeOutliers.name())) {
						RadiomicsJ.removeOutliers = val.equals("1") || val.toLowerCase().equals("true") ? true:false;
					}
					//DOUBLEARRAY_resamplingFactorXYZ
					if(keyString.equals(SettingParams.DOUBLEARRAY_resamplingFactorXYZ.name())) {
						if(val.length()<1) {
							RadiomicsJ.resamplingFactorXYZ = null;//default
						}else {
							//if string parsing was failed, set null automatically.
							RadiomicsJ.resamplingFactorXYZ = Utils.s2doubles(val);
						}
					}
					if(keyString.equals(SettingParams.BOOL_force2D.name())) {
						RadiomicsJ.force2D = val.equals("1") || val.toLowerCase().equals("true") ? true:false;
					}
					if(keyString.equals(SettingParams.BOOL_activate_no_default_features.name())) {
						RadiomicsJ.activate_no_default_features = val.equals("1") || val.toLowerCase().equals("true") ? true:false;
					}
					if(keyString.equals(SettingParams.DOUBLE_Mask_PartialVolumeThareshold.name())) {
						try{
							Double n = Double.valueOf(val);
							if(n < 0 || n > 0.999) {
								n = 0.5;
							}
							RadiomicsJ.mask_PartialVolumeThareshold = n;
						}catch(NumberFormatException e) {
							//keep default
							continue;
						}
					}
					
					/*
					 * features
					 */
					if(keyString.equals(SettingParams.BOOL_enableOperationalInfo.name())) {
						this.BOOL_enableOperationalInfo = val.equals("1") || val.toLowerCase().equals("true") ? true:false;
					}
					if(keyString.equals(SettingParams.BOOL_enableDiagnostics.name())) {
						this.BOOL_enableDiagnostics = val.equals("1") || val.toLowerCase().equals("true") ? true:false;
					}
					if(keyString.equals(SettingParams.BOOL_enableIntensityBasedStatistics.name())) {
						this.BOOL_enableIntensityBasedStatistics = val.equals("1") || val.toLowerCase().equals("true") ? true:false;
					}
					if(keyString.equals(SettingParams.BOOL_enableIntensityHistogram.name())) {
						this.BOOL_enableIntensityHistogram = val.equals("1") || val.toLowerCase().equals("true") ? true:false;
					}
					if(keyString.equals(SettingParams.BOOL_enableIntensityVolumeHistogram.name())) {
						this.BOOL_enableIntensityVolumeHistogram = val.equals("1") || val.toLowerCase().equals("true") ? true:false;
					}
					if(keyString.equals(SettingParams.BOOL_enableMorphological.name())) {
						this.BOOL_enableMorphological = val.equals("1") || val.toLowerCase().equals("true") ? true:false;
					}
					if(keyString.equals(SettingParams.BOOL_enableLocalIntensityFeatures.name())) {
						this.BOOL_enableLocalIntensityFeatures = val.equals("1") || val.toLowerCase().equals("true") ? true:false;
					}
					if(keyString.equals(SettingParams.BOOL_enableGLCM.name())) {
						this.BOOL_enableGLCM = val.equals("1") || val.toLowerCase().equals("true") ? true:false;
					}
					if(keyString.equals(SettingParams.BOOL_enableGLRLM.name())) {
						this.BOOL_enableGLRLM = val.equals("1") || val.toLowerCase().equals("true") ? true:false;
					}
					if(keyString.equals(SettingParams.BOOL_enableGLSZM.name())) {
						this.BOOL_enableGLSZM = val.equals("1") || val.toLowerCase().equals("true") ? true:false;
					}
					if(keyString.equals(SettingParams.BOOL_enableGLDZM.name())) {
						this.BOOL_enableGLDZM = val.equals("1") || val.toLowerCase().equals("true") ? true:false;
					}
					if(keyString.equals(SettingParams.BOOL_enableNGTDM.name())) {
						this.BOOL_enableNGTDM = val.equals("1") || val.toLowerCase().equals("true") ? true:false;
					}
					if(keyString.equals(SettingParams.BOOL_enableNGLDM.name())) {
						this.BOOL_enableNGLDM = val.equals("1") || val.toLowerCase().equals("true") ? true:false;
					}
					if(keyString.equals(SettingParams.BOOL_enableHomological.name())) {
						this.BOOL_enableHomological = val.equals("1") || val.toLowerCase().equals("true") ? true:false;
					}
					if(keyString.equals(SettingParams.BOOL_enableFractal.name())) {
						this.BOOL_enableFractal = val.equals("1") || val.toLowerCase().equals("true") ? true:false;
					}
					if(keyString.equals(SettingParams.BOOL_enableShape2D.name())) {
						this.BOOL_enableShape2D = val.equals("1") || val.toLowerCase().equals("true") ? true:false;
					}
				}
			}
		}
	}
	
	/**
	 * create copy original as float processor,
	 * and replace target label to analysis mask label(1).
	 * @param originalImp
	 * @param originalMask
	 * @param targetLabel
	 * @throws Exception
	 */
	public void preprocess(ImagePlus originalImp, ImagePlus originalMask, Integer targetLabel) throws Exception {
		if(originalMask == null) {
			int w = originalImp.getWidth();
			int h = originalImp.getHeight();
			int s = originalImp.getNSlices();
			originalMask = ImagePreprocessing.createMask(w, h, s, null, label_, originalImp.getCalibration().pixelWidth, originalImp.getCalibration().pixelHeight, originalImp.getCalibration().pixelDepth);
		}
		if(debug) {
			System.out.println("preparing analysis images ...");
		}
		//label to 1.
		preprocessAnalysisReady(originalImp, originalMask, targetLabel);
		
		if(currentImp == null || currentMask == null) {
			System.out.println("RadiomicsJ:preprocess()::Creating Mask was failed. return.");
			return;
		}
		
		if(debug) {
			System.out.println("perform resampling ...");
		}
		preprocessResample(currentImp, currentMask);
		if(debug) {
			System.out.println("perform re-segmentation ...");
		}
		//use label 1.
		preprocessResegment(resampledImp, resampledMask, RadiomicsJ.label_);
		/*
		 * normalize
		 */
		if(normalize) {
			if(debug) {
				System.out.println("perform normalization ...");
			}
			resampledImp = ImagePreprocessing.normalize(resampledImp, resegmentedMask, RadiomicsJ.label_);
		}
		if(debug) {
			System.out.println("perform discretisation ...");
		}
		preprocessDiscretise(resampledImp, resegmentedMask, RadiomicsJ.label_);
	}
	
	/**
	 * convert to float32 and,
	 * mask label will convert label(1), this is because deal with partial volume effects at interpolation.
	 * @param img
	 * @param mask
	 * @return
	 */
	public ImagePlus[] preprocessAnalysisReady(ImagePlus img, ImagePlus mask, Integer targetLabel) {
		currentImp = Utils.createImageCopyAsFloat(img, false);
		/*
		 * convert target label(any) to analysis label(1) 
		 */
		currentMask = Utils.initMaskAsFloatAndConvertLabelOne(mask, targetLabel);
		
		if(Utils.isBlankMaskStack(currentMask, RadiomicsJ.label_)) {
			currentImp = null;
			currentMask = null;
			new Exception("Mask does not have target label. Can not compute features.");
		}
		return new ImagePlus[] {currentImp, currentMask};
	}
	
	/**
	 * resample x-y-z.
	 * @param img
	 * @param mask
	 * @return
	 */
	public ImagePlus[] preprocessResample(ImagePlus img, ImagePlus mask) {
		if(resamplingFactorXYZ != null) {
			if(force2D) {
				//ignore z
				resampledImp = Utils.resample2D(img, false, resamplingFactorXYZ[0], resamplingFactorXYZ[1], RadiomicsJ.interpolation2D);
				resampledMask = Utils.resample2D(mask, true, resamplingFactorXYZ[0], resamplingFactorXYZ[1], RadiomicsJ.interpolation2D);
			}else {
				// trilinear interpolation
				resampledImp = Utils.resample3D(img, false, resamplingFactorXYZ[0], resamplingFactorXYZ[1], resamplingFactorXYZ[2]);
				resampledMask = Utils.resample3D(mask, true, resamplingFactorXYZ[0], resamplingFactorXYZ[1], resamplingFactorXYZ[2]);
			}
		}else {
			//AS-IS
			resampledImp = Utils.createImageCopy(img);
			resampledMask = Utils.createMaskCopy(mask);
		}
		return new ImagePlus[] {resampledImp, resampledMask};
	}
	
	/**
	 * If did preprocessAnalysisReady() before, 
	 * targetLabel should be "1".
	 * @param img
	 * @param mask
	 * @return
	 */
	public ImagePlus preprocessResegment(ImagePlus img, ImagePlus mask, Integer targetLabel) {
		
		/*
		 * rangeFilter
		 */
		if(rangeMax != null && rangeMin != null) {
			resegmentedMask = ImagePreprocessing.rangeFiltering(img, mask, targetLabel, rangeMax, rangeMin);
		}else {
			resegmentedMask = Utils.createMaskCopy(mask);
		}
		
		if(removeOutliers) {
			// get new mask removed outliers
			resegmentedMask = ImagePreprocessing.outlierFiltering(img, resegmentedMask, targetLabel);
		}
		
		if(resegmentedMask == null) {
			resegmentedMask = Utils.createMaskCopy(mask);
		}
		
		return resegmentedMask;
	}
	
	/**
	 * create discretized image.
	 * 
	 * @param resampled : after preprocess()
	 * @param resegmentedMask : after preprocess()
	 * @param targetLabel : If preprocessAnalysisReady() performed before, targetLabel should be "1".
	 * @return
	 * @throws Exception
	 */
	public ImagePlus preprocessDiscretise(ImagePlus resampled, ImagePlus resegmentedMask, Integer targetLabel) throws Exception {
		discretisedImp = null;
		if(BOOL_USE_FixedBinNumber) {
			discretisedImp = Utils.discrete(resampled, resegmentedMask, targetLabel, RadiomicsJ.nBins);
		}else {
			/*
			 * Fixed Bin Width
			 */
			discretisedImp = Utils.discreteByBinWidth(resampled, resegmentedMask, targetLabel, binWidth);
			RadiomicsJ.nBins = Utils.getNumOfBinsByMax(discretisedImp, resegmentedMask, targetLabel);
		}
		return discretisedImp;
	}
	
	public ResultsTable execute(File imgSeriesFileFolder, File maskSeriesFileFolder, Integer targetLabel) throws Exception {
		
		System.out.println("execute");
		if(activate_no_default_features) {
			activateNoDefaultFeatures();
		}
		
		// do not do this, to read NifTi.
//		if(!imgSeriesFileFolder.isDirectory() || !maskSeriesFileFolder.isDirectory()) {
//			System.out.println("Sorry, please input directory. return null.");
//			return null;
//		}
		/*
		 * nifti
		 */
		if(imgSeriesFileFolder.isFile()) {
			if(imgSeriesFileFolder.getName().contains(".nii.gz")) {
				String p2i = imgSeriesFileFolder.getAbsolutePath();
				String p2m = maskSeriesFileFolder.getAbsolutePath();
				Object img = null;
				Object mask = null;
				img = IJ.runPlugIn("Nifti_Reader", p2i);
		        mask = IJ.runPlugIn("Nifti_Reader", p2m);

				//img = BF.openImagePlus(p2i)[0];
				//mask = BF.openImagePlus(p2m)[0];

		        if(img == null) {
		        	System.out.println("Can not load nifti file... return null.");
		        	return null;
		        }
				if(force2D) {
					return extractAllSlice((ImagePlus)img,(ImagePlus)mask,targetLabel);
				}else {
					return extractAll((ImagePlus)img,(ImagePlus)mask,targetLabel);
				}
			}else if(imgSeriesFileFolder.getName().endsWith(".tif") || imgSeriesFileFolder.getName().endsWith(".tiff")) {
				String p2i = imgSeriesFileFolder.getAbsolutePath();
				String p2m = maskSeriesFileFolder.getAbsolutePath();
				//ImagePlus img = new ImagePlus(p2i);
				//ImagePlus mask = new ImagePlus(p2m);
				ImagePlus img = BF.openImagePlus(p2i)[0];
				ImagePlus mask = BF.openImagePlus(p2m)[0];
				if(force2D) {
					return extractAllSlice(img, mask,targetLabel);
				}else {
					return extractAll(img, mask,targetLabel);
				}
			}
		}else if(imgSeriesFileFolder.listFiles().length == 1 && maskSeriesFileFolder.listFiles().length == 1) {
			imgSeriesFileFolder = imgSeriesFileFolder.listFiles()[0];
			maskSeriesFileFolder = maskSeriesFileFolder.listFiles()[0];
			if(imgSeriesFileFolder.getName().contains(".nii.gz")) {
				String p2i = imgSeriesFileFolder.getAbsolutePath();
				String p2m = maskSeriesFileFolder.getAbsolutePath();
				Object img = null;
				Object mask = null;
				img = IJ.runPlugIn("Nifti_Reader", p2i);
		        mask = IJ.runPlugIn("Nifti_Reader", p2m);
		        if(img == null) {
		        	System.out.println("Can not load nifti file... return null.");
		        	return null;
		        }
				if(force2D) {
					return extractAllSlice((ImagePlus)img,(ImagePlus)mask,targetLabel);
				}else {
					return extractAll((ImagePlus)img,(ImagePlus)mask,targetLabel);
				}
			}else if(imgSeriesFileFolder.getName().endsWith(".tif") || imgSeriesFileFolder.getName().endsWith(".tiff")) {
				String p2i = imgSeriesFileFolder.getAbsolutePath();
				String p2m = maskSeriesFileFolder.getAbsolutePath();
				ImagePlus img = new ImagePlus(p2i);
				ImagePlus mask = new ImagePlus(p2m);
				if(force2D) {
					return extractAllSlice(img, mask,targetLabel);
				}else {
					return extractAll(img, mask,targetLabel);
				}
			}
		}
		
		if(force2D) {
			return extractAllSlice(imgSeriesFileFolder.listFiles(), maskSeriesFileFolder.listFiles(),targetLabel);
		}else {
			return extractAll(new ImagePlus(imgSeriesFileFolder.getAbsolutePath()), new ImagePlus(maskSeriesFileFolder.getAbsolutePath()),targetLabel);
		}
	}
	
	public ResultsTable execute(ImagePlus img, ImagePlus mask, Integer targetLabel) throws Exception {
		if(activate_no_default_features) {
			activateNoDefaultFeatures();
		}
		if(force2D) {
			return extractAllSlice(img, mask,targetLabel);
		}else {
			return extractAll(img, mask,targetLabel);
		}
	}
	
	public ResultsTable extractAll(ImagePlus img, ImagePlus mask, Integer targetLabel) throws Exception {
		originalImp = img;
		originalMask = mask;
		/*
		 * create label 1 mask
		 * resample
		 * re-segmentation
		 * standardization
		 */
		preprocess(originalImp, originalMask, targetLabel);
		return compute(resampledImp, resegmentedMask,RadiomicsJ.label_);
	}
	
	
	/**
	 * images and masks file names should be same or set sortable names pair (it can keep order images and masks list).
	 * extract features slice by slice
	 * @throws Exception 
	 */
	public ResultsTable extractAllSlice(File[] images, File[] masks, Integer targetLabel) throws Exception {
		/*
		 * if dicom
		 */
		ImagePlus[] sampleIs = BF.openImagePlus(images[0].getAbsolutePath());
		ImagePlus[] sampleMs = BF.openImagePlus(masks[0].getAbsolutePath());
		ImagePlus sampleI = sampleIs[0];
		ImagePlus sampleM = sampleMs[0];

		/*
		for(float[] arr: sampleM.getProcessor().getFloatArray()) {
			for(float m : arr){
				System.out.print(m);
				System.out.print(" ");
			}
			System.out.println(" ");
		}
		*/
		//System.out.println(sampleM.getProcessor().getFloatArray());

		String sopInstUID_I = DicomTools.getTag(sampleI, "0008,0018");
		String sopInstUID_M = DicomTools.getTag(sampleM, "0008,0018");
		if(sopInstUID_I != null && sopInstUID_M != null) {
			File parentImgFolder = images[0].getParentFile();
			File parentMaskFolder = masks[0].getParentFile();
			ImagePlus is = new ImagePlus(parentImgFolder.getAbsolutePath());
			ImagePlus ms = new ImagePlus(parentMaskFolder.getAbsolutePath());
			//sort by image number
			is.setStack(DicomTools.sort(is.getStack()));
			ms.setStack(DicomTools.sort(ms.getStack()));
			//do not preprocess here yet
			return extractAllSlice(is, ms, targetLabel);
		}else {
			/*
			 * check matching names pair ?
			 * if found no-match, return exception ?
			 */
			ArrayList<String> iNameArray = new ArrayList<>();
			ArrayList<String> mNameArray = new ArrayList<>();
			int s = images.length;
			for(int i=0;i<s;i++) {
				String iName = images[i].getName();
				String mName = masks[i].getName();
				iNameArray.add(iName);
				mNameArray.add(mName);
			}
			System.out.println(iNameArray);
			Collections.sort(iNameArray);
			Collections.sort(mNameArray);
			int w = sampleI.getWidth();
			int h = sampleI.getHeight();
			ImageStack is = new ImageStack(w, h);
			ImageStack ms = new ImageStack(w, h);
			for(int i=0;i<s;i++) {
				String iName = iNameArray.get(i);
				String mName = mNameArray.get(i);
				File imgF = null;
				File mskF = null;
				for(int j=0;j<s;j++) {
					if(images[j].getName().equals(iName)) {
						imgF = images[j];
					}
					if(masks[j].getName().equals(mName)) {
						mskF = masks[j];
					}
				}
				//System.out.println(" ");
				//System.out.println(imgF.getAbsolutePath());
				is.addSlice(BF.openImagePlus(imgF.getAbsolutePath())[0].getProcessor());
				ms.addSlice(BF.openImagePlus(mskF.getAbsolutePath())[0].getProcessor());
			}
			ImagePlus ds_i = new ImagePlus("images", is);
			ds_i.setCalibration(sampleI.getCalibration());
			ImagePlus ds_m = new ImagePlus("masks", ms);
			ds_m.setCalibration(sampleI.getCalibration());//set calibration using from image

			//System.out.println(ds_m.getProcessor().getFloatArray());

			//do not preprocess here yet
			return extractAllSlice(ds_i, ds_m, targetLabel);
		}
	}
	
	/**
	 * extract features slice by slice
	 * @param images : stack series images
	 * @param masks : stack series masks
	 * @return
	 */
	public ResultsTable extractAllSlice(ImagePlus images, ImagePlus masks, Integer targetLabel) {
		originalImp = images;
		originalMask = masks;
		ResultsTable rt = null;
		int num = images.getNSlices();
		for(int i=0;i<num;i++) {
			try {
				currentImp = new ImagePlus(i+"", images.getStack().getProcessor(i+1).duplicate());
				currentMask = new ImagePlus(i+"", masks.getStack().getProcessor(i+1).duplicate());
				currentImp.setCalibration(images.getCalibration());
				currentMask.setCalibration(masks.getCalibration());
				if(Utils.isBlankMaskSlice(currentMask.getProcessor(), targetLabel)) {
					continue;
				}
				/*
				 * do preprocessing
				 */
				preprocess(currentImp, currentMask, targetLabel);
				System.out.println("Compute at "+(i+1));
				ResultsTable table = compute(resampledImp, resegmentedMask,RadiomicsJ.label_);
				if(rt == null) {
					rt = table;
				}else {
					if(table != null) {
						rt.incrementCounter();
						String[] headings = table.getHeadings();
						int row  = 0;
						for(String h : headings) {
							if(h.contains("OperationalInfo_")) {
								String v = table.getStringValue(h, row);
								rt.addValue(h, v);
							}else {
								double v = table.getValue(h, row);
								rt.addValue(h, v);
							}
						}
					}
				}
			} catch (Exception e) {
				System.err.println("Something strange skip this images and masks stack pair -> "+images.getTitle()+" and "+masks.getTitle());
				e.printStackTrace();
				continue;
			}
		}
		return rt;
	}
	
	/**
	 * 
	 * @param img
	 * @param mask
	 * @param targetLabel : if preprocess() is done, set to (1)
	 * @return
	 * @throws Exception
	 */
	public ResultsTable compute(ImagePlus img, ImagePlus mask, Integer targetLabel) throws Exception {

		if(img == null) {
			return null;
		}
		
		ResultsTable rt = ResultsTable.getResultsTable(resultWindowTitle);
		if(rt == null) {
			rt = new ResultsTable();
		}
		rt.incrementCounter();
		
		if(BOOL_enableOperationalInfo) {
			if(debug) {
				System.out.println("=======================");
				System.out.println("OperationalInformations");
			}
			OperationalInfoFeatures oif = new OperationalInfoFeatures(img);
			java.util.HashMap<String,String> info = oif.getInfo();
			Iterator<String> keys = info.keySet().iterator();
			while(keys.hasNext()) {
				String key = keys.next();
				String val = info.get(key);
				rt.addValue("OperationalInfo_" + key, val == null ? "NaN":val);
				if(debug) {
					System.out.println(key+", "+val);
				}
			}
		}
		
		/*
		 * diagnostics...
		 */
		if(BOOL_enableDiagnostics) {
			if(debug) {
				System.out.println("=======================");
				System.out.println("Diagnostics information");
			}
			
			DiagnosticsInfo di = new DiagnosticsInfo(currentImp, currentMask, resampledImp, resampledMask, resegmentedMask, targetLabel);
			
			for(DiagnosticsInfoType dinfo : DiagnosticsInfoType.values()) {
				Double i = di.getDiagnosticsBy(dinfo.name());
				if(i == null) {
					rt.addValue("Diagnostics_" + dinfo.name(), "NaN");
				}else {
					rt.addValue("Diagnostics_" + dinfo.name(), i);
				}
				if(debug) {
					System.out.println(dinfo.name()+", "+i);
				}
			}
		}
		
		if(BOOL_enableMorphological) {
			if(debug) {
				System.out.println("=======================");
				System.out.println("Morphological features");
			}
			MorphologicalFeatures f = new MorphologicalFeatures(img, mask, targetLabel);
			for (MorphologicalFeatureType ft : MorphologicalFeatureType.values()) {
				if(excluded.contains(ft.name())) {
					continue;
				}
				Double feature = f.calculate(ft.id());
				if(feature == null || feature == Double.NaN) {
					rt.addValue("Morphology_" + ft.name(), "NaN");
				}else {
					rt.addValue("Morphology_" + ft.name(), feature);
				}
				if(debug) {
					System.out.println(ft.name()+", "+feature);
				}
			}
		}
		
		if(BOOL_enableLocalIntensityFeatures) {
			if(debug) {
				System.out.println("=======================");
				System.out.println("Local intensity features");
			}
			LocalIntensityFeatures f = new LocalIntensityFeatures(img, mask, targetLabel);
			for (LocalIntensityFeatureType ft : LocalIntensityFeatureType.values()) {
				if(excluded.contains(ft.name())) {
					continue;
				}
				Double feature = f.calculate(ft.id());
				if(feature == null || feature == Double.NaN) {
					rt.addValue("LocalIntensity_" + ft.name(), "NaN");
				}else {
					rt.addValue("LocalIntensity_" + ft.name(), feature);
				}
				if(debug) {
					System.out.println(ft.name()+", "+feature);
				}
			}
		}
		
		if(BOOL_enableIntensityBasedStatistics) {
			if(debug) {
				System.out.println("=================================");
				System.out.println("IntensityBasedStatistics features");
			}
			IntensityBasedStatisticalFeatures executer = new IntensityBasedStatisticalFeatures(img, mask,targetLabel);
			for (IntensityBasedStatisticalFeatureType f : IntensityBasedStatisticalFeatureType.values()) {
				if(excluded.contains(f.name())) {
					continue;
				}
				Double feature = executer.calculate(f.id());
				if (feature == null || feature == Double.NaN) {
					rt.addValue("IntensityBasedStatistical_" + f.name(), "NaN");
				} else {
					rt.addValue("IntensityBasedStatistical_" + f.name(), feature);
				}
				if(debug) {
					System.out.println(f.name()+", "+feature);
				}
			}
		}
		
		if(BOOL_enableIntensityHistogram) {
			if(debug) {
				System.out.println("=================================");
				System.out.println("IntensityHistogram features");
			}
			IntensityHistogramFeatures executer = new IntensityHistogramFeatures(img, mask, targetLabel, BOOL_USE_FixedBinNumber, nBins,binWidth);
			for (IntensityHistogramFeatureType f : IntensityHistogramFeatureType.values()) {
				if(excluded.contains(f.name())) {
					continue;
				}
				Double feature = executer.calculate(f.id());
				if (feature == null || feature == Double.NaN) {
					rt.addValue("IntensityHistogram_" + f.name(), "NaN");
				} else {
					rt.addValue("IntensityHistogram_" + f.name(), feature);
				}
				if(debug) {
					System.out.println(f.name()+", "+feature);
				}
			}
		}
		
		if(BOOL_enableIntensityVolumeHistogram) {
			if(debug) {
				System.out.println("=================================");
				System.out.println("IntensityVolumeHistogram features");
			}
			IntensityVolumeHistogramFeatures executer = new IntensityVolumeHistogramFeatures(img, mask, targetLabel, IVH_mode);
			for (IntensityVolumeHistogramFeatureType f : IntensityVolumeHistogramFeatureType.values()) {
				if(excluded.contains(f.name())) {
					continue;
				}
				Double feature = executer.calculate(f.id());
				if (feature == null || feature == Double.NaN) {
					rt.addValue("IntensityVolumeHistogram_" + f.name(), "NaN");
				} else {
					rt.addValue("IntensityVolumeHistogram_" + f.name(), feature);
				}
				if(debug) {
					System.out.println(f.name()+", "+feature);
				}
			}
		}
		
		if(BOOL_enableShape2D && force2D) {
			if(debug) {
				System.out.println("=================================");
				System.out.println("Shape2D features");
			}
			if(img.getNSlices() > 1) {
				System.out.println("RadiomicsJ: Cannot calculate Shape2D, because image has multi slices.");
				System.out.println("If you need Shape2D, Try create single slice imageplus, then perform Shape2D.");
				System.out.println("Or, you can try to use Shape2DFeatures class on another scripts.");
			}else {
				Shape2DFeatures shape2DExecuter = new Shape2DFeatures(img, mask,1,targetLabel);
				for (Shape2DFeatureType shape : Shape2DFeatureType.values()) {
					if(excluded.contains(shape.name())) {
						continue;
					}
					Double feature = shape2DExecuter.calculate(shape.id());
					if (feature == null || feature == Double.NaN) {
						rt.addValue("Shape2D_" + shape.name(), "NaN");
					} else {
						rt.addValue("Shape2D_" + shape.name(), feature);
					}
					if (debug) {
						System.out.println(shape.name() + ", " + feature);
					}
				}
			}
		}
	
		if(BOOL_enableGLCM) {
			if(debug) {
				System.out.println("=================================");
				System.out.println("GLCM features");
			}

			GLCMFeatures glcmExecuter = new GLCMFeatures(img, 
														 mask, 
														 targetLabel,
														 deltaGLCM,
														 BOOL_USE_FixedBinNumber, 
														 nBins,
														 binWidth,
														 weightingNorm);
			for (GLCMFeatureType glcm : GLCMFeatureType.values()) {
				if(excluded.contains(glcm.name())) {
					continue;
				}
				Double feature = glcmExecuter.calculate(glcm.id());
				if (feature == null|| feature == Double.NaN) {
					rt.addValue("GLCM_" + glcm.name(), "NaN");
				} else {
					rt.addValue("GLCM_" + glcm.name(), feature);
				}
				if (debug) {
					System.out.println(glcm.name() + ", " + feature);
				}
			}
		}
		
		if(BOOL_enableGLRLM) {
			if(debug) {
				System.out.println("=================================");
				System.out.println("GLRLM features");
			}
			GLRLMFeatures glrlmExecuter = new GLRLMFeatures(img, 
															mask, 
															targetLabel,
															BOOL_USE_FixedBinNumber,
															nBins, 
															binWidth,
															weightingNorm);
			for (GLRLMFeatureType glrlm : GLRLMFeatureType.values()) {
				if(excluded.contains(glrlm.name())) {
					continue;
				}
				Double feature = glrlmExecuter.calculate(glrlm.id());
				if (feature == null|| feature == Double.NaN) {
					rt.addValue("GLRLM_" + glrlm.name(), "NaN");
				} else {
					rt.addValue("GLRLM_" + glrlm.name(), feature);
				}
				if (debug) {
					System.out.println(glrlm.name() + ", " + feature);
				}
			}
		}
		
		if(BOOL_enableGLSZM) {
			if(debug) {
				System.out.println("=================================");
				System.out.println("GLSZM features");
			}
			GLSZMFeatures glszmExecuter = new GLSZMFeatures(img,
															mask,
															targetLabel,
															BOOL_USE_FixedBinNumber,
															nBins,
															binWidth);
			for (GLSZMFeatureType glszm : GLSZMFeatureType.values()) {
				if(excluded.contains(glszm.name())) {
					continue;
				}
				Double feature = glszmExecuter.calculate(glszm.id());
				if (feature == null || feature == Double.NaN) {
					rt.addValue("GLSZM_" + glszm.name(), "NaN");
				} else {
					rt.addValue("GLSZM_" + glszm.name(), feature);
				}
				if (debug) {
					System.out.println(glszm.name() + ", " + feature);
				}
			}
		}
		
		if(BOOL_enableGLDZM) {
			if(debug) {
				System.out.println("=================================");
				System.out.println("GLDZM features");
			}
			GLDZMFeatures gldzmExecuter = new GLDZMFeatures(img,
															mask,
															targetLabel,
															BOOL_USE_FixedBinNumber,
															nBins,
															binWidth);
			for (GLDZMFeatureType gldzm : GLDZMFeatureType.values()) {
				if(excluded.contains(gldzm.name())) {
					continue;
				}
				Double feature = gldzmExecuter.calculate(gldzm.id());
				if (feature == null || feature == Double.NaN) {
					rt.addValue("GLDZM_" + gldzm.name(), "NaN");
				} else {
					rt.addValue("GLDZM_" + gldzm.name(), feature);
				}
				if (debug) {
					System.out.println(gldzm.name() + ", " + feature);
				}
			}
		}
		
		if(BOOL_enableNGTDM) {
			if(debug) {
				System.out.println("=================================");
				System.out.println("NGTDM features");
			}
			NGTDMFeatures ngtdmExecuter = new NGTDMFeatures(img,
															mask,
															targetLabel,
															deltaNGToneDM,
															BOOL_USE_FixedBinNumber,
															nBins,
															binWidth);
			for (NGTDMFeatureType ngtdm : NGTDMFeatureType.values()) {
				if(excluded.contains(ngtdm.name())) {
					continue;
				}
				Double feature = ngtdmExecuter.calculate(ngtdm.id());
				if (feature == null || feature == Double.NaN) {
					rt.addValue("NGTDM_" + ngtdm.name(), "NaN");
				} else {
					rt.addValue("NGTDM_" + ngtdm.name(), feature);
				}
				if (debug) {
					System.out.println(ngtdm.name() + ", " + feature);
				}
			}
		}
		
		if(BOOL_enableNGLDM) {
			if(debug) {
				System.out.println("=================================");
				System.out.println("NGLDM features");
			}
			NGLDMFeatures gldmExecuter = new NGLDMFeatures(img, 
															mask, 
															targetLabel,
															alpha, 
															deltaNGLevelDM,
															BOOL_USE_FixedBinNumber,
															nBins,
															binWidth);
			for(NGLDMFeatureType gldm:NGLDMFeatureType.values()) {
				if(excluded.contains(gldm.name())) {
					continue;
				}
				Double feature = gldmExecuter.calculate(gldm.id());
				if(feature == null || feature == Double.NaN) {
					rt.addValue("NGLDM_"+gldm.name(), "NaN");
				}else {
					rt.addValue("NGLDM_"+gldm.name(), feature);
				}
				if (debug) {
					System.out.println(gldm.name() + ", " + feature);
				}
			}
		}

		if(BOOL_enableFractal) {
			if(debug) {
				System.out.println("=================================");
				System.out.println("Fractal features");
			}
			FractalFeatures fractalExecuter = null;
			if(force2D) {
				fractalExecuter = new FractalFeatures(img, mask, targetLabel, 1, RadiomicsJ.box_sizes);
			}else {
				fractalExecuter = new FractalFeatures(img, mask, targetLabel, null, RadiomicsJ.box_sizes);
			}
			if(fractalExecuter != null) {
				for(FractalFeatureType fractal:FractalFeatureType.values()) {
					if(excluded.contains(fractal.name())) {
						continue;
					}
					Double feature = fractalExecuter.calculate(fractal.id());
					if(feature == null || feature == Double.NaN) {
						rt.addValue("Fractal_"+fractal.name(), "NaN");
					}else {
						rt.addValue("Fractal_"+fractal.name(), feature);
					}
					if (debug) {
						System.out.println(fractal.name() + ", " + feature);
					}
				}
			}
		}
		System.gc();
		return rt;
	}
}
