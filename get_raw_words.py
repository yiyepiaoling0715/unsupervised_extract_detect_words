import collections
import re

import jieba

from util_funcs import _generate_ngram

"""
统计词频方式， trie存储
统计互信息，  获取字符串片段
获取字符串片段，跟jieba 已有分词进行对比，去掉已经存在的。
"""


def _read_dict_from_jieba():
    words = []
    with open('./files/dict.txt', 'r') as fr:
        for line in fr:
            parts = line.split()
            words.append(parts[0])
            # print(parts[0])
    return words


def cluster_strparts_by_length(words_list_in):
    length2words = collections.defaultdict(list)
    for word_iter in words_list_in:
        length2words[len(word_iter)].append(word_iter)
    print(length2words.keys())
    for k, v in length2words.items():
        print(k, len(v))


def _cut_str(line_in):
    words = jieba.lcut(line_in)
    return words


def _read_corpus():
    filepath = './files/a.txt'
    with open(filepath, 'r') as fr:
        for line in fr:
            line_strip = line.strip('\r\n ')
            yield line_strip


def _strs2longstr():
    longstr = ''
    for str_iter in _read_corpus():
        longstr += str_iter
        longstr += '\t'
    return longstr


pattern_punctuation = re.compile('[,，。.!！？?;；：:]+')


class GetRawWords(object):
    def __init__(self):
        self._word_threshold = [2, 11]
        # self._longstr=_strs2longstr()
        self._threshold_freq = 3

    def _get_all_partstr_from_line(self, line_in):
        words_from_jieba = _read_dict_from_jieba()

        partstrs_triples = []
        length = len(line_in)
        counter_in_jieba = 0
        for index in range(length):
            for thres_iter in range(self._word_threshold[0], self._word_threshold[1]):
                partstr_iter = line_in[index:][:thres_iter]
                if partstr_iter in words_from_jieba:
                    counter_in_jieba += 1
                    continue
                if self._word_threshold[0] <= len(partstr_iter) < self._word_threshold[1]:
                    strs_split = line_in.split(partstr_iter)
                    words_pre = _cut_str(strs_split[0])
                    words_post = _cut_str(strs_split[-1])
                    # print(words_pre,partstr_iter,words_post)
                    strs_kept = words_pre[-2:] + [partstr_iter] + words_post[:2]
                    words_triples = _generate_ngram(strs_kept)
                    # print(words_triples)
                    partstrs_triples.extend(words_triples)
        # partstrs_duplicate=list(set(partstrs))
        # print(partstrs)
        print('counter_in_jieba==>', counter_in_jieba)
        return partstrs_triples

    def get_part_strs(self):
        words_from_jieba = _read_dict_from_jieba()

        all_strparts = []
        for line_iter in _read_corpus():
            lines_iter = pattern_punctuation.split(line_iter)
            for line_iter in lines_iter:
                partstrs = self._get_all_partstr_from_line(line_iter)
                # print(len(partstrs))
                # print(partstrs)
                all_strparts.extend(partstrs)
        print(len(all_strparts))
        all_strparts_duplicate = list(set(all_strparts))
        print(len(all_strparts_duplicate))
        return all_strparts_duplicate

    def _sort_words_by_counter(self):
        word2counters = collections.defaultdict(int)
        for line_iter in _read_corpus():
            lines_iter = pattern_punctuation.split(line_iter)
            for line_iter in lines_iter:
                partstrs = self._get_all_partstr_from_line(line_iter)
                for word_iter in partstrs:
                    word2counters[word_iter] += 1
        word2counters_filtered = {word: counter for word, counter in word2counters.items() if
                                  counter > self._threshold_freq}
        # return word2counters_filtered
        word2counters_sorted = sorted(word2counters_filtered, key=lambda x: word2counters_filtered.get(x), reverse=True)
        return word2counters_sorted, word2counters_filtered

    def get_words_counter(self):
        word2counters_sorted, word2counters_filtered = self._sort_words_by_counter()
        words_jieba = _read_dict_from_jieba()
        word2counters_orderdict = collections.OrderedDict()
        for word in word2counters_sorted:
            if word not in words_jieba:
                word2counters_orderdict[word] = word2counters_filtered[word]
        return word2counters_orderdict

    def deal(self):
        pass


if __name__ == '__main__':
    grw = GetRawWords()
    allwords = grw.get_part_strs()

    # grw.cluster_strparts_by_length(allwords)
    # word2counter=grw.get_words_counter(grw._longstr,allwords)
    # for word,counter in word2counter.items():
    #     print(word,counter)
    # print(len(word2counter))

    word2counters = grw.get_words_counter()
    for word, counter in word2counters.items():
        print(word, counter)
    print(len(word2counters))
    # read_dict_from_jieba()
