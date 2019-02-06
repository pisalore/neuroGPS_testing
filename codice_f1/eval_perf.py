from markers.matching import distance, match_markers
from markers.matching import distance, match_markers


def eval_perf(C_true, C_pred, verbose=True, errors_marker_file=None, rp_file=None, max_cell_diameter=None):
    # max-cardinality bipartite matching
    C_true = list(C_true)
    C_pred = list(C_pred)

    true_positives_true = set()  # subset of C_true that are true positives
    true_positives_pred = set()  # subset of C_pred that are true positives
    TP = 0
    TP_inside = []
    G, mate, node2center = match_markers(C_true, C_pred, 2 * max_cell_diameter, verbose=True)
    kw = 0
    for k1, k2 in mate.items():
        if k1[0] == 'p':  # mate is symmetric
            continue
        c1 = node2center[k1]
        c2 = node2center[k2]
        d = distance((c1.x, c1.y, c1.z), (c2.x, c2.y, c2.z))
        if d < max_cell_diameter / 2:
            true_positives_pred.add(c2)
            true_positives_true.add(c1)
            TP += 1
            # assert _is_inside_margin(substack, c1):
            if verbose:
                print(' TP:', k2, c2.name, c2.x, c2.y, c2.z, c2, k1,
                      c1.name, c1.x, c1.y, c1.z, d)
            TP_inside.append(c2)
            kw += 1
        else:
            if verbose:
                print('---> too far', c2.name, c2.x, c2.y, c2.z, c2, c1.name,
                      c1.x, c1.y, c1.z, d)

    FP_inside, FN_inside = [], []
    if errors_marker_file is not None:
        ostream = open(errors_marker_file, 'w')
        print(
            '##x,y,z,radius,shape,name,comment, color_r,color_g,color_b',
            file=ostream)

    for i, c in enumerate(C_true):
        if c not in true_positives_true:
            # assert _is_inside_margin(substack, c):
            r, g, b = 255, 0, 255
            name = 'FN_%03d' % (i + 1,)
            cx, cy, cz = int(round(c.x)), int(round(c.y)), int(round(c.z))
            comment = ':'.join(map(str, [cx, cy, cz, c]))
            if errors_marker_file is not None:
                print(
                    ','.join(
                        map(str,
                            [cx, cy, cz, 0, 1, name, comment, r, g, b])),
                    file=ostream)
            FN_inside.append(c)
            if verbose:
                print('FN: ', c.name, c.x, c.y, c.z, c)
    for i, c in enumerate(C_pred):
        c.is_false_positive = False
        if c not in true_positives_pred:
            # assert _is_inside_margin(substack, c):
            r, g, b = 255, 0, 0
            name = 'FP_%03d' % (i + 1,)
            c.is_false_positive = True
            cx, cy, cz = int(round(c.x)), int(round(c.y)), int(round(c.z))
            comment = ':'.join(map(str, [cx, cy, cz, c]))
            if errors_marker_file is not None:
                print(
                    ','.join(
                        map(str, [
                            1 + cx, 1 + cy, 1 + cz, 0, 1, name, comment, r,
                            g, b
                        ])),
                    file=ostream)
            FP_inside.append(c)
            if verbose:
                print('FP: ', c.name, c.x, c.y, c.z, c)
    # Also print predicted TP in error marker file (helps debugging)
    for i, c in enumerate(C_pred):
        if c in true_positives_pred:
            # assert _is_inside_margin(substack, c):
            r, g, b = 0, 255, 0
            name = 'TP_%03d' % (i + 1,)
            cx, cy, cz = int(round(c.x)), int(round(c.y)), int(round(c.z))
            comment = ':'.join(map(str, [cx, cy, cz, c]))
            if errors_marker_file is not None:
                print(
                    ','.join(
                        map(str, [
                            1 + cx, 1 + cy, 1 + cz, 0, 1, name, comment, r,
                            g, b
                        ])),
                    file=ostream)

    # Also print true TP in error marker file (helps debugging)
    for i, c in enumerate(C_true):
        if c in true_positives_true:
            # assert _is_inside_margin(substack, c):
            r, g, b = 0, 255, 255
            name = 'TP_%03d' % (i + 1,)
            cx, cy, cz = int(round(c.x)), int(round(c.y)), int(round(c.z))
            comment = ':'.join(map(str, [cx, cy, cz, c]))
            if errors_marker_file is not None:
                print(
                    ','.join(
                        map(str, [
                            1 + cx, 1 + cy, 1 + cz, 0, 1, name, comment, r,
                            g, b
                        ])),
                    file=ostream)

    # # Finally, print rejected predictions error marker file (to show the benefit of the filter)
    # for i, c in enumerate(C_rejected):
    #     # assert _is_inside_margin(substack, c):
    #     r, g, b = 255, 128, 0
    #     name = 'REJ_%03d (%s)' % (i + 1, c.name)
    #     cx, cy, cz = int(round(c.x)), int(round(c.y)), int(round(c.z))
    #     comment = ':'.join(map(str, [cx, cy, cz, c]))
    #     if errors_marker_file is not None:
    #         print(
    #             ','.join(
    #                 map(str, [
    #                     1 + cx, 1 + cy, 1 + cz, 0, 1, name, comment, r, g,
    #                     b
    #                 ])),
    #             file=ostream)

    if errors_marker_file is not None:
        ostream.close()

    if len(C_pred):
        if hasattr(C_pred[0], 'distance') and rp_file is not None:
            with open(rp_file, 'w') as ostream:
                for i, c in enumerate(C_pred):
                    # assert _is_inside_margin(substack, c):
                    if c in true_positives_pred:
                        print(-c.distance, '1', file=ostream)
                    else:
                        print(-c.distance, '0', file=ostream)
                # Add also the false negatives with infinite distance so they will always be rejected
                for i, c in enumerate(C_true):
                    if c not in true_positives_true:
                        # assert _is_inside_margin(substack, c):
                        print(-1000, '1', file=ostream)

    if len(TP_inside) > 0:
        precision = float(
            len(TP_inside)) / float(len(TP_inside) + len(FP_inside) + 1e-6)
        recall = float(len(TP_inside)) / float(len(TP_inside) + len(FN_inside) + 1e-6)
    else:
        precision = int(len(FP_inside) == 0)
        recall = int(len(FN_inside) == 0)

    if len(TP_inside) == 0 and len(FP_inside) > 0 and len(FN_inside) > 0:
        F1 = 0.00
    else:
        F1 = 2 * precision * recall / (precision + recall)

    print(
        '|pred|=%d |true|=%d  P: %.2f / R: %.2f / F1: %.2f ==== TP: %d / FP: %d / FN: %d'
        % (len(C_pred), len(C_true), precision * 100,
           recall * 100, F1 * 100, len(TP_inside), len(FP_inside),
           len(FN_inside)))
    precision = precision * 100
    recall = recall * 100
    F1 = F1 * 100

    return precision, recall, F1, TP_inside, FP_inside, FN_inside