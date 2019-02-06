import hashlib
import os

def model_hash_and_meta(model_dir, mb_idx):
    model_meta = '("model dir",  "{}", "mb", "{}")'.format(model_dir, mb_idx)
    model_hash = hashlib.sha256(model_meta.encode('ascii')).hexdigest()
    return model_hash, model_meta


def monitor_arg_shape(src_idx=None, dst_idx=None):
    def _wrapper(F):
        def _wrapper2(*args, **kwargs):
            res = F(*args, **kwargs)
            if src_idx is None:
                shape_src = args[0].shape
            elif isinstance(src_idx, int):
                shape_src = args[src_idx].shape
            elif isinstance(src_idx, str):
                shape_src = kwargs[src_idx].shape
            else:
                raise ValueError()

            shape_dst = (res if dst_idx is None else res[dst_idx]).shape
            print('function {} shape {} -> {}'.format(F.__name__, shape_src, shape_dst))
            return res

        return _wrapper2

    return _wrapper

class GTPathManager(object):
    def __init__(self, working_dir):
        self.working_dir = working_dir

    def stitch_path(self, stitch_file_name):
        path = os.path.join(self.working_dir, hashlib.sha256(stitch_file_name.encode('ascii')).hexdigest())
        if not os.path.exists(path):
            os.makedirs(path)
            with open(os.path.join(path, 'meta.txt'), 'w') as meta_file:
                print('{}'.format(stitch_file_name), file=meta_file)
        return path

    def block_dir_path(self, stitch_file, x, y, z):
        block_dir_path = os.path.join(self.stitch_path(stitch_file), 'x{:06d}_y{:06d}_z{:06d}'.format(x, y, z))
        if not os.path.exists(block_dir_path):
            os.makedirs(block_dir_path)
        return block_dir_path

    def substack_path(self, stitch_file, x, y, z):
        sspath = os.path.join(self.block_dir_path(stitch_file, x, y, z), 'ss')
        if not os.path.exists(sspath):
            os.makedirs(sspath)
        return sspath

# class GTPathManager(object):
#     def __init__(self, working_dir):
#         self.working_dir = working_dir
#
#     def stitch_path(self, stitch_file_name):
#         path = os.path.join(self.working_dir, hashlib.sha256(stitch_file_name.encode('ascii')).hexdigest())
#         if not os.path.exists(path):
#             os.makedirs(path)
#             with open(os.path.join(path, 'meta.txt'), 'w') as meta_file:
#                 print('{}'.format(stitch_file_name), file=meta_file)
#         return path
#
#     def block_dir_path(self, stitch_file, x, y, z):
#         block_dir_path = os.path.join(self.stitch_path(stitch_file), 'x{:06d}_y{:06d}_z{:06d}'.format(x, y, z))
#         if not os.path.exists(block_dir_path):
#             os.makedirs(block_dir_path)
#         return block_dir_path
#
#     def substack_path(self, stitch_file, x, y, z):
#         sspath = os.path.join(self.block_dir_path(stitch_file, x, y, z), 'ss')
#         if not os.path.exists(sspath):
#             os.makedirs(sspath)
#         return sspath
