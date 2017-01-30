# -*- coding: utf-8 -*-
from typing import Dict


class Webpage:

    def __init__(self, dict: Dict={}):
        self._page = dict

    @property
    def webpage(self):
        return self._page

    @property
    def id(self) -> str:
        return self._page.get('_id')

    @property
    def url(self) -> str:
        return self._page.get('url')

    @property
    def word_count(self) -> int:
        return self._page.get('word_count')

    @property
    def words(self) -> Dict[str, int]:
        return self._page.get('words')

    @property
    def category(self) -> str:
        return self._page.get('category', '')

    @category.setter
    def category(self, category: str):
        self._page['category'] = category


def main():
    webpage = Webpage({})
    print(webpage.url)


if __name__ == '__main__':
    main()
