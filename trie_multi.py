"""
一个句子的分词，所有的3元词组都有组合，每个组合左边，右边的作为统计熵
2-11个字作为的切词，就是在 把这个片段看作词的基础上，看能不能继续组合成词。
"""

"""
上一个版本的理论基础，是在已有jieba分词的基础上，进行词语之间的组合，作为新词挖掘；
n个词组合为新词的情况；  任意两个词，找出所有的左信息，右信息进行统计；

此次优化：1.如果 任意一个短语切片假定为词语， 看左右信息熵，左右很活跃，此词成立，左右不活跃，进行组合【直接不成立】
                【的电影  电影院】，无法计算 内部聚合度
        
优化方向：  1.过滤掉pmi低于一定阈值的，2.过滤掉 entropy 低于一定阈值的，3. 调节idf权重
"""
import collections
import math
import multiprocessing as mp

from multiprocess_deal import split_dict_data
from util_funcs import _calc_idf, reverse_first, calc_pmi, calc_entropy, _filter_str



class Node(object):
    def __init__(self, char):
        self.char = char
        self.count = 0
        self.child_value2nodes = {}
        self.is_end = False
        self.is_back = False


class Trie(object):
    def __init__(self):
        self._root = Node('root')
        self._word2counter = collections.defaultdict(int)
        self._words_total = 0

    def counter_allwords_once(self, words_in):
        for word_iter in words_in:
            self._word2counter[word_iter] += 1
        self._words_total = len(words_in)

    def counter_allwords_add(self, words_in):
        for word_iter in words_in:
            self._word2counter[word_iter] += 1
        self._words_total += len(words_in)

    def set_phrase2idf(self, dict_in):
        self.phrase2idf_dict = dict_in

    def set_file2longline(self, file2longline_dict, length_files):
        self.file2longline_dict = file2longline_dict
        self.length_files = length_files

    def add(self, words_parts_in):
        """统计所有的词频，左信息，右信息数量   words_parts 比实际要合并计算的要多一个词"""
        # print('words_parts_in==>',words_parts_in)
        words_parts_left = words_parts_in

        def add_forward(words_parts_forward, forward=True):
            node_cur = self._root
            for index, word_iter in enumerate(words_parts_forward):
                if word_iter in node_cur.child_value2nodes:
                    node_cur = node_cur.child_value2nodes[word_iter]
                else:
                    node_new = Node(word_iter)
                    node_cur.child_value2nodes[word_iter] = node_new
                    node_cur = node_new

                if index == len(words_parts_forward) - 1:
                    node_cur.is_end = True
                    node_cur.count += 1
                if index == len(words_parts_forward) - 1 and not forward:
                    node_cur.is_back = True

        add_forward(words_parts_left)
        words_parts_right = reverse_first(words_parts_left)
        add_forward(words_parts_right, forward=False)

    def search_one(self, word_in):
        """每一个词出现的总频率"""
        ratio = self._word2counter[word_in] / self._words_total
        return ratio

    def search_entropy(self):
        strconcat2entropy_dict = dict()

        def recursive(node_cur, str_concat_in):
            # if str_concat_in.count('_')>2:
            #     print(str_concat_in)
            forward_childs_count = []
            backward_childs_count = []
            for value_iter, child_node_iter in node_cur.child_value2nodes.items():
                if child_node_iter.is_end == True:
                    if child_node_iter.is_back:
                        backward_childs_count.append(child_node_iter.count)
                    else:
                        forward_childs_count.append(child_node_iter.count)
                else:
                    pass
            # sums=sum(childs_count)
            if forward_childs_count:
                forward_entropy_cur = calc_entropy(forward_childs_count)
            else:
                forward_entropy_cur = 10000
            if backward_childs_count:
                backward_entropy_cur = calc_entropy(backward_childs_count)
            else:
                backward_entropy_cur = 10000
            if forward_entropy_cur != 10000 or backward_entropy_cur != 10000:
                strconcat2entropy_dict[str_concat_in] = (forward_entropy_cur, backward_entropy_cur)
            else:
                pass
            for value_iter, node_iter in node_cur.child_value2nodes.items():
                # if not node_iter.is_end:
                if node_iter.child_value2nodes:
                    str_concat_iter = str_concat_in + '_' + value_iter
                    recursive(node_iter, str_concat_iter)

        recursive(self._root, '')
        return strconcat2entropy_dict

    def search_cooccurance(self):
        strconcat2count_dict = collections.defaultdict(int)

        def recursive(node_in, str_concat_in):
            counts = 0
            for value_iter, node_iter in node_in.child_value2nodes.items():
                # if node_iter.is_end and not node_iter.is_back:
                if node_iter.is_end:
                    counts += node_iter.count
            strconcat2count_dict[str_concat_in] = counts

            for value_iter, node_iter in node_in.child_value2nodes.items():
                # if not node_iter.is_end:
                if node_iter.child_value2nodes:
                    str_concat_iter = str_concat_in + '_' + value_iter
                    recursive(node_iter, str_concat_iter)

        recursive(self._root, '')
        return strconcat2count_dict

    def calc_pmis(self):
        """ 连续的几个词的组合，pmi如何计算， 连续的概率积，还是取两个连续值的概率积的最小值 """
        str_concat2count_dict = self.search_cooccurance()
        sum_all = sum(list(str_concat2count_dict.values()))
        strconcat2pmi_dict = dict()
        for str_concat_iter, count_iter in str_concat2count_dict.items():
            if not str_concat_iter:
                continue
            strs_iter = str_concat_iter.split('_')
            strs_iter = [elem for elem in strs_iter if elem]
            # print('strs_iter==>',strs_iter)
            ratios = [self.search_one(str_iter) for str_iter in strs_iter]
            dot_base_elem = calc_pmi(ratios)
            strconcat2pmi_dict[str_concat_iter] = (
                math.log(max(1, count_iter), 2) - math.log(sum_all, 2) - 2 * math.log(dot_base_elem, 2),
                count_iter / sum_all)
        return strconcat2pmi_dict

    def process_iter(self, strconcat2entropy_dict_in, strconcat2pmi_dict_in, return_dict_in):
        strconcat2score_dict = dict()
        strconcat2entropy_dict = strconcat2entropy_dict_in
        strconcat2pmi_dict = strconcat2pmi_dict_in
        print('strconcat2entropy_dict_filtered length', len(strconcat2entropy_dict))
        for strconcat_iter, entropy_iter in strconcat2entropy_dict.items():
            # print('strconcat_iter==>',strconcat_iter)
            # print('pmi_iter=>',strconcat_iter,pmi_iter)
            pmi_iter = strconcat2pmi_dict[strconcat_iter]
            # print('strconcat2entropy_dict[strconcat_iter]==>',strconcat2entropy_dict[strconcat_iter])
            score_iter = (pmi_iter[0] + min(strconcat2entropy_dict[strconcat_iter][0],
                                            strconcat2entropy_dict[strconcat_iter][1])) * pmi_iter[1]
            phrase_iter = ''.join(strconcat_iter.split('_'))
            idf_phrase = _calc_idf(phrase_iter, self.file2longline_dict, self.length_files)
            # if idf_phrase>0:
            if strconcat_iter in ['_不_在_保障_范围', '_重大_疾病']:
                print(idf_phrase)
            strconcat2score_dict[strconcat_iter] = score_iter * idf_phrase
        return_dict_in.update(strconcat2score_dict)
        return strconcat2score_dict

    def find_topn(self, lines, topn):
        # node_cur = self._root
        # strconcat2score_dict=dict()
        strconcat2entropy_dict_raw = self.search_entropy()
        strconcat2pmi_dict = self.calc_pmis()

        strconcat2entropy_dict_filtered = {k: v for k, v in strconcat2entropy_dict_raw.items() if
                                           float(v[0]) != 0 and float(v[1] != 0)}
        strconcat2entropy_dict_slices = split_dict_data(strconcat2entropy_dict_filtered)
        print('过滤掉0以后的 length--strconcat2entropy_dict_filtered', len(strconcat2entropy_dict_filtered))
        print('切分的数据份数', len(strconcat2entropy_dict_slices))
        manager = mp.Manager()
        strconcat2score_dict = manager.dict()

        processes = []
        for strconcat2entropy_dict_slice_iter in strconcat2entropy_dict_slices:
            process_iter = mp.Process(target=self.process_iter, args=(
                strconcat2entropy_dict_slice_iter, strconcat2pmi_dict, strconcat2score_dict))
            processes.append(process_iter)
        for process_iter in processes:
            process_iter.start()
        for process_iter in processes:
            process_iter.join()

        strconcat2score_sorted = sorted(strconcat2score_dict.items(), key=lambda x: x[1], reverse=True)
        strconcat2score_sorted = [iterow for iterow in strconcat2score_sorted if
                                  _filter_str(''.join(iterow[0].split('_')), lines)]
        return strconcat2score_sorted[:topn]


if __name__ == '__main__':
    trie = Trie()
    result = trie.find_topn()
    print(result)
