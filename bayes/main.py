# -*- coding: utf-8 -*-
from collections import defaultdict
from typing import Dict
from typing import List

from janome.tokenizer import Token
from janome.tokenizer import Tokenizer as TK

# tf-idf
# tf
# ある単語の出現回数を、文書中の全単語の単語数で割った値



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




def tf(sentence: str):
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(sentence, ['名詞', '動詞'])
    flatten = flat(tokens)
    print(len(flatten))
    for i in flatten:
        print(i)
    

def size(dic: Dict[str, Token]):
    return sum(list(map(lambda x: len(x), dic.values())))


def flat(dic: Dict[str, Token]):
    result = []
    for v in dic.values():
        result.extend(v)
    return result


def main():
    tf('明日、サッカーの試合なのですが、どう考えても相手のほうが強いので、気がめいりますが、サッカーが大好きなので楽しむつもりで試合にのぞもうと思います。')


if __name__ == '__main__':
    main()