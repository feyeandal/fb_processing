# Facebook Population Processing Tool Using FOSS

This document contains the workflow for the processing of the Facebook Population Density Data and the NOAH hazard maps to compute for the total area of population and the area of affected population per hazard level. Open-source tools like Python, GeoPandas, Fiona, GDaL, and QGIS will be used for this methodology.

## Dependencies:

- Python 3.9.1 or higher
- Python `os`
- Python `geopandas 0.9.0`
- Python `fiona 1.8.19`
- Python `pandas 1.2.1`
- Python `numpy 1.19.5`
- GDAL
- QGIS 3 or higher

## Installation:

All of the mentioned tools above are mandatory, so make sure that you have properly set-up everything before you run the scripts.

1. Install `Python 3.9.1` or higher on your machine. You may check this [link](https://www.python.org/downloads/) for the active Python releases. Alternatively, you may install `Anaconda` Python distribution. This already contains packages for GDAL (that is also required for this set-up). Check this [link](https://docs.conda.io/projects/conda/en/latest/user-guide/install/windows.html) to download and install Anaconda.
2. Download `pip` on your machine. For Windows users, check this [guide](https://phoenixnap.com/kb/install-pip-windows#ftoc-heading-3).
3. Download `GDAL` and other dependencies mentioned on your machine. GDAL is a translator library for raster and vector spatial data formats. We will be using GDAL to process the raster data from Facebook. Check this [link](https://www.lfd.uci.edu/~gohlke/pythonlibs/) to download.
4. Once everything is downloaded on your machine, we need to tell your OS where the python and pip installations are located. We need to add some system variables on your python path.
5. Install the dependencies by doing: `pip install file.whl`.
6. For Anaconda users, you may install GDAL by running `conda create -n gdal_env -c conda-forge gdal` on your conda terminal.

## Data Processing

The processing of the data is divided into three methods:

1. Pre-processing of the data (Part 1). This involves clipping the population density (raster) to your assigned province and converting the clipped population density to a vector format using a python script.
2. Pre-processing of the data (Part 2). This method involves using QGIS model builder to be able to run fix geometries of the converted population density data and intersect this with the barangay boundaries containing the 2015 census data.
3. Processing of the population and hazard data. This part involves computation of the area of population per barangay and the area of affected population per hazard level. This will be used to compute the total affected population per hazard. This part will be ran using a python script.
4. Generation of pivot table. This contains a pivot table of the computation generated from the processing script.

## Data Requirements:

To be able to conduct this process, you need to prepare the following data:

1. ![IMTWG Provincial Boundary](https://drive.google.com/drive/folders/1bVsda5GlkLlbmS2yFIsCW-rpGGJTfah-) (Boundary_Province_Visual.shp). *No need to rename/reproject the file*.
2. ![Facebook Population Density Data](https://drive.google.com/drive/folders/1RS10GnXL1dZzvAZPE_DL0JqF3yxKE7sm) (FBPD_utm.tif) *This is already reprojected to UTM so no need to reproject. Please do not rename the file as well.*
3. ![Barangay Boundaries with 2015 Census](https://drive.google.com/drive/folders/1f0fSX41nJ9BwwQiYJ1G6ZxEmhuLH3sW3) (bgys_utm.shp)
4. Hazard (SSA4, Landslide Hazards, and 100-Year Flood) per province. Name it as: `Province_StormSurge_SSA4.shp`, `Province_Fl.shp`, `Province_LH.shp`

## Folder Configuration:

The python scripts are modeled to read input files and produce output files in a structured format. Hence, you need to follow the steps below.

1. Download the python scripts and the model builder from this link.
2. On your machine, identify where you will place the python scripts and the input files (data required). All of these data must be stored on your base folder path.

    e.g. `/Users/localUser/UPRI/FacebookProcessing`

3. Insider this base folder path, create the following folders:
    - `input`
        - `Province 1`
        - `Province 2`
        - `Province 3`

When naming the `Province` folders, make sure to name it according to the `Pro_Name` column of the IMTWG Provincial Boundaries data. Failure to name it in this format will cause the Pre-Processing script to fail.

All output files will be stored separately on the designated `Province` folder inside the `output` folder. These folders are automatically generated from the script.

Your folder configuration should look similar to this:

`/Users/localUser/UPRI/FacebookProcessing`

- config.py
- pre-processing.py
- processing.py
- pivot_table.py
- `input`
    - `Province 1`
        - SSA4
        - LH
        - Fl
    - `Province 2`
        - SSA4
        - LH
        - Fl
    - `Province 3`
        - SSA4
        - LH
        - Fl
- `output` *(only generated when you ran the script)*
    - `Province 1`
    - `Province 2`
    - `Province 3`

## Pre-processing of the data (Part 1)

1. On your terminal (cmd prompt/ conda), go to your base folder path. Run `cd /Users/localUser/UPRI/FacebookProcessing`
2. Run `python pre-processing.py` to generate the clipped population density data and the polygonized population density data.
3. If successfully ran, your terminal should look similar like this:
4. Check your `input` > `Province` folders for the generated files:
    - `Province_clip.tif`- clipped population data according to province
    - `Province_pop_poly.gpkg` - polygonized population data
    - `Province_bounds.shp` - provincial boundary
    - `Province_bgys.shp` - barangay boundary for this province

## Pre-processing of the data (Part 2)

In this step, you will be needing to run the pre-processing tool using QGIS. This model is designed to process only one province at once so this might take some time.

1. Open QGIS.
2. Go to `Processing` > `Graphical Modeler` > `Open` > `pre-processing_2.model3` > `Open`
3. Double-click the `Fix Geometries` algorithm and select the `Input Layer` as the `_poly.gpkg` from your `Input` > `Province` folder. This is one of the output files from the Pre-processing Part 1.
4. In the `Intersection` algorithm, set the `Input Layer` as the barangay boundaries (`_bgys1.shp`) from your `Input` > `Province` folder. 
5. Click `Run model` to start the processing. 

![Graphic modeler for QGIS](https://raw.githubusercontent.com/feyeandal/photos/master/pre_processing.png)

6. You will be asked for the output path and file for `out_inte`. Name it as `Province 1_inte.gpkg` then click `Run`.

7. Wait for it to finish running and processing.

## Processing of the population and hazard data

Once you have completed the first two pre-processing steps, you are now ready to proceed with the processing method.

1. On your terminal, run `python processing.py`
2. The intersection may take a while especially if you have large input files size. Wait for it to finish running and check the output files from the `output` > `Province` folders.
3. Your `output` > `Province` folder should contain the following:
    - `Province_Haz_utm.shp` - reprojected hazard to UTM
    - `Province_Haz_diss.shp` - dissolved version of the reprojected hazard
    - `Province_Haz_Bgy.shp` - intersected vector of the dissolved hazard vector and the polygonized population data. This contains the computation of area of population, area of hazard, and number of affected population that is aggregated per barangay

## Generation of pivot table for summary

1. Run `python pivot_table.py` on your terminal.
2. Check your `output` > `Province` folder and open the generated pivot table (`_affected.csv`).
