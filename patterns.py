import re


class Patterns(object):
    _only_pure_num = [re.compile('\d+')]
    _space_num = [re.compile('\d+[ \t]+')]
    # _pure_num = [re.compile('(?P<number>\d+)[.、．]{1}(?!\d+)')]
    _pure_num = [re.compile('\d+[.、．]{1}')]
    # _pure_num = [re.compile('\d+[.、．]{1}')]
    # _bracket_num=[re.compile('(\d+)[)）]+|[(（]+(\d+)')]
    _bracket_num = [re.compile('[(（]+\d+'), re.compile('\d+[)）]+')]
    _decimal_num = [re.compile('\d+[.、．]+\d+')]
    _continu_decimal_num = [re.compile('\d+[.、．]+\d+[.、．]+\d+')]
    _longer_continus_decimal_num = [re.compile('\d+[.、．]+\d+[.、．]+\d+[.、．]+\d+')]
    # chines_num=[re.compile('第(?P<number>[一二三四五六七八九])+部分')]
    _sequence_num_zhang = [re.compile('第\d+章')]
    _sequence_num_tiao = [re.compile('第\d+条')]
    _sequence_num_bufen = [re.compile('第\d+部分')]
    _char_num = [re.compile('[A-Z]+\d+[.、．]{1}(?!\d+)')]

    _inner_space_line = [re.compile('(?<=[\u4e00-\u9fa5])([ \t]{1,})(?=[\u4e00-\u9fa5])', flags=re.MULTILINE), ]
    _page_num = [re.compile('第[\t ]*\d+[\t ]*页[\t ]*共[\t ]*\d+[\t ]*页'), ]
    _shiyi_num = [re.compile('释义[\t \n]{,2}\d+[.、]', flags=re.MULTILINE)]

    _full_space = [re.compile('[\n \t]+')]
    _split_punc = [re.compile('[:：]+'), ]

    _ascii_num1 = [re.compile('[⒈⒉⒊⒋⒌⒍⒎⒏⒐⒑⒒⒓⒔⒕⒖⒗⒘⒙⒚⒛]+')]
    _ascii_num2 = [re.compile('[⑴⑵⑶⑷⑸⑹⑺⑻⑼⑽⑾⑿⒀⒁⒂⒃⒄⒅⒆⒇]+')]
    _ascii_num3 = [re.compile('[①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳]+')]

    _pure_chinese = re.compile('[\u4e00-\u9fa5]+')
    # _punctuation_not_question=[re.compile('[;；。]+'),re.compile('[\u4e00-\u9fa5a-zA-Z0-9]+\n[\u4e00-\u9fa5a-zA-Z0-9]+')]
    _punctuation_not_question = [re.compile('[;；。]+'),
                                 re.compile('[\u4e00-\u9fa5a-zA-Z0-9]+\n[\u4e00-\u9fa5a-zA-Z0-9]+')]
    _punctuation_question = [re.compile('【.*】')]
    # _further_punctuation_question=[re.compile('【.*】'),[re.compile('[:：]$')]]
    _colon_question = [re.compile('[:：]$')]

    _pattern_category_text = [re.compile('(目[ \t]{0,10}录|索[ \t]{0,10}引|提[ \t]{0,10}示|指[ \t]{0,10}引)+'), ]
    # _pattern_category_nodes=[re.compile('\.\.\.\.\.')]
    _pattern_category_nodes = [re.compile('[…．.·-]{5,}')]
    _pattern_company_name = [re.compile('(有[ \t]{0,10}限[ \t]{0,10}公[ \t]{0,10}司|条[ \t]{0,10}款|合[ \t]{0,10}同)+')]

    _pattern_footers = [re.compile('第[ \t]{0,10}\d+[ \t]{0,10}页[ \t,，]{0,10}共[ \t]{0,10}\d+[ \t]{0,10}页'),
                        re.compile('-+[ \t]{0,10}\d+[ \t]{0,10}-+'),
                        re.compile('第[ \t]{0,10}\d+[ \t]{0,10}页'), re.compile('\d+[ \t]{0,10}/[ \t]{0,10}\d+')]
    _pattern_useful = re.compile(
        '[ \u4E00-\u9FA5a-zA-Z0-9,，.·．。！!（）();；：:/、%⒈⒉⒊⒋⒌⒍⒎⒏⒐⒑⒒⒓⒔⒕⒖⒗⒘⒙⒚⒛⑴⑵⑶⑷⑸⑹⑺⑻⑼⑽⑾⑿⒀⒁⒂⒃⒄⒅⒆⒇①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳]+')
    # _pattern_useful_no_space = re.compile('[\u4E00-\u9FA5a-zA-Z0-9,，.·．。！!（）();；：:/、%⒈⒉⒊⒋⒌⒍⒎⒏⒐⒑⒒⒓⒔⒕⒖⒗⒘⒙⒚⒛⑴⑵⑶⑷⑸⑹⑺⑻⑼⑽⑾⑿⒀⒁⒂⒃⒄⒅⒆⒇①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳]+')
    _pattern_headers = [re.compile('附件\d+.*\d+')]

    def __init__(self):
        pass

    @property
    def colon_pattern(self):
        return self._colon_question

    @property
    def kv_pattern_num(self):
        kv = {1: self._space_num, 2: self._pure_num, 3: self._bracket_num, 4: self._decimal_num,
              5: self._continu_decimal_num, 6: self._longer_continus_decimal_num, 7: self._sequence_num_zhang,
              8: self._sequence_num_tiao, 9: self._sequence_num_bufen, 10: self._char_num, 11: self._ascii_num1,
              12: self._ascii_num2, 13: self._ascii_num3, 14: self._shiyi_num}
        return kv

    @property
    def split_punctuation_null(self):
        patterns = [*self._full_space]
        return patterns

    @property
    def split_punctuation_colon(self):
        return self._split_punc

    @property
    def pattern_useful(self):
        return self._pattern_useful

    @property
    def pattern_footers(self):
        return self._pattern_footers

    @property
    def pattern_headers(self):
        return self._pattern_headers

    @property
    def pattern_company_name(self):
        return self._pattern_company_name

    @property
    def patterns_category_nodes(self):
        return self._pattern_category_nodes

    @property
    def patterns_category_text(self):
        return self._pattern_category_text

    @property
    def patterns_chinese(self):
        return self._pure_chinese

    def bool_chinese_in(self, text_in):
        if self._pure_chinese.search(text_in):
            return True
        return False

    @property
    def only_pure_num(self):
        return self._only_pure_num

    # @property
    # def patterns_num_(self):
    #     return [*self._only_pure_num, *self._pure_num, *self._decimal_num, *self._sequence_num, *self._shiyi_num,
    #             *self._char_num, *self._continu_decimal_num]
    @property
    def patterns_num(self):
        return [*self._space_num, *self._pure_num, *self._decimal_num, *self._sequence_num_zhang,
                *self._sequence_num_tiao, *self._sequence_num_bufen, *self._shiyi_num,
                *self._char_num, *self._continu_decimal_num, *self._longer_continus_decimal_num, *self._ascii_num1,
                *self._ascii_num2, *self._ascii_num3]

    @property
    def pattern_punctuation_question(self):
        return self._punctuation_question

    @property
    def pattern_full_space(self):
        return self._full_space

    @property
    def pattern_punctuaion_not_question(self):
        return self._punctuation_not_question

    def bool_number(self, line_in):
        for pattern_iter in self.patterns_num:
            # for pattern_iter in patterns:
            if pattern_iter.match(line_in):
                return True
        return False

    @property
    def pattern_inner_space_line(self):
        return self._inner_space_line

    def bool_inner_line_space(self, text_in):
        for pattern_iter in self._inner_space_line:
            if pattern_iter.search(text_in):
                return True
        return False

    def bool_delete(self, text_in):
        """如果是页数，则予以删除"""
        text_cur = text_in
        for pattern_iter in self._page_num:
            if pattern_iter.fullmatch(text_cur):
                return True
        return False

    def bool_question(self, text_in):
        """排除标点干扰，  确认数字，  标题符号【】"""
        # for pattern_iter in self.pattern_punctuaion_not_question:
        #     if pattern_iter.search(text_in):
        #         return False
        for pattern_iter in self.patterns_num:
            if pattern_iter.match(text_in):
                return True
        for pattern_iter in self.pattern_punctuation_question:
            if pattern_iter.search(text_in):
                return True
        return False

    def bool_fullmatch_space(self, text_in):
        for pattern_iter in self._full_space:
            if pattern_iter.fullmatch(text_in):
                return True
        return False

    def bool_fullmatch_split_punctuation_null(self, text_in):
        for pattern_iter in self.split_punctuation_null:
            if pattern_iter.fullmatch(text_in):
                return True
        return False

    def bool_fullmatch_split_punctuation_colon(self, text_in):
        for pattern_iter in self.split_punctuation_colon:
            if pattern_iter.fullmatch(text_in):
                return True
        return False

    def bool_question_existed_num(self, text_in):
        for pattern_iter in self.patterns_num:
            if pattern_iter.match(text_in):
                return True
        return False
