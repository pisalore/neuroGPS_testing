from scipy.spatial import cKDTree
import numpy as np
import numbers

class Center(object):
    # TODO make it a slot
    # TODO it is hard to turn this class into a slot
    """Similar to voxel but coordinates are real- instead of integer-valued

    Attributes
    ----------
    hue : int
        used to colorize the intermediate debugging images

    mass : float
        sum of voxel intensities for all voxels that are assigned to this
        center and are close enough to the center. Used in various places.

    volume : float
        number of voxels assigned to this center
    """

    def __init__(self, x, y, z):
        assert isinstance(x, numbers.Number), (type(x), x)
        assert isinstance(y, numbers.Number), (type(y), y)
        assert isinstance(z, numbers.Number), (type(z), z)
        
        self.x = x
        self.y = y
        self.z = z
        self.hue = 0
        self.reset()

    def ensure_numeric(self):
        self.x = float(self.x)
        self.y = float(self.y)
        self.z = float(self.z)

    def is_contained_in_shape(self, shape):
        return self.x >= 0 and self.x < shape[0] and \
            self.y >= 0 and self.y < shape[1] and \
            self.z >= 0 and self.z < shape[2]
    
    def is_in_padding(self, shape, padding):
        return self.x >= padding[0] and self.x < shape[0] - padding[0] and \
            self.y >= padding[1] and self.y < shape[1] - padding[1] and \
            self.z >= padding[2] and self.z < shape[2] - padding[2]
    
    def sqeuclidean(self, other):
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2

    def add(self, xyz):
        x, y, z = xyz
        return Center(self.x + x, self.y + y, self.z + z)

    
    def int_center(self):
        assert isinstance(self.x, numbers.Number), (type(self.x), self.x)
        assert isinstance(self.y, numbers.Number), (type(self.y), self.y)
        assert isinstance(self.z, numbers.Number), (type(self.z), self.z)
        xyz = [int(np.round(coord)) for coord in [self.x, self.y, self.z]]
        return Center(*xyz)
    
    def swap_xy(self):
        return Center(self.y, self.x, self.z)
    
    def _sub_ones(self):
        return Center(self.x - 1, self.y - 1, self.z - 1)

    def reset(self):
        self.sum_x = 0  # accumulator for barycenter
        self.sum_y = 0  # accumulator for barycenter
        self.sum_z = 0  # accumulator for barycenter
        self.mass = 0.01  # sum of intensities in the cluster
        self.volume = 0  # number of voxels in the cluster

    def short_desc(self):
        s = 'm=%.2f v=%.2f' % (self.mass, self.volume)
        return s

    def __str__(self):
        if self.volume != 0:
            s = 'm=%.1f\tv=%.2f\tr=%.2f\thue=%.2f' % (self.mass,
                                                      self.volume,
                                                      float(self.mass) / float(self.volume),
                                                      self.hue)
        else:
            s = 'm=%.1f\tv=%.2f\tr=%.2f\thue=%.2f' % (self.mass,
                                                      self.volume,
                                                      0.0,
                                                      self.hue)
        if hasattr(self, 'distances'):
            s = s + '\t' + ':'.join(['%.1f' % d for d in self.distances])
        if hasattr(self, 'EVR'):
            s = s + '\t' + ':'.join(['%.2f' % d for d in self.EVR])
        if hasattr(self, 'radius'):
            s = s + '\t' + str(self.radius)
        if hasattr(self, 'curvature'):
            s = s + '\t' + self.curvature
        if hasattr(self, 'distance'):
            s = s + '\t%.2f' % self.distance
        return s


class CenterList(object):
    def __init__(self, center_list=None):
        if center_list is None:
            self._center_list = []
        else:
            if not all(isinstance(c, Center) for c in center_list):
                raise TypeError('{}'.format(list(map(type, center_list))))
            self._center_list = center_list
    
    def unpad_markers(self, shape, padding):
        # REMOVE SPURIOUS CENTERS (in the padding area)
        center_list = CenterList([center for center in self._center_list if center.is_in_padding(shape, padding)])
        # SHIFT (the unpadded origin becomes (0,0,0))
        center_list = center_list.add((-padding[0], -padding[1], -padding[2]))
        return center_list

    def rescale(self, scale):
        return CenterList([Center(c.x*scale[0], c.y*scale[1], c.z*scale[2]) for c in self._center_list])

    def bbox_shape(self):
        corner_min, corner_max = self._bbox_endpoints()
        if corner_min is None or corner_max is None:
            return None
        return tuple(corner_max - corner_min)



    def _bbox_endpoints(self):
        corner_max = None
        corner_min = None
        for center in self._center_list:
            point = np.array([center.x, center.y, center.z])
            if corner_max is None:
                corner_max = point
            else:
                corner_max = np.maximum(corner_max, point)
            if corner_min is None:
                corner_min = point
            else:
                corner_min = np.minimum(corner_min, point)
        return corner_min, corner_max

    def bbox_str(self):
        self._bbox_endpoints()
        corner_min, corner_max = self._bbox_endpoints()
        if corner_min is None or corner_max is None:
            bbox_shape = None
        else:
            bbox_shape = tuple(corner_max - corner_min)
        
        corner_max = "({:.1f}, {:.1f}, {:.1f})".format(*tuple(corner_max)) if corner_max is not None else None
        corner_min = "({:.1f}, {:.1f}, {:.1f})".format(*tuple(corner_min)) if corner_min is not None else None
        shape = "({:.1f}, {:.1f}, {:.1f})".format(*tuple(bbox_shape)) if bbox_shape is not None else None 
        return "shape {} endpoints {} / {} ".format(shape, corner_min, corner_max)




    def is_contained_in_shape(self, shape):
        return all(center.is_contained_in_shape(shape) for center in self._center_list)


    def filter_in_padding(self, shape, padding):
        assert isinstance(shape, tuple)
        assert isinstance(padding, int)
        return CenterList([center for center in self._center_list if center.is_in_padding(shape, padding)])

    def __add__(self, other):
        return CenterList(self._center_list + other._center_list)
    
    def int_center(self):
        return CenterList(center_list=[c.int_center() for c in self])

    def add(self, xyz):
        return CenterList([c.add(xyz) for c in self._center_list])
    
    def append(self, c):
        if not isinstance(c, Center):
            raise TypeError('received type {} instead of Center'.format(type(c)))
        self._center_list.append(c)
    
    def extend(self, l):
        for c in l:
            self.append(c)
    
    def __iter__(self):
        return iter(self._center_list)
    
    def __len__(self):
        return len(self._center_list)

    def __bool__(self):
        return bool(self._center_list)

    def neighbors_graph(self):
        X = np.array([[c.x, c.y, c.z] for c in self._center_list])
        kdtree = cKDTree(X)
        for c in self._center_list:
            distances, _neighbors = kdtree.query([c.x, c.y, c.z], 6)
            c.distances = sorted(distances)[1:]
    