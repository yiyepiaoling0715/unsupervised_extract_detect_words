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
import jieba
from bak.trie import Trie
from util_funcs import _generate_ngram
from get_corpus import  _read_corpus_mgr,_read_corpus_mgr_groupby_file
from patterns import Patterns

_pattern_class=Patterns()


def _load_stopwords():
    with open('./files/stopword.txt','r',encoding='utf-8') as fr:
        lines=[line.strip('\r\n ') for line in fr]
        return lines
stopwords=_load_stopwords()
def _jieba_lcut(line_in):
    words=jieba.lcut(line_in)
    words_filtered=[word for word in words if word not in stopwords]
    return words_filtered

def train_with_idf_multiprocessing():
    trie=Trie()
    file2lines_dict=_read_corpus_mgr_groupby_file()
    length_files=len(file2lines_dict)
    file2longline_dict={k:' '.join(v) for k,v in file2lines_dict.items()}
    # phrase2idf_dict=dict()
    trie.set_file2longline(file2longline_dict,length_files)
    lines=list(itertools.chain.from_iterable(list(file2lines_dict.values())))
    words_raw=list(itertools.chain.from_iterable([_jieba_lcut(line) for line in lines]))
    words_filtered=[word_iter for word_iter in words_raw if _pattern_class.pattern_useful.fullmatch(word_iter)]
    trie.counter_allwords_once(words_filtered)
    print('len(lines)==>',len(lines))
    for index,line in enumerate(lines):
        words_iter=_jieba_lcut(line)
        words_filtered = [word_iter for word_iter in words_iter if _pattern_class.pattern_useful.fullmatch(word_iter)]
        words_groups=list()
        for n_iter in range(3,8):
            words_group_iter=_generate_ngram(words_filtered,n_iter)

            words_groups.extend(words_group_iter)
        # words_groups=list(words_groups)
        for word_group_iter in words_groups:
        #     phrase_iter=''.join(word_group_iter)
            # idf_phrase=_calc_idf(phrase_iter,file2longline_dict,length_files)
            # phrase2idf_dict[phrase_iter]=idf_phrase
            trie.add(word_group_iter)
        if index%1000==0:
            print(index)
    # trie.set_phrase2idf(phrase2idf_dict)
    result=trie.find_topn()
    # print(result[:100])
    print('---')
    for iterow in result[:100]:
        str_iter=''.join(iterow[0].split('_'))
        # print(str_iter)
        count=sum([1 for line in lines if str_iter in line])
        # print(str_iter,count)
        if count>5:
            print(iterow)



def train_with_idf():
    trie=Trie()
    file2lines_dict=_read_corpus_mgr_groupby_file()
    length_files=len(file2lines_dict)
    file2longline_dict={k:' '.join(v) for k,v in file2lines_dict.items()}
    phrase2idf_dict=dict()

    lines=list(itertools.chain.from_iterable(list(file2lines_dict.values())))
    words_raw=list(itertools.chain.from_iterable([_jieba_lcut(line) for line in lines]))
    words_filtered=[word_iter for word_iter in words_raw if _pattern_class.pattern_useful.fullmatch(word_iter)]
    trie.counter_allwords_once(words_filtered)
    print('len(lines)==>',len(lines))
    for index,line in enumerate(lines):
        words_iter=_jieba_lcut(line)
        words_filtered = [word_iter for word_iter in words_iter if _pattern_class.pattern_useful.fullmatch(word_iter)]
        words_groups=list()
        for n_iter in range(3,8):
            words_group_iter=_generate_ngram(words_filtered,n_iter)

            words_groups.extend(words_group_iter)
        words_groups=list(words_groups)
        for word_group_iter in words_groups:
            phrase_iter=''.join(word_group_iter)
            idf_phrase=_calc_idf(phrase_iter,file2longline_dict,length_files)
            phrase2idf_dict[phrase_iter]=idf_phrase

            trie.add(word_group_iter)
        if index%100==0:
            print(index)
    trie.set_phrase2idf(phrase2idf_dict)
    result=trie.find_topn()
    # print(result[:100])
    print('---')
    for iterow in result[:100]:
        str_iter=''.join(iterow[0].split('_'))
        # print(str_iter)
        count=sum([1 for line in lines if str_iter in line])
        # print(str_iter,count)
        if count>5:
            print(iterow)

def train():
    trie=Trie()
    lines=_read_corpus_mgr()
    words_raw=list(itertools.chain.from_iterable([_jieba_lcut(line) for line in lines]))
    words_filtered=[word_iter for word_iter in words_raw if _pattern_class.pattern_useful.fullmatch(word_iter)]
    trie.counter_allwords_once(words_filtered)
    print('len(lines)==>',len(lines))
    for index,line in enumerate(lines):
        words_iter=_jieba_lcut(line)
        words_filtered = [word_iter for word_iter in words_iter if _pattern_class.pattern_useful.fullmatch(word_iter)]
        words_groups=list()
        for n_iter in range(3,8):
            words_group_iter=_generate_ngram(words_filtered,n_iter)

            words_groups.extend(words_group_iter)
        words_groups=list(words_groups)
        for word_group_iter in words_groups:
            trie.add(word_group_iter)
        if index%1000==0:
            print(index)
    result=trie.find_topn()
    # print(result[:100])
    print('---')
    for iterow in result[:100]:
        str_iter=''.join(iterow[0].split('_'))
        # print(str_iter)
        count=sum([1 for line in lines if str_iter in line])
        # print(str_iter,count)
        if count>5:
            print(iterow)
if __name__=='__main__':
    train_with_idf_multiprocessing()
