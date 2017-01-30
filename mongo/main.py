# -*- coding: utf-8 -*-
import hashlib

from collections import Counter
from typing import Dict
from typing import List

import pymongo
import requests
from bson.objectid import ObjectId
from bs4 import BeautifulSoup, NavigableString, Declaration, Comment

from janome.tokenizer import Tokenizer
from janome.tokenizer import Token

from mongo.model import Webpage



def md5(s: str):
    return hashlib.md5(s.encode()).hexdigest()


class Crawler:

    def __init__(self):
        self._analyzer = HtmlAnalyzer()

    def crawl(self, url: str) -> Webpage:
        html = self.download(url)
        tokens = self._analyzer.analyze(html)

        dic = {}
        dic['_id'] = md5(url)
        dic['url'] = url
        dic['category'] = ''
        counter = Counter(map(lambda  token: token.surface, tokens))
        dic['words'] = {w: cnt for w, cnt in counter.most_common()}
        dic['word_count'] = sum(counter.values())

        return Webpage(dic)

    def download(self, url: str) -> str:
        response = requests.get(url)
        return response.text


class HtmlAnalyzer:

    def __init__(self):
        self.tokenizer = Tokenizer()

    def analyze(self, html: str):
        sentence = self._strip_html(html)
        return self._tokenize(sentence)

    def _tokenize(self, sentence: str) -> List[Token]:
        tokens = []
        for token in self.tokenizer.tokenize(sentence):
            if token.part_of_speech.startswith('動詞') or token.part_of_speech.startswith('名詞'):
                if token.surface != '.':
                    tokens.append(token)

        return tokens

    def _strip_html(self, html: str) -> str:
        return '\n'.join(
            [sentence.strip() for sentence in self._get_navigable_strings(BeautifulSoup(html)) if sentence.strip() != ''])

    def _get_navigable_strings(self, soup: BeautifulSoup):
        if isinstance(soup, NavigableString):
            if type(soup) not in (Comment, Declaration) and soup.strip():
                yield soup
        elif soup.name not in ('script', 'style'):
            for c in soup.contents:
                for g in self._get_navigable_strings(c):
                    yield g


def connect_crawler():
    client = pymongo.MongoClient('localhost', 27017)
    return client.crawler


class WebpageDao:

    def __init__(self):
        self._collection = connect_crawler().webpages

    def add(self, webpage: Dict):

        if not self._collection.find_one({'_id': hashlib.md5(webpage['url'].encode()).hexdigest()}):
            self._collection.insert(webpage, check_keys=False)

    def find_by_word(self, word: str):
        return self._collection.find({'words.{}'.format(word): {'$exists': True}})

    def update(self, webpage: Webpage):
        self._collection.find_one_and_update({'_id': webpage.id}, {'$set': webpage.webpage}, upsert=True)

    def size(self) -> int:
        return self._collection.find().count()


def main():
    urls = [
        'http://www.gozmez.net/entry/2017/01/23/094533',
        # 'http://tomotty-tty.hatenablog.com/entry/2017/01/19/235753'
    ]
    crawler = Crawler()
    dao = WebpageDao()
    print(dao.size())
    for url in urls:
        webpage = crawler.crawl(url)
        webpage.category = 'test2'
        # print(webpage)
        dao.update(webpage)




if __name__ == '__main__':
    main()


    # collection.insert({'cnt': 2, 'words': ['a', 'b', 'あ']}, check_keys=False)
    # r = collection.find({'words': {'$in': ['あ']}})
    # print(r.count())
    # for i in r:
    #     print(i)
    #
    #


