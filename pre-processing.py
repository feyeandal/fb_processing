import os
import geopandas as gpd
from geopandas.tools import sjoin
import fiona
from config import fpath
from config import input_path
from config import output_folder
from config import provinces

def make_output_folders(path): # Create function to create output folders
    try:
        os.makedirs(output_path, exist_ok = True)
    except Exception as e:
        print(e)

def filter_prov_bounds():
    imtwg_bounds_filter = imtwg_bounds[imtwg_bounds.PHCode_Pro==prov].index
    imtwg_bounds_filter_geom = imtwg_bounds.loc[imtwg_bounds_filter, 'geometry']
    imtwg_bounds_filter_geom_utm = imtwg_bounds_filter_geom.to_crs('EPSG:32651')
    imtwg_bounds_filter_geom_utm.to_file(os.path.abspath(os.path.join(folder_path, prov + '_bounds.shp')))

def filter_bgy_bounds():
    bgy_bounds_filter = bgy_bounds[bgy_bounds.Pro_Code==prov]
    bgy_bounds_filter.to_file(os.path.abspath(os.path.join(folder_path, prov + '_bgys.shp')))


# Read IMTWG provincial boundary
imtwg_bounds = gpd.read_file('Boundary_Province_Visual.shp')
bgy_bounds = gpd.read_file('bgys_utm.shp')

for prov in provinces:
    folder_path = os.path.join(fpath, 'input', prov) # Create the absolute path
    output_path = os.path.join(fpath, 'output', prov)
    make_output_folders(output_path)

    filter_prov_bounds()
    filter_bgy_bounds()

    for file in os.listdir(folder_path): # list all items in a dir
        if file.endswith('bounds.shp'):
            full_file_path = os.path.join(folder_path, file)
            out_file_path = os.path.join(output_path, file)
            read_bounds = full_file_path
            open_bounds = fiona.open(read_bounds)
            print(open_bounds)
            get_bounds = open_bounds.bounds
            print(get_bounds)

            # Clip Population TIF by extent
            clip_tif = "gdal_translate -projwin " + str(get_bounds[0]) +  " " + str(get_bounds[3]) + " " + str(get_bounds[2]) + " " + str(get_bounds[1]) + " -of GTiff FBPD_utm.tif " + folder_path + '/' + prov + "_clip.tif"
            os.system(clip_tif)
            
    for file in os.listdir(folder_path):   
        if file.endswith('_clip.tif'):
            full_file_path = os.path.join(folder_path, file)
            out_file_path = os.path.join(output_path, file)
            # Polygonize Clipped Provincial Population
            test_poly = "gdal_polygonize.py " + full_file_path + " " + folder_path + '/' + prov + "_pop_poly.gpkg -b 1 -f 'GPKG'"
            # print(test_poly)
            os.system(test_poly)
