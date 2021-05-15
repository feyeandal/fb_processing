import pandas as pd
import geopandas as gpd
import numpy as np
from config import *

for prov in provinces:
    folder_path = os.path.join(fpath, 'input', prov) # Create the absolute path
    output_path = os.path.join(fpath, 'output', prov)

    read_ssa = []
    read_lh = []
    read_fl = []

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
        print(ssa)
        for lh in read_lh:
            print(lh)
            for fl in read_fl:
                print('flood')
                print(fl)
                # result = (pd.merge(pd.merge(lh, ssa, on=['Bgy_Code', 'Bgy_Name', 'Pop2015', 'Mun_Code', 'Mun_Name', 'Pro_Code', 'Pro_Name', 'A1']), fl, on=['Bgy_Code', 'Bgy_Name', 'Pop2015', 'Mun_Code', 'Mun_Name', 'Pro_Code', 'Pro_Name', 'A1']))
                result = (lh.merge(ssa, on=['Bgy_Name', 'Pop2015', 'Mun_Code', 'Mun_Name', 'Pro_Code', 'Pro_Name', 'A1'], how='outer')).merge(fl, on=['Bgy_Name', 'Pop2015', 'Mun_Code', 'Mun_Name', 'Pro_Code', 'Pro_Name', 'A1'], how='outer')
                # result2 = result.merge(fl, on=['Bgy_Name', 'Pop2015', 'Mun_Code', 'Mun_Name', 'Pro_Code', 'Pro_Name', 'A1'], how='outer')
                # result23 = result2.drop(['_merge'], axis=1, inplace=True, errors='ignore')
                # print(result2)
                # .query('_merge != "both"').drop('_merge', 1)
                result.to_csv(output_path + '/' + prov + '_affected.csv')
