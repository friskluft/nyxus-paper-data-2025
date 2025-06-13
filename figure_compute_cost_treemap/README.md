# Compute cost GPU vs non-GPU

![](logo_figure_computecosttreemap.jpg)

## Workflow:

(1) assuming a benchmark is in file /work/benchmark1.csv

(2) pull the renderer from github.com/friskluft/vhrend

(3) using R, execute 
```r
source("vthie_df_2_tree.r")

source("vthie_df_2_tree.r")

vthie_render (datafname="/work/benchmark1", outfname="/work/benchmark1.html")
```

(4) using a browser, open file /work/benchmark1.html

(5) print it to a PDF

(6) use the PDF file as a graphics file in PowerPoint or LaTeX to prepare a figure (clip the PDF-provided graphics, add callouts, etc.)

