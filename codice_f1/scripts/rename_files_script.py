import glob
import os

#rinomino tutti i file che vengono creati da glob_marker_script da .swc_definitiVe_marker a nome_volume_T*R*. Il problema
#è che ho dovuto cambiare a mano i volumi, devo riuscire ad automatizzare il processo. In ogni caso, adesso ho i file ordinati.
#posso fare come in F1_LOSO, ovvero creando una lista con tutti i nomi delle gt e ciclare su quella.

V1 = "x000938"
V2 = "x004647"
V3 = "x004649"
V4 = "x005415"
V5 = "x006319"
V6 = "x006782"
V7 = "x007038"
V8 = "x010194"
V9 = "x010600"
V10 = "x010605"
V11 = "x011270"
V12 = "x013315"
V13 = "x013442"

for pred_file_path in glob.glob(os.path.join('treshold/treshold_*/T*_R*', f"{V1}.swc_definitive.marker")):
    print(os.path.abspath(pred_file_path))
    save_path = os.path.split(os.path.abspath(pred_file_path))[0]
    print(save_path)
    string = os.path.abspath(pred_file_path)
    splitting = string.split("\\")
    add = '_' + str(splitting[8]) + '.marker'
    print(str(splitting[8]))
#V1
    print(os.path.basename(pred_file_path))
    old_file = os.path.join(save_path, f"{V1}.swc_definitive.marker")
    new_file = os.path.join(save_path, V1 + add)
    os.rename(old_file, new_file)

for file_path in glob.glob(os.path.join('treshold/treshold_*/T*_R*', 'x*.swc.marker')):
    print (os.path.abspath(file_path))
    os.remove(os.path.abspath(file_path))
