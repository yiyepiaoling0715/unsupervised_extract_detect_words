"""
1.提取 2-10长度范围内所有的字符串
2.统计字符串词频
3.给字符串分词，统计相邻两个分词结果的聚合度，取最小值，代表这个字符串的聚合度
4.看字符串外部的自由度，统计左右信息熵。
5.综合上述信息，卡阈值，保留符号条件的新词。

优化：
    是否需要卡出现频次阈值


"""

import itertools
import os

import jieba

from configs import Thresholds as ths
from configs import output_dirpath
from get_corpus import _read_corpus_mgr_groupby_file
from patterns import Patterns
from trie_multi import Trie
from util_funcs import _generate_ngram,_jieba_lcut,_write_file

_pattern_class = Patterns()

result_filepath = os.path.join(output_dirpath, 'result.txt')



def train_with_idf_multiprocessing():
    trie = Trie()
    file2lines_dict = _read_corpus_mgr_groupby_file()
    length_files = len(file2lines_dict)
    print('length_files==>', length_files)
    file2longline_dict = {k: ' '.join(v) for k, v in file2lines_dict.items()}
    # phrase2idf_dict=dict()
    trie.set_file2longline(file2longline_dict, length_files)
    lines = list(itertools.chain.from_iterable(list(file2lines_dict.values())))
    words_raw = list(itertools.chain.from_iterable([_jieba_lcut(line) for line in lines]))
    words_filtered = [word_iter for word_iter in words_raw if _pattern_class.pattern_useful.fullmatch(word_iter)]
    trie.counter_allwords_once(words_filtered)
    print('读取的所有文件的行数  len(lines)==>', len(lines))
    for index, line in enumerate(lines):
        words_iter = _jieba_lcut(line)
        words_filtered = [word_iter for word_iter in words_iter if _pattern_class.pattern_useful.fullmatch(word_iter)]
        words_groups = list()
        for n_iter in range(ths.ngram_area.value[0], ths.ngram_area.value[1]):
            words_group_iter = _generate_ngram(words_filtered, n_iter)
            words_groups.extend(words_group_iter)
        for word_group_iter in words_groups:
            trie.add(word_group_iter)
        if index % 1000 == 0:
            print(index)
    # trie.set_phrase2idf(phrase2idf_dict)
    result = trie.find_topn(lines, topn=1000)
    _write_file(result, result_filepath)
    for iterow in result:
        str_iter = ''.join(iterow[0].split('_'))
        # print(str_iter)
        # print(str_iter,count)
        print(iterow)


if __name__ == '__main__':
    train_with_idf_multiprocessing()
