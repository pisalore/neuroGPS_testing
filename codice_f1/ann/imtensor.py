import tables
import os
import numpy as np
from progressbar import *
import glob
from skimage.external import tifffile

def pad_if_out_of_range(from_shape, origin, ss_shape):
    """Take a subtensor of shape `ss_shape` from a tensor of shape
`from_shape` starting from `origin`. All are n-dim tuples.  Returns an
n-dim tuple of pairs that may be used with numpy.pad

    """

    def start(a, b):
        if b >= a:
            return 0
        else:
            return a - b

    def end(c, d):
        if d <= c:
            return 0
        else:
            return d - c

    if len(from_shape) != len(origin) or len(from_shape) != len(ss_shape):
        raise Exception('The three tuples should have the same length')
    widths = []
    for dim in range(len(from_shape)):
        widths.append((start(0, origin[dim]),
                       end(from_shape[dim], origin[dim] + ss_shape[dim])))
    return tuple(widths)


def load_nearby(tensorimage, substack, extramargin):
    """Load a substack from a large tensor image stored in an HDF5
file. The extramargin is useful when convolut-like operations are
performed on the substack."""
    with tables.File(tensorimage, 'r') as hf5:
        X0, Y0, Z0 = substack.X0, substack.Y0, substack.Z0
        H, W, D = substack.height, substack.width, substack.depth
        from_shape = hf5.root.full_image.shape
        origin = (Z0 - extramargin, Y0 - extramargin, X0 - extramargin)
        substack_shape = (D + 2 * extramargin, H + 2 * extramargin, W + 2 * extramargin)
        # np_tensor_3d = hf5.root.full_image[1200:1500,1200:1500,1200:1500]
        np_tensor_3d = hf5.root.full_image[
            max(0, origin[0]):min(origin[0] + substack_shape[0], from_shape[0]),
            max(0, origin[1]):min(origin[1] + substack_shape[1], from_shape[1]),
            max(0, origin[2]):min(origin[2] + substack_shape[2], from_shape[2])]
        pad = pad_if_out_of_range(from_shape, origin, substack_shape)
        print('pad', pad)
        np_tensor_3d = np.pad(np_tensor_3d, pad, mode='constant')
        print('new shape', np_tensor_3d.shape)
        minz = int(hf5.root.minz[0])
    return np_tensor_3d, minz


def save_tensor_as_tif(np_tensor_3d, path, minz, prefix='full_'):
    #TODO In the future when we will use float32 the range will be [0,256) instead of [0,255] and we will divide and multiply by 256.

    """Export a 3D numpy tensor as a sequence of tiff files (one for each
z coordinate). Each file is named as prefix followed by an integer id,
which ranges in minz:minz+np_tensor_3d.shape[0].  The tensor is
expected to be stored in the order Z,Y,X
    """
    import uuid
    assert np_tensor_3d.dtype == np.float32
    assert np_tensor_3d.min() >= 0 and np_tensor_3d.max() <= 255.
    if not os.path.exists(path):
        os.makedirs(path)
    np_tensor_3d = (np_tensor_3d * 255).astype(np.uint16)
    pbar = ProgressBar(widgets=['Saving %d tiff files: ' % np_tensor_3d.shape[0], Percentage(), ' ', ETA()])
    for z in pbar(range(np_tensor_3d.shape[0])):
        tempname = '/tmp/' + str(uuid.uuid4()) + '.tif'
        tifffile.imsave(tempname, np_tensor_3d[z, ::-1, :])

        destname = path + '/' + prefix + '%04d.tif' % (minz + z)
        os.system('tiffcp -clzw:2 ' + tempname + ' ' + destname)
        os.remove(tempname)

    print('Saved substack in', path)

# def save_tensor_as_tif_16bit(np_tensor_3d, path, minz, prefix='full_'):
#     """Export a 3D numpy tensor as a sequence of tiff files (one for each
# z coordinate). Each file is named as prefix followed by an integer id,
# which ranges in minz:minz+np_tensor_3d.shape[0].  The tensor is
# expected to be stored in the order Z,Y,X"""
#     import uuid
#     assert np_tensor_3d.dtype == np.float32
#     if not os.path.exists(path):
#         os.makedirs(path)
#     pbar = ProgressBar(widgets=[
#         'Saving %d tiff files: ' % np_tensor_3d.shape[0],
#         Percentage(), ' ',
#         ETA()
#     ])
#     for z in pbar(range(np_tensor_3d.shape[0])):
#         tempname = '/tmp/' + str(uuid.uuid4()) + '.tif'
#         out_img = tifffile.imsave(tempname, np_tensor_3d[z, :, :].astype(np.uint16))
#         # out_img = Image.fromarray(np_tensor_3d[z, :, :])
#         # out_img.save(tempname)
#         assert os.path.exists(tempname)
#         destname = path + '/' + prefix + '%09d.tif' % (minz + z)
#         cmd = ['tiffcp', '-c', 'lzw:2', tempname, destname]
#         subprocess.run(['tiffcp', '-c', 'lzw:2', tempname, destname])
#         assert os.path.exists(tempname)
#         assert os.path.exists(destname)
#         os.remove(tempname)

    # print('Saved substack in', path)


def load_tensor_from_tif(path):
    x_list = []
    for tiff_file_name in sorted(glob.glob(os.path.join(path, '*.tif*'))):
        im = tifffile.imread(tiff_file_name)
        assert im.dtype == np.uint16
        x = im.reshape((1,) + im.shape)
        x = x[:,::-1,:].astype(np.float32) / 255.
        assert x.min() >= 0 and x.max() <= 255.
        # x = x.astype(np.uint8)
        x_list.append(x)
    return np.concatenate(x_list)

