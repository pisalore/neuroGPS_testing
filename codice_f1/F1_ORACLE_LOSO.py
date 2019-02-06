from eval_perf import eval_perf
from markers.io import load_markers
import glob
import os
import time
GT_DIR = 'gt'
ERROR_DIR = 'error'
ERROR_DIR_LOSO = 'error_loso'
MAX_KEYS = 0
T = 0
R = 0
arg_max = []
TRESHOLDS = []
MIN_RADIUS = []
GT_NAMES = []
LOSO = []
MAX = 0


start = time.time()

for gt_marker_file_path in glob.glob(os.path.join(GT_DIR, 'x*.marker')):
    gt_filename = os.path.basename(gt_marker_file_path)
    GT_NAMES.append(gt_filename)
    C_TRUE = load_markers(gt_marker_file_path, from_vaa3d=True, check_coords=False, count_from_zero_flag=True)
    pred_filename = gt_filename.split('.')[0]
    F1 = {}

    for pred_marker_file_path in glob.glob(os.path.join('treshold/treshold_*/T*_R*', f"{pred_filename}_T*_R*.marker")):
        string = os.path.abspath(pred_marker_file_path)
        splitting = string.split("\\")
        print()
        value = splitting[9]
        print('Treshold and min. radius: ', splitting[9])
        C_pred = load_markers(pred_marker_file_path, from_vaa3d=True, check_coords=False, count_from_zero_flag=True)
        x = eval_perf(C_TRUE, C_pred, verbose=False, errors_marker_file=os.path.join(ERROR_DIR, f"error_{pred_filename}"),
                  rp_file=None, max_cell_diameter=20)

        F1.update({f"{value}" : x[2]})

    MAX_KEYS = list(max(zip(F1.values(), F1.keys())))
    arg_max.append(MAX_KEYS)
    split = MAX_KEYS[1].split('_')
    T = split[0]
    R = split[1]
    T = float(T[1:])
    R = float(R[1:])
    TRESHOLDS.append(T)
    MIN_RADIUS.append(R)
print()
end = time.time()
print('-----------------------------------------------------------------------------------------------')
print ('EXECUTION TIME (IN MINUTES) : {:02f}'.format((end - start) / 60))
print('-----------------------------------------------------------------------------------------------')
print()
print()
print('RESULTS OF ORACLE FUNCTION THAT FIND THE BEST TRESHOLDS AND MINIMUM RADIUS FOR EACH SUBSTACK OF 3D IMAGES:')
for i in range(GT_NAMES.__len__()):
    print('-----------------------------------------------------------------------------------------------')
    print('|SUBSTACK|:', GT_NAMES[i], '|TRESHOLD AND MIN RADIUS USED|:', arg_max[i][1], '|BEST F1|: {:0.2f}'.format(arg_max[i][0]) )
    print('-----------------------------------------------------------------------------------------------')
print()
count = []
for i in range(arg_max.__len__()):
   count.append(arg_max[i][0])
print('-----------------------------------------------------------------------------------------------')
print('BEST F1_ORACLE:', (max(count)))
print('-----------------------------------------------------------------------------------------------')
print('-----------------------------------------------------------------------------------------------')
print('WORST F1_ORACLE:', (min(count)))
print('-----------------------------------------------------------------------------------------------')
print('-----------------------------------------------------------------------------------------------')
print('AVERAGE F1_ORACLE:', (sum(count) / count.__len__()))
print('-----------------------------------------------------------------------------------------------')
print()
#LOSO
count_loso = []
for i in range(arg_max.__len__()):
    pred_filename = GT_NAMES[i]
    for j in range(arg_max.__len__()):
        if j != i:
            if MAX < arg_max[j][0]:
                MAX = arg_max[j][0]
                LOSO.clear()
                LOSO.append(arg_max[j])
    MAX = 0

    gt_marker_file_path = os.path.join(GT_DIR, pred_filename)
    C_TRUE = load_markers(gt_marker_file_path, from_vaa3d=True, check_coords=False, count_from_zero_flag=True)

    t_loso = LOSO[0][1].split('_')[0].split('T')[1]
    pred_marker_file_path = os.path.join('treshold/treshold_'f"{t_loso}"'/'f"{LOSO[0][1]}/", f"{os.path.basename(gt_marker_file_path).split('.')[0]}_"f"{LOSO[0][1]}"f"{'.marker'}")
    C_pred = load_markers(pred_marker_file_path, from_vaa3d=True, check_coords=False, count_from_zero_flag=True)
    print('-----------------------------------------------------------------------------------------------')
    print('LOSO FOR THE STACK:', GT_NAMES[i], '. CALCULATING F1 WITH TRESHOLD AND MIN RADIUS', LOSO[0][1])
    x = eval_perf(C_TRUE, C_pred, verbose=False, errors_marker_file=os.path.join(ERROR_DIR_LOSO, f"error_{pred_filename}"),
              rp_file=None, max_cell_diameter=20)
    count_loso.append(x[2])
    print('-----------------------------------------------------------------------------------------------')

print()
print('-----------------------------------------------------------------------------------------------')
print('BEST F1_LOSO:', (max(count_loso)))
print('-----------------------------------------------------------------------------------------------')
print('-----------------------------------------------------------------------------------------------')
print('WORST F1_LOSO:', (min(count_loso)))
print('-----------------------------------------------------------------------------------------------')
print('-----------------------------------------------------------------------------------------------')
print('AVERAGE F1_LOSO:', (sum(count_loso) / count_loso.__len__()))
print('-----------------------------------------------------------------------------------------------')
print()