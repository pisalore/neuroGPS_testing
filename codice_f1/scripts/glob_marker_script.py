import os
import glob

for pred_swc_file_path in glob.glob(os.path.join('treshold/treshold_*/T*_R*', 'x*.swc')):
    print (os.path.abspath(pred_swc_file_path))
    split = os.path.split(os.path.abspath(pred_swc_file_path))
    save_path = split[0]
    marker_file_name = os.path.abspath(pred_swc_file_path)
    completeName = os.path.join(save_path, f"{marker_file_name}.marker")
    swc_file = open(f"{marker_file_name}", 'r+')
    file1 = open(completeName, "w+")
    definitiveName = os.path.join(save_path, f"{marker_file_name}_definitive.marker")
    definitive_marker_file = open(definitiveName, "w+")
    definitive_marker_file.write('#x, y, z, radius, shape, name, comment \n') #header


    lines1 = swc_file.readlines()
    str1 = []

    for i in range(0, lines1.__len__()):
        lines1[i] = lines1[i].replace('-1', '1,,')
        lines1[i] = lines1[i].split()
        lines1[i] = lines1[i][2:7]  # x,y,z,raggio,commento
        str1.append(','.join(lines1[i]))
        file1.write(str1[i])
        file1.write('\n')

    str = []

    for i in range(0, lines1.__len__()):
        lines1[i] = lines1[i][0:6]
        lines1[i][1] = 458 - float(lines1[i][1])
        lines1[i][1] = repr(lines1[i][1])
        str.append(','.join(lines1[i]))
        definitive_marker_file.write(str[i])
        definitive_marker_file.write('\n')




