import functools
import math

import numpy as np

from configs import Thresholds as ths


def _generate_ngram(words_in, ngram=3):
    words_out = []
    words_out.extend(zip(*[words_in[i:] for i in range(ngram)]))
    return words_out


def _calc_idf(str_in, file2longline_in, length_files):
    idf_val = 0
    for file_iter, longline_iter in file2longline_in.items():
        # bool_in=[1 for line_iter in lines_iter if str_in in line_iter]
        # for line_iter in lines_iter:
        #     if str_in in line_iter:
        #         idf_val+=1
        #         break
        if str_in in longline_iter:
            idf_val += 1
    return idf_val / length_files


def _calc_idf01(str_in, file2lines_in):
    idf_val = 0
    for file_iter, lines_iter in file2lines_in.items():
        # bool_in=[1 for line_iter in lines_iter if str_in in line_iter]
        for line_iter in lines_iter:
            if str_in in line_iter:
                idf_val += 1
                break
    return idf_val / len(file2lines_in)


def reverse_first(words_series_in):
    # print('words_series_in==>',words_series_in)
    words_series_left = ['' for _ in words_series_in]
    length = len(words_series_in)
    # words_1st=words_series_in[0]
    # words_last=words_series_in[-1]
    for index in range(length - 1):
        # print(index)
        words_series_left[index] = words_series_in[index + 1]
    words_series_left[length - 1] = words_series_in[0]
    return words_series_left


def calc_entropy(counts_list_in):
    entropies = []
    total_num = sum(counts_list_in)
    for num_iter in counts_list_in:
        entropy_iter = (num_iter / total_num) * math.log(num_iter / total_num, 2)
        entropies.append(entropy_iter)
    return -sum(entropies)


def calc_pmi01(ratios_in):
    ratios = ratios_in
    # print('ratios==>',ratios)
    if len(ratios) > 1:
        dots = [ratios[index] * ratios[index + 1] for index in range(len(ratios) - 1)]
    else:
        dots = ratios
    dots_sorted = sorted(dots, reverse=False)
    # print('dots==>',dots,str_concat_iter)
    # print(str_concat_iter)
    # ratios_sorted=sorted(ratios,reverse=False)
    # print('ratios_sorted==>',ratios_sorted)
    dot_min = dots_sorted[0]
    return dot_min


def calc_pmi02(ratios_in):
    ratios = ratios_in
    # print('ratios==>',ratios)
    length = len(ratios)
    dot = functools.reduce(lambda x, y: x * y, ratios)
    dot_elem = np.power(dot, 1 / length)
    return dot_elem


def calc_pmi(ratios_in):
    # return calc_pmi02(ratios_in)
    return calc_pmi01(ratios_in)


def _filter_by_freq(str_in, lines_in):
    count = sum([1 for line in lines_in if str_in in line])
    if count > ths.phrase_occur_freq.value:
        return True
    return False


if __name__ == '__main__':
    words = ['我', '和你', '心连心', '同住', '地球村']
    out = _generate_ngram(words)
    print(out)
