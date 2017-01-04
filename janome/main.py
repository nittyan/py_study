# -*- coding: utf-8 -*-
from collections import defaultdict
from typing import Dict
from typing import List

from janome.tokenizer import Tokenizer as TK
from janome.tokenizer import Token


class Tokenizer:

    def __init__(self, path: str=''):
        if path:
            self._tk = TK(path, udic_type='simpledic', udic_enc='utf8')
        else:
            self._tk = TK()

    def tokenize(self, s: str, targets: List[str]) -> Dict[str, Token]:
        """

        :param s: 文字列
        :param targets: 動詞、名詞、助詞、助動詞、記号、副詞
        :return:
        """
        result = defaultdict(list)

        for token in self._tk.tokenize(s):
            for target in targets:
                if token.part_of_speech.startswith(target):
                    result[target].append(token)

        return result


def main():
    tokenizer = Tokenizer('mydict.csv')
    for k, v in tokenizer.tokenize("明日、実家に帰ろうと思っているのですが、巣年どうしようか悩んでいます。", ['動詞', '名詞']).items():
        print(k)
        for token in v:
            print(token)



if __name__ == '__main__':
    main()