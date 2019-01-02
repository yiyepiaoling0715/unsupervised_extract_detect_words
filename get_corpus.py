import collections
import glob
import itertools
import os

import pandas as pd

from configs import files_dirpath


def _read_corpus():
    filepath = './files/demo.txt'
    with open(filepath, 'r', encoding='utf-8') as fr:
        for line in fr:
            line_strip = line.strip('\r\n ')
            yield line_strip


def alllines_from_corpus():
    filepath = './files/demo.txt'

    with open(filepath, 'r', encoding='utf-8') as fr:
        lines = [line.strip('\r\n ') for line in fr]
        return lines


def _get_zjx_paths():
    zjx_dirpath = os.path.join(files_dirpath, 'zjx', '**', '*.xlsx')
    print(zjx_dirpath)
    filepaths = glob.glob(zjx_dirpath, recursive=True)
    # print(filepaths)
    return filepaths


def _get_csv_paths():
    ydlj_dirpath = os.path.join(files_dirpath, 'ydlj', '**', '*.tsv')
    filepaths = glob.glob(ydlj_dirpath)
    print('filepaths==>', filepaths)
    return filepaths


def _read_csvpaths(paths_in):
    filepath2lines = collections.defaultdict(list)
    # lines=[]
    print('len(paths_in)==>', len(paths_in))
    for path_iter in paths_in:
        # print(path_iter)
        rc = pd.read_csv(path_iter, sep='\t', engine='python', encoding='gbk')
        # print(rc.)
        # print(rc.keys())
        questions = rc['question']
        questions = [iterow for iterow in questions if isinstance(iterow, str)]
        # questions=rc[0]
        answers = rc['answer']
        answers = [iterow for iterow in answers if isinstance(iterow, str)]
        # answers=rc[1]
        # print(questions)
        # print(answers)
        # print(len(questions),len(answers))
        # print(questions)
        # print(answers)
        filepath2lines[path_iter] = questions + answers
        # lines.extend(questions+answers)
    # print(lines)
    return filepath2lines


def _read_excels(excel_paths):
    filepath2lines = collections.defaultdict(list)
    for excel_path_iter in excel_paths:
        re = pd.read_excel(excel_path_iter)
        questions = re['question']
        answers = re['answer']
        # print(questions)
        questions = [iterow for iterow in questions if isinstance(iterow, str)]
        answers = [iterow for iterow in answers if isinstance(iterow, str)]
        filepath2lines[excel_path_iter] = questions + answers
        # lines.extend(questions+answers)
    return filepath2lines


def _read_corpus_mgr():
    file2lines_dict = _read_corpus_mgr_groupby_file()
    return list(itertools.chain.from_iterable(list(file2lines_dict.values())))


def _read_corpus_mgr_groupby_file():
    excelpaths = _get_zjx_paths()
    file2lines_dict01 = _read_excels(excelpaths)
    csvpaths = _get_csv_paths()
    file2lines_dict02 = _read_csvpaths(csvpaths)
    # print('len(lines02)==>',len(lines02))
    # return lines+lines02
    # for line in lines:
    #     print(line)
    file2lines_dict = {**file2lines_dict01, **file2lines_dict02}
    return file2lines_dict


if __name__ == '__main__':
    # _read_corpus()
    # _get_zjx_corpus()
    #   _read_corpus_mgr()
    _get_csv_paths()
