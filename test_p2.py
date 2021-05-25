import os
import geopandas as gpd
from config import fpath
from config import input_path
from config import output_folder
from config import provinces

def make_output_folders(path): # Create function to create output folders
    # make folder using path
    """
    Create output folders.
    """
    try:
        os.makedirs(output_path, exist_ok = True)
    except Exception as e:
        print(e)

def pre_processing_data(output_path):
    """
    Does pre-processing to the input hazard files such as converting its projection to UTM, normalizing haz cols, fixing geometries,
    and dissolving shapes.
    """
    hazards_code = ['SSA', 'Fl', 'LH']
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
            # Here change creation of path using abspath and .join
            haz_diss_buffer.to_file(output_path + "/" + prov + "_" + code + '_diss.shp')

def compute_area(output_path):
    """
    Dissolve intersected brgy data by barangay code.
    Also computes for the area of population per barangay.
    """
    # San galing si read_int? Di naman sya na declare as parameter ni function. It should be declared before being
    # used inside the scope of this function 
    pop_filter = read_int[['Bgy_Code', 'Bgy_Name', 'Pop2015', 'Mun_Code', 'Mun_Name', 'Pro_Code', 'Pro_Name', 'geometry']]
    pop_diss = pop_filter.dissolve(by='Bgy_Code')
    pop_diss["A1"] = pop_diss['geometry'].area
    # Here change creation of path using abspath and .join
    pop_diss.to_file(output_path + '/' + prov + '_FB_Bgy.gpkg', driver='GPKG')
    return pop_diss

def compute_affected(df1, df2):
    """
    Compute affected population by SSA4 haz.
    """
    hazards_code = ['SSA', 'Fl', 'LH']
    affected = gpd.overlay(ssa, pop, how='intersection')
    affected["A2"] = affected['geometry'].area
    affected["aff"] = (affected['A2']/affected['A1'])
    affected["Pop_Aff"] = (affected['A2']/affected['A1']) * affected['Pop2015']
    for hazard in hazards_code:
        if hazard in filed:
            # Here change creation of path using abspath and .join
            affected.to_file(output_path + '/' + prov + "_" + hazard + '_Bgy.shp')

if __name__ == "__main__":
    for prov in provinces:
        # Add os.path.abspath to joins kasi magkaka error sa windows
        folder_path = os.path.abspath(os.path.join(fpath, 'input', prov)) # Create the absolute path
        output_path = os.path.abspath(os.path.join(fpath, 'output', prov))
        make_output_folders(output_path)

        for file in os.listdir(folder_path):
            # print(file) # list all items in a dir
            hazards = ['StormSurge_SSA4.shp', 'Fl.shp', 'LH.shp']
            for haz in hazards:
                if file.endswith(haz):
                    full_file_path = os.path.join(folder_path, file)
                    read_haz = gpd.read_file(full_file_path)
                    print('Pre-processing the haz data')
                    pre_processing_data(output_path)
                
                if file.endswith('_inte.gpkg'):
                    full_file_path = os.path.join(folder_path, file)
                    # Compute for the area of a population per barangay (Calls the function)
                    read_int = gpd.read_file(full_file_path)
                    print('Computing for the area of population')
                    compute_area(output_path)

        compare_pop = []
        compare_ssa = []
        filename_t = []

        for file in os.listdir(output_path):
            filenametype = ['_SSA_diss.shp', '_Fl_diss.shp', '_LH_diss.shp']
            if file.endswith('_FB_Bgy.gpkg'):
                # print(file)
                out_file_path = os.path.join(output_path, file)
                read_pop = gpd.read_file(out_file_path)
                compare_pop.append(read_pop)

            for filename in filenametype:
                # print(filename)
                if file.endswith(filename):
                    # print(file)
                    out_file_path = os.path.join(output_path, file)
                    # print(out_file_path)
                    read_haz = gpd.read_file(out_file_path)
                    filename_t.append(file)
                    compare_ssa.append(read_haz)

        hazards_code = ['SSA', 'Fl', 'LH']
        for filed in filename_t:
            print(filed)
            print('Computing for affected population')
            # print(filed)
            for ssa in compare_ssa:
                # print(ssa)
                for pop in compare_pop:
                    compute_affected(ssa, pop)
       
    print('Processing Done.')
