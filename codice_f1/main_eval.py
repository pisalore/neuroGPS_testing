import glob
import os

import numpy as np
from ann.imtensor import load_tensor_from_tif
from markers.io import load_markers
from markers.center import CenterList, Center
from variables import  PADDING_MS, PADDING424242
from utils import model_hash_and_meta
from eval_perf import eval_perf


def perf_str(comment, TP, FP, FN):
    PREC = TP / (TP + FP + 1e-6)
    RECALL = TP / (TP + FN + 1e-6)
    F1 = (2 * TP) / (2 * TP + FP + FN + 1e-6)
    print('{} >>> prec {:.3f} recall {:.3f} F1 {:.3f} TP {:d} FP {:d} FN {:d}'.format(comment, PREC, RECALL, F1, TP, FP, FN))


def main_eval(args):

    model_hash, model_meta = model_hash_and_meta(args.model_dir, args.mb_idx)
    working_dir = args.working_dir

    # if args.gt_dir is None:
    TP_all, FP_all, FN_all = 0, 0, 0
    for brainid, ssid, TP, FP, FN in main_eval_helper_gen(working_dir, working_dir, model_hash):
        TP_all += TP
        FP_all += FP
        FN_all += FN
    PREC_all = TP_all / (TP_all + FP_all + 1e-6)
    RECALL_all = TP_all / (TP_all + FN_all + 1e-6)
    F1_all = 2 * TP_all / (2 * TP_all + FP_all + FN_all + 1e-6)
    print('TOTAL: prec {:.3f} recall {:.3f} F1 {:.3f} TP {:d} FP {:d} FN {:d}'.format(PREC_all, RECALL_all, F1_all,
                                                                                      TP_all, FP_all, FN_all))


def main_eval_helper_gen(working_dir, gt_dir, model_hash):
    for substack_path in glob.iglob(os.path.join(working_dir, '*', 'x*_y*_z*')):
        rest, ssid = os.path.split(substack_path)
        secondary_working_dir, brainid = os.path.split(rest)
        gt_markers = glob.glob(os.path.join(gt_dir, brainid, ssid, 'x*_y*_z*.marker'))

        if not gt_markers:
            print('No ground truth for {}'.format(substack_path))
            continue

        deconv_dir = os.path.join(substack_path, 'deconv', 'model_{}'.format(model_hash))

        gt_marker_filename, = gt_markers
        ms_marker_filename = os.path.join(deconv_dir, 'ms.marker')
        # if not os.path.exists(ms_marker_filename): continue  # TODO remove
        error_marker_filename = os.path.join(deconv_dir, 'error.marker')
        print('GT: ', gt_marker_filename)
        print('MS: ', ms_marker_filename)
        print()

        assert os.path.exists(gt_marker_filename), gt_marker_filename
        assert os.path.exists(ms_marker_filename), ms_marker_filename


        C_true = load_markers(
            gt_marker_filename,
            from_vaa3d=True,
            count_from_zero_flag=True,
            check_coords=False
        )

        C_pred = load_markers(
            ms_marker_filename,
            from_vaa3d=True,
            count_from_zero_flag=True,
            check_coords=False
        )
        for c in C_pred:
            c.name = 'ms'

        precision, recall, F1, TP_inside, FP_inside, FN_inside = eval_perf(
            C_true,
            C_pred,
            verbose=True,
            errors_marker_file=error_marker_filename,
            rp_file=None,
            max_cell_diameter=20
        )
        TP = len(TP_inside)
        FP = len(FP_inside)
        FN = len(FN_inside)

        print('prec {:.3f} recall {:.3f} F1 {:.3f} TP {:d} FP {:d} FN {:d} SS {}'.format(precision, recall, F1, TP,  FP, FN, substack_path))
        yield brainid, ssid, TP, FP, FN





