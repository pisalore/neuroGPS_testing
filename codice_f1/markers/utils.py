import pandas as pd
from .center import Center, CenterList

def is_empty_csv(filename):
    # #x, y, z, radius, shape, name, comment
    # no marker found in the volume
    with open(filename) as f:
        lines = list(f)
        try:
            line1, line2, *rest = lines
            if not rest and line2.startswith('no marker found in the volume'):
                return True
        except ValueError:
            return True
    return False


def m_load_markers(filename, from_vaa3d=False, count_from_zero_flag=False):
    print('DEBUG reading {}...'.format(filename))
    data = pd.read_csv(filename, skipinitialspace=True, na_filter=False)
    if '#x' in data.keys():  # fix some Vaa3d garbage
        data.rename(columns={'#x': 'x'}, inplace=True)
    if '##x' in data.keys():  # fix some Vaa3d garbage
        data.rename(columns={'##x': 'x'}, inplace=True)
    
    C = []
    if not is_empty_csv(filename):
        for i in data.index:
            row = data.ix[i]
            if not row['x']: continue # FIXME this should not be needed
            c = Center(0, 0, 0)
            for k in row.keys():
                setattr(c, k, row[k])
            if from_vaa3d:
                if c.name == '':
                    c.name = 'landmark %d' % (i + 1)
            else:  # from predictor..
                try:
                    c.volume = float(c.comment.split('v=')[1].split()[0])
                    c.mass = float(c.comment.split('m=')[1].split()[0])
                    c.hue = float(c.comment.split('hue=')[1].split()[0])
                    citems = c.comment.split('\t')
                    if len(citems) > 5:
                        c.EVR = [float(x) for x in citems[5].split(':')]
                        if len(c.EVR) > 2:
                            c.last_variance = c.EVR[2]
                    if len(citems) > 6:
                        try:
                            c.radius = float(citems[6])
                        except ValueError:
                            pass
                except IndexError:
                    print('Warning: comment string unformatted (%s), is this really a predicted marker file?' % c.comment)
            c.ensure_numeric()
            C.append(c)
    if count_from_zero_flag:
        C = [c._sub_ones() for c in C]
    return CenterList(C)


def a_load_markers(filename, count_from_zero_flag=False):
    assert not count_from_zero_flag, 'unspecified behavior when count_from_zero_flag = True'
    data = pd.read_csv(filename, skipinitialspace=True, na_filter=False)
    C = []
    for i in data.index:
        row = data.ix[i]
        c = Center(0, 0, 0)
        for k in row.keys():
            setattr(c, k, row[k])
        C.append(c)
    return CenterList(C)
