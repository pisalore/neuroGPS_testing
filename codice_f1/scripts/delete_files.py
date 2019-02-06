import os
import glob

print(os.path.abspath('treshold'))

for file_path in glob.glob(os.path.join('treshold/treshold_*/T*_R*', 'x*.swc.marker')):
    print (os.path.abspath(file_path))
    os.remove(os.path.abspath(file_path))
