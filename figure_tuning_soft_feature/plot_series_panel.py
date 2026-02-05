# load data
fpath = "/work/nyxuspaper/XY_grey2wob1s10-200_oldnjagged.csv"
dfSeries = pd.read_csv(fpath)

my_dpi = 96
#fig = plt.figure(figsize=(10, 5))
fig = plt.figure(figsize=(1000/my_dpi, 500/my_dpi), dpi=my_dpi)
plt.plot (dfSeries['X'], dfSeries['Y'], linewidth=3.0, marker='o', markeredgecolor='k', markerfacecolor='w')
plt.title("")

# without font
'''
plt.xlabel("grey depth")
plt.ylabel("wb-statistics")
'''
# with font
hfont = {'fontname':'Arial'}
font = {'family' : 'Arial',
        #'weight' : 'bold',
        'size'   : 20}
plt.xlabel('grey depth', **font)
plt.ylabel('wb-statistic', **font)
plt.savefig('/work/nyxuspaper/anova_glcm_tune_graydepth_10-200.png', bbox_inches='tight', dpi=2*my_dpi) # 4x larger
plt.show()

