# COPC Processing with PDAL, Python, and Dask

## Installation

* Install Conda environment


```
conda env create -n copc-dem -f environment.yml
```

* Install PDAL `master`

* Install PDAL Python `master`

* Install COPC-DEM

```
pip install -e .
```

```
mkdir dtm
copc_dem autzen-classified.copc.laz --debug -threshold 2000000 -read_resolution 0 -write_resolution 1 -window_size=0
```

```
find dtm -iname '*.tif' > file-list
gdalbuildvrt -input_file_list file-list dtm.vrt -r bilinear
gdaldem hillshade dtm.vrt hillshade.png
open hillshade.png
```