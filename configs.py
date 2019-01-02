import os
from enum import Enum

abspath = os.path.abspath(__file__)
project_path = os.path.dirname(abspath)
files_dirpath = os.path.join(project_path, 'files')
output_dirpath = os.path.join(project_path, 'output')
if not os.path.exists(output_dirpath):
    os.mkdir(output_dirpath)


class Thresholds(Enum):
    phrase_occur_freq = 5
    ngram_area = [3, 8]
