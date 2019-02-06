from eval_perf import eval_perf
from markers.io import load_markers
import glob
import os
GT_DIR = 'gt'
PRED_DIR = 'pred'
ERROR_DIR = 'error'

if not os.path.exists(ERROR_DIR):
    os.makedirs(ERROR_DIR)

for gt_marker_file_path in glob.glob(os.path.join(GT_DIR, 'gt_000938.marker')):
    C_true = load_markers(gt_marker_file_path, from_vaa3d=True, check_coords=False, count_from_zero_flag=True)
    gt_filename = os.path.basename(gt_marker_file_path)
    print(gt_filename)
    pred_filename = "_".join(gt_filename.split('_')[1:])
    pred_marker_file_path = os.path.join(PRED_DIR, pred_filename)
    C_pred = load_markers(pred_marker_file_path, from_vaa3d=True, check_coords=False, count_from_zero_flag=True)
    eval_perf(C_true, C_pred, verbose=False, errors_marker_file=os.path.join(ERROR_DIR, f"error_{pred_filename}"),
              rp_file=None,  max_cell_diameter=20)

