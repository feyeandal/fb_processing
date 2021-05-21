import os
import pandas as pd
import geopandas as gpd
import numpy as np
from config import fpath
from config import input_path
from config import output_folder
from config import provinces

def make_output_folders(path): # Create function to create output folders
    """
    Create output folders.
    """
    try:
        os.makedirs(output_path, exist_ok = True)
    except Exception as e:
        print(e)

def get_filetype_of_file():
    """
    Function to get the filetype for a specific file.
    """
    for filetype in file_type_mapping:
        if filetype in file:
            for f in filetypem:
                if f in filetype:
                    return file

def process_file(filetype):
    """
    Process the file for pivot.
    """
    out_file_path = os.path.join(output_path, file)
    shapefile_df = gpd.read_file(out_file_path)

    # Pivot the table
    affected_pivot = pd.pivot_table(
        shapefile_df, 
        index=['Bgy_Code', 'Bgy_Name', 'Pop2015', 'Mun_Code', 'Mun_Name', 'Pro_Code', 'Pro_Name', 'A1'],
        values='Pop_Aff',
        columns=['HAZ'],
        aggfunc=np.sum,
        fill_value=0
    )

    renamed_columns = affected_pivot.rename(columns=file_type_mapping[code]['columns'])
    file_type_mapping[code]['data'].append(renamed_columns)

if __name__ == "__main__":
    for prov in provinces:
        folder_path = os.path.join(fpath, 'input', prov) # Create the absolute path
        output_path = os.path.join(fpath, 'output', prov)
        make_output_folders(output_path)

        file_type_mapping = {
        'SSA_affected': {
            'columns': {1: 'SSA4_Low', 2: 'SSA4_Moderate', 3: 'SSA4_High'},
            'data': []
        },
        'LH_affected': {
            'columns': {1: 'LH_Low', 2: 'LH_Moderate', 3: 'LH_High'},
            'data': []
        },
        'Fl_affected': {
            'columns': {1: 'Fl_Low', 2: 'Fl_Moderate', 3: 'Fl_High'},
            'data': []
        }
        }
        
        filetype_code = ['SSA_affected', 'LH_affected', 'Fl_affected']

        for file in os.listdir(output_path):
            if file.endswith('.shp'):
                for filetype in file_type_mapping:
                    if filetype in file:
                        for code in filetype_code:
                            if code in filetype:
                                print(file)
                                process_file(file)


        all_results = []
        for key in file_type_mapping:
            all_results+=file_type_mapping[key]['data']

        for ssa in file_type_mapping['SSA_affected']['data']:
            print(ssa)
            for lh in file_type_mapping['LH_affected']['data']:
                print(lh)
                for fl in file_type_mapping['Fl_affected']['data']:
                    print(fl)
                    result = (lh.merge(ssa,
                    on=['Bgy_Name', 'Pop2015', 'Mun_Code', 'Mun_Name', 'Pro_Code', 'Pro_Name', 'A1'], 
                    how='outer')).merge(fl,
                    on=['Bgy_Name', 'Pop2015', 'Mun_Code', 'Mun_Name', 'Pro_Code', 'Pro_Name', 'A1'], 
                    how='outer')
                    print(result)
                    result.to_csv(output_path + '/' + prov + '_affected.csv')
