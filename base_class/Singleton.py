# -*- coding: utf-8 -*-
'''單例模式基類'''

from ..utils.GlobalValueUtils import *

class Singleton:
    '''單例模式基類。单例類也是跨模塊的，所以名稱不可重複'''
    _instance = None # 實例

    def __new__(cls, *args, **kwargs):
        if HasGlobalValue(cls.__qualname__):
            # 如果已經有實例，直接返回
            return GetGlobalValue(cls.__qualname__)
        else:
            # 如果沒有實例，生成實例
            if cls.__qualname__ == "Singleton":
                # 基類不可實例化
                raise Exception("Singleton can't be instantiated directly")
            cls._instance = super().__new__(cls)
            SetGlobalValue(cls.__qualname__, cls._instance)
            cls.__init__(cls._instance, *args, **kwargs)
            cls.__init__ = lambda *args: None
            cls._instance.__init__ = lambda *args: None
            cls.__call__ = lambda *args: cls._instance
            return cls._instance

    def __getattribute__(self, item):
        # getattribute 時，返回類的屬性
        if item == '__class__':
            return super().__getattribute__(item)
        return getattr(self.__class__, item)

    def __setattr__(self, key, value):
        # setattr 時，設置類的屬性
        setattr(self.__class__, key, value)

    @classmethod
    def instance(cls):
        '''如果没有实例，會自動生成'''
        return cls()

__all__ = ["Singleton"]