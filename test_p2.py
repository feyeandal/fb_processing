import os
import geopandas as gpd
from config import *

def make_output_folders(path): # Create function to create output folders
    # make folder using path
    """Create output folders."""
    try:
        os.mkdir(output_folder)
    except Exception as e:
        print(e)
    
    try:
        os.mkdir(output_path)
    except Exception as e:
        print(e)

def pre_processing_data(output_path):
    """Does pre-processing to the input hazard files such as converting its projection to UTM, normalizing haz cols, fixing geometries,
    and dissolving shapes."""
    hazards_code = ['SSA', 'LH', 'Fl']
                # Convert haz file to UTM
    ssa_utm = read_haz.to_crs('EPSG:32651')
    for code in hazards_code:
        if code in haz:
            print('Converting haz files to UTM')
            ssa_utm.to_file(output_path + "/" + prov + '_' + code + '_utm.shp')
    # Rename all haz files column to 'HAZ' for consitency
    col_names = ['LH', 'VAR']
    for col in col_names:
        if col in ssa_utm.columns:
            ssa_utm = ssa_utm.rename(columns={col:'HAZ'})
    # Dissolve haz file by 'HAZ' attribute
    print('Dissolving haz files')
    haz_diss_filter = ssa_utm[['HAZ', 'geometry']]
    haz_diss_dissolve = haz_diss_filter.dissolve(by='HAZ')
    # Fix geometry of dissolved haz file by applying a buffer of 0
    haz_diss_buffer = haz_diss_dissolve.buffer(0)
    for code in hazards_code:
        if code in haz:
            haz_diss_buffer.to_file(output_path + "/" + prov + "_" + code + '_diss.shp')

def compute_area(output_path):
    """
    Dissolve intersected brgy data by barangay code.
    Also computes for the area of population per barangay.
    """
    pop_filter = read_int[['Bgy_Code', 'Bgy_Name', 'Pop2015', 'Mun_Code', 'Mun_Name', 'Pro_Code', 'Pro_Name', 'geometry']]
    pop_diss = pop_filter.dissolve(by='Bgy_Code')
    pop_diss["A1"] = pop_diss['geometry'].area
    pop_diss.to_file(output_path + '/' + prov + '_FB_Bgy.gpkg', driver='GPKG')
    return pop_diss

def compute_affected_ssa(df1, df2):
    """
    Compute affected population by SSA4 haz.
    """
    affected = gpd.overlay(df1, df2, how='intersection')
    affected["A2"] = affected['geometry'].area
    affected["aff"] = (affected['A2']/affected['A1'])
    affected["Pop_Aff"] = (affected['A2']/affected['A1']) * affected['Pop2015']
    i = 0
    affected.to_file(output_path + '/' + prov + '_SSA4_Bgy.shp')
    out_int = (output_path + '/' + prov + '_SSA4_Bgy.shp')
    while path.exists(out_int):
         out_int = (output_path + '/' + prov + '_SSA4_Bgy' + str(i) + '.shp')
         i += 1

def compute_affected_lh(df1, df2):
    """
    Compute affected population by Landslide haz.
    """
    affected = gpd.overlay(df1, df2, how='intersection')
    affected["A2"] = affected['geometry'].area
    affected["aff"] = (affected['A2']/affected['A1'])
    affected["Pop_Aff"] = (affected['A2']/affected['A1']) * affected['Pop2015']
    affected.to_file('Pampanga_LH_Bgy.shp')

def compute_affected_fl(df1, df2):
    """
    Compute affected population by 100-Year Flood haz.
    """
    affected = gpd.overlay(df1, df2, how='intersection')
    affected["A2"] = affected['geometry'].area
    affected["aff"] = (affected['A2']/affected['A1'])
    affected["Pop_Aff"] = (affected['A2']/affected['A1']) * affected['Pop2015']
    affected.to_file('Pampanga_Fl_Bgy.shp')

if __name__ == "__main__":
    for prov in provinces:
        folder_path = os.path.join(fpath, 'input', prov) # Create the absolute path
        output_path = os.path.join(fpath, 'output', prov)
        for file in os.listdir(folder_path):
            # print(file) # list all items in a dir
            # hazards = ['StormSurge_SSA4.shp', 'LH.shp']
            # for haz in hazards:
            #     if file.endswith(haz):
            #         full_file_path = os.path.join(folder_path, file)
            #         read_haz = gpd.read_file(full_file_path)
            #         pre_processing_data(output_path)
                
                if file.endswith('_inte.gpkg'):
                    full_file_path = os.path.join(folder_path, file)
                    # Compute for the area of a population per barangay (Calls the function)
                    read_int = gpd.read_file(full_file_path)
                    print('Computing for the area of population')
                    compute_area(output_path)

        compare_pop = []
        compare_ssa = []
        compare_lh = []
        compare_fl = []

        for file in os.listdir(output_path):
            if file.endswith('_FB_Bgy.gpkg'):
                out_file_path = os.path.join(output_path, file)
                read_pop = gpd.read_file(out_file_path)
                compare_pop.append(read_pop)

            elif file.endswith('_SSA_diss.shp'):
                out_file_path = os.path.join(output_path, file)
                read_haz = gpd.read_file(out_file_path)
                compare_ssa.append(read_haz)
            
            elif file.endswith('_LH_diss.shp'):
                out_file_path = os.path.join(output_path, file)
                read_haz = gpd.read_file(out_file_path)
                compare_ssa.append(read_haz)

            elif file.endswith('_Fl_diss.shp'):
                out_file_path = os.path.join(output_path, file)
                read_haz = gpd.read_file(out_file_path)
                compare_fl.append(read_haz)

        # Compute affected pop from the dataframes
        for pop in compare_pop:
            for ssa in compare_ssa:
                print('Computing affected pop area by SSA4')
                compute_affected_ssa(pop, ssa)
            # for lh in compare_lh:
                # print('Computing affected pop area by LH')
            #     compute_affected_lh(pop, lh)
            # for fl in compare_fl:
                # print('Computing affected pop area by Flood')
            #     compute_affected_fl(pop, fl)
    print('Processing Done.')
