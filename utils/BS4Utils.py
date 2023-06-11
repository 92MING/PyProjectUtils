# -*- coding: utf-8 -*-
'''BS4沒有、但常用的操作。'''

from bs4 import Tag, NavigableString
from typing import Tuple


def selfTexts(tag:Tag)-> Tuple[str]:
    '''取得tag自身的所有文字內容，不包含子tag的文字內容。以列表形式返回。'''
    return tuple([str(content) for content in tag.contents if isinstance(content, NavigableString)])

def selfText(tag:Tag, joinStr="")->str:
    '''取得tag自身的所有文字內容，不包含子tag的文字內容。自動將列表內容以joinStr連接。'''
    return joinStr.join(selfTexts(tag))


__all__ = ['selfTexts', 'selfText']
