import os
import geopandas as gpd
import fiona
from config import *

# Read IMTWG provincial boundary
imtwg_bounds = gpd.read_file('Boundary_Province_Visual.shp')
bgy_bounds = gpd.read_file('Barangay.shp')

for prov in provinces:
    folder_path = os.path.join(fpath, 'input', prov) # Create the absolute path
    output_path = os.path.join(fpath, 'output', prov)
    bgy_bounds_filter = bgy_bounds[bgy_bounds.Pro_Name==prov].index
    bgy_bounds_filter_geom = bgy_bounds.loc[bgy_bounds_filter, 'geometry']
    bgy_bounds_filter_geom_utm = bgy_bounds_filter_geom.to_crs('EPSG:32651')
    bgy_bounds_filter_geom_utm.to_file(folder_path + '/' + prov + '_bgys.shp')


    # Filter prov boundary according to the provinces and convert its projection
    imtwg_bounds_filter = imtwg_bounds[imtwg_bounds.Pro_Name==prov].index
    imtwg_bounds_filter_geom = imtwg_bounds.loc[imtwg_bounds_filter, 'geometry']
    imtwg_bounds_filter_geom_utm = imtwg_bounds_filter_geom.to_crs('EPSG:32651')
    imtwg_bounds_filter_geom_utm.to_file(folder_path + '/' + prov + '_bounds.shp')
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
            
    # for file in os.listdir(output_path):   
        if file.endswith('_clip.tif'):
            full_file_path = os.path.join(folder_path, file)
            out_file_path = os.path.join(output_path, file)
            # Polygonize Clipped Provincial Population
            test_poly = "gdal_polygonize.py " + out_file_path + " " + folder_path + '/' + prov + "_pop_poly.gpkg -b 1 -f 'GPKG'"
            os.system(test_poly)
