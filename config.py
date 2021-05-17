import os

fpath = os.path.dirname(os.path.abspath(__file__)) # Gate the root path of the file

print(fpath)

input_path = os.path.join(fpath, 'input')
print(input_path)
output_folder = os.path.join(fpath, 'output')
print(output_folder)
provinces = os.listdir(input_path)
print(provinces)

try:
    os.makedirs(output_folder, exist_ok = True)
except Exception as e:
    print(e)
    
for prov in provinces:
    folder_path = os.path.join(fpath, 'input', prov) # Create the absolute path
    # print(folder_path)
    files_all = os.listdir(folder_path)
    # print(files_all)
    haz_files = [os.path.join(folder_path, file) for file in files_all if ".shp" in file]
    # print(haz_files)
    # print(file)
    haz_files = [os.path.join(folder_path, file) for file in files_all if ".gpkg" in file]
    output_path = os.path.join(fpath, 'output', prov)
    try:
        os.makedirs(output_path, exist_ok = True)
    except Exception as e:
        print(e)
    print(output_path)
for file in os.listdir(folder_path):
    full_file_path = os.path.join(folder_path, file)
    out_file_path = os.path.join(output_path, file)
    files_all_out = os.listdir(output_path)
    haz_files_out = [os.path.join(output_path, file) for file in files_all if ".shp" in file]   
