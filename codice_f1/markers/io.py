from .utils import m_load_markers, a_load_markers
from .center import CenterList
import os

def save_markers(filename, C, floating_point=False, center_name=None):
    assert center_name is not None
    """save_markers(filename, C)

    Save markers to a Vaa3D readable file.

    Parameters
    ----------
    filename : str
        Name of the file where markers are saved
    C : list
        List of :class:`Center` objects
    floating_point: bool
        If true, save coordinates in floating point, else round to int
    """
    assert isinstance(C, CenterList), 'type(C): {}'.format(type(C))
    filename = os.path.abspath(filename)
    with open(filename, 'w') as ostream:
        print('##x,y,z,radius,shape,name,comment, color_r,color_g,color_b', file=ostream)
        if C:  # if CenterList is not empty            
            # C.neighbors_graph()
            with open(filename, 'w') as ostream:
                # for i,c in enumerate(C):
                for c in C:
                    r, g, b = 0, 200, 100
                    radius, shape = 0, 1
                    if floating_point:
                        cx, cy, cz = c.x, c.y, c.z
                    else:
                        cx, cy, cz = int(round(c.x)), int(round(c.y)), int(round(c.z))
                    c = c.swap_xy()
                    comment = str(c)
                    print(','.join(map(str, [1 + cx, 1 + cy, 1 + cz, radius, shape, center_name, comment, r, g, b])), file=ostream)
    assert os.path.exists(filename)


def load_markers(filename, from_vaa3d=False, check_coords=True, count_from_zero_flag=False, substack=None):
    suffix = filename.split('.')[-1]
    if suffix == 'marker':
        C = m_load_markers(filename, from_vaa3d, count_from_zero_flag)
    elif suffix == 'apo':
        C = a_load_markers(filename, count_from_zero_flag)
    else:
        raise ValueError("Don't understand suffix", suffix)
    if check_coords:
        if substack is None:
            raise ValueError('we can not check the coordinates without a substack')
        # for c in C:
        #     if c.x > substack.width or c.y > substack.height or c.z > substack.depth:
        #         raise Exception('Coordinates in marker file are out of range', (c.x, c.y, c.z), substack.substack_id)
        
    assert isinstance(C, CenterList)
    return C.int_center()


