from benchmark import Benchmark
from datageneration import DatasetGenerator

# settings-1
idir = "/home/kharchenkoa2/work/data/synthetic3/int"
sdir = "/home/kharchenkoa2/work/data/synthetic3/seg"

# settings-2
work_dir = "/home/kharchenkoa2/work/data/synthetic3"
nyxus_executable = "/is/not/used"
feature_list = "*ALL*"
generate_missing_image = False
base_mask_image_path = "./arnoldcat_pure_cat.jpg"
base_intensity_image_path = "./siemens_star.tif"

if __name__ == '__main__':

    # settings-3
    n_rois = [10, 50, 100, 500, 1000, 10000, 100000, 500000]	# Smaller ROI first
    roi_areas = [10, 100, 500, 1000, 10000, 100000]
    padding = 5
    percent_oversized_roi = 30

    #generate
    dataset_generator = DatasetGenerator(
        idir,
        sdir,
        base_mask_image_path,
        base_intensity_image_path)

    for n in n_rois:
        for s in roi_areas:
            print (f"generating n_roi={n} roi_size={s} \n")
            dataset_generator.generate_image_pair (n, s, padding, percent_oversized_roi)

    ''' ------ skip benchmarking, just generate data ------
    benchmark = Benchmark(  int_image_dir,
                            seg_image_dir,
                            work_dir, 
                            nyxus_executable, 
                            feature_list, 
                            generate_missing_image
                        )


    benchmark.run_benchmark_suit()
    benchmark.create_benchmark_plot("Total", "All", "All")
    ------ '''
