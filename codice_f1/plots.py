from eval_perf import eval_perf
from markers.io import load_markers
import glob
import os
import matplotlib.pyplot as plt
import numpy as np
GT_DIR = 'gt'
ERROR_DIR = 'error'
PRECISION = []
RECALL = []
F1 = []

for gt_marker_file_path in glob.glob(os.path.join(GT_DIR, 'x000938.marker')):
    gt_filename = os.path.basename(gt_marker_file_path)
    C_TRUE = load_markers(gt_marker_file_path, from_vaa3d=True, check_coords=False, count_from_zero_flag=True)
    pred_filename = gt_filename.split('.')[0]
    print(pred_filename)

    for i in range(1,10):
        print(i)
        pred_marker_file_path = os.path.join('treshold/treshold_6/T6_R'f"{i}/", f"{pred_filename}_T6_R"f"{i}"f"{'.marker'}")
        print(pred_marker_file_path)
        C_pred = load_markers(pred_marker_file_path, from_vaa3d=True, check_coords=False, count_from_zero_flag=True)
        x = eval_perf(C_TRUE, C_pred, verbose=False,
                      errors_marker_file=os.path.join(ERROR_DIR, f"error_{pred_filename}"),
                      rp_file=None, max_cell_diameter=20)
        PRECISION.append(x[0])
        RECALL.append(x[1])
        F1.append(x[2])

    print(PRECISION)
    print(F1)
    print(RECALL)
RADIUS = [1,2,3,4,5,6,7,8,9]


# Data for plotting


fig, ax = plt.subplots()
ax.plot(RADIUS, F1)
ax.plot(RADIUS, RECALL)
ax.plot(RADIUS, PRECISION)

ax.set(xlabel='MIN RADIUS', ylabel='PERCENTAGE', title='F1, PRECISION AND RECALL FOR TRESHOLD = 6')
plt.legend(['F1', 'RECALL', 'PRECISION'], loc='lower left')


plt.show()