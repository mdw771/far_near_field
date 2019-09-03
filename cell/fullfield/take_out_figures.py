import os
import glob
import shutil

folder_list = glob.glob('n*e*')
folder_list = [f for f in folder_list if os.path.isdir(f)]
folder_list.sort()
print(folder_list)

for f in folder_list:
    dest_fname = 'fullfield_p_{}.tiff'.format(f)
    print(dest_fname)
    try:
        shutil.copyfile(os.path.join(f, dest_fname), dest_fname)
    except:
        shutil.copyfile(os.path.join(f, 'delta_ds_1.tiff'), dest_fname)