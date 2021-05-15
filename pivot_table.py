# Try to structure this script as functional
from functools import reduce
import pandas as pd
import geopandas as gpd
import numpy as np

# Try to not use this kind of import since it creates vague importing into the current namespace.
# For example, I can't find the provinces being used in the for loop explixcitly imported
from config import * 

for prov in provinces:
    folder_path = os.path.join(fpath, 'input', prov) # Create the absolute path
    output_path = os.path.join(fpath, 'output', prov)

    read_ssa = []
    read_lh = []
    read_fl = []

    # Let us refactor this code block . Remember, DRY! Do not Repeat Yourself
    for file in os.listdir(output_path): 
        if file.endswith('_SSA4_Bgy.shp'):
            print(file)
            out_file_path = os.path.join(output_path, file)
            read_ssa_out = gpd.read_file(out_file_path)
            affected_pivot = pd.pivot_table(read_ssa_out, values='Pop_Aff', index=['Bgy_Code', 'Bgy_Name', 'Pop2015', 'Mun_Code', 'Mun_Name', 'Pro_Code', 'Pro_Name', 'A1'], columns=['HAZ'], aggfunc=np.sum, fill_value=0)
            affected_pivot2 = affected_pivot.rename(columns = ({1: 'SSA4_Low', 2: 'SSA4_Moderate', 3: 'SSA4_High'}))
            # affected_pivot2.to_file('ssa.csv')
            read_ssa.append(affected_pivot2)
        
        elif file.endswith('LH_Bgy.shp'):
            # print(file)
            out_file_path = os.path.join(output_path, file)
            read_lh_out = gpd.read_file(out_file_path)
            affected_pivot = pd.pivot_table(read_lh_out, values='Pop_Aff', index=['Bgy_Code', 'Bgy_Name', 'Pop2015', 'Mun_Code', 'Mun_Name', 'Pro_Code', 'Pro_Name', 'A1'], columns=['LH'], aggfunc=np.sum, fill_value=0)
            affected_pivot2= affected_pivot.rename(columns = ({1: 'LH_Low', 2: 'LH_Moderate', 3: 'LH_High'}))
            read_lh.append(affected_pivot2)
        
        elif file.endswith('_Fl_Bgy.shp'):
            out_file_path = os.path.join(output_path, file)
            read_fl_out = gpd.read_file(out_file_path)
            affected_pivot = pd.pivot_table(read_fl_out, values='Pop_Aff', index=['Bgy_Code', 'Bgy_Name', 'Pop2015', 'Mun_Code', 'Mun_Name', 'Pro_Code', 'Pro_Name', 'A1'], columns=['HAZ'], aggfunc=np.sum, fill_value=0)
            affected_pivot2= affected_pivot.rename(columns = ({1: 'Fl_Low', 2: 'Fl_Moderate', 3: 'Fl_High'}))
            read_fl.append(affected_pivot2)

    for ssa in read_ssa:
        # print(ssa)
        for lh in read_lh:
            # print(lh)
            for fl in read_fl:
                print(fl)
                result = (pd.merge(pd.merge(ssa, lh, on=['Bgy_Code', 'Bgy_Name', 'Pop2015', 'Mun_Code', 'Mun_Name', 'Pro_Code', 'Pro_Name', 'A1']), fl, on=['Bgy_Code', 'Bgy_Name', 'Pop2015', 'Mun_Code', 'Mun_Name', 'Pro_Code', 'Pro_Name', 'A1']))
                print(result)
                result.to_csv(output_path + '/' + prov + '_affected.csv')

    # Create a data mapping to hold the columns per filetype and the array for the processed data
    file_type_mapping = {
        'SSA4_Bgy': {
            'columns': {1: 'SSA4_Low', 2: 'SSA4_Moderate', 3: 'SSA4_High'},
            'data': []
        },
        'LH_Bgy': {
            'columns': {1: 'LH_Low', 2: 'LH_Moderate', 3: 'LH_High'},
            'data': []
        },
        'Fl_Bgy': {
            'columns': {1: 'Fl_Low', 2: 'Fl_Moderate', 3: 'Fl_High'},
            'data': []
        }
    }

    def get_filetype_of_file(filename):
        """
            Function to get the filetype for a specific file
        """
        for filetype in file_type_mapping:
            if filetype in filename:
                return filetype
    
    def process_file(filetype):
        """
            Process a file
        """
        out_file_path = os.path.join(output_path, file)
        shapefile_df = gpd.read_file(out_file_path)

        # Rename LH column to HAZ to have uniformity
        shapefile_df.rename(columns={'LH': 'HAZ'})

        # Use multiline to improve readability of code
        affected_pivot = pd.pivot_table(
            shapefile_df, 
            index=['Bgy_Code', 'Bgy_Name', 'Pop2015', 'Mun_Code', 'Mun_Name', 'Pro_Code', 'Pro_Name', 'A1'],
            values='Pop_Aff',
            columns=['HAZ'],
            aggfunc=np.sum,
            fill_value=0
        )

        renamed_columns = affected_pivot.rename(columns=file_type_mapping[filetype]['columns'])
        file_type_mapping[filetype]['data'].append(renamed_columns)

    for file in os.listdir(output_path):
        if file.endswith('.shp'):
            filetype = get_filetype_of_file(file)
            process_file(filetype)

    # Create a list with all the results
    all_results = []
    for key in file_type_mapping:
        all_results+=file_type_mapping[key]['data']
    
    # Pa try neto
    # Apply function to every element of the array
    result = reduce(lambda df1,df2: pd.merge(
        df1,df2,on=['Bgy_Code', 'Bgy_Name', 'Pop2015', 'Mun_Code', 'Mun_Name', 'Pro_Code', 'Pro_Name', 'A1']
    ), all_results)
    result.to_csv(output_path + '/' + prov + '_affected.csv')

    # If not then uncomment this
    # for ssa in file_type_mapping['SSA4_Bgy']['data']:
    #     for lh in file_type_mapping['LH_Bgy']['data']:
    #         for fl in file_type_mapping['Fl_Bgy']['data']:
    #             print(fl)
    #             result = (pd.merge(pd.merge(ssa, lh, on=['Bgy_Code', 'Bgy_Name', 'Pop2015', 'Mun_Code', 'Mun_Name', 'Pro_Code', 'Pro_Name', 'A1']), fl, on=['Bgy_Code', 'Bgy_Name', 'Pop2015', 'Mun_Code', 'Mun_Name', 'Pro_Code', 'Pro_Name', 'A1']))
    #             print(result)
    #             result.to_csv(output_path + '/' + prov + '_affected.csv')


