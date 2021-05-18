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
