# -*- coding: utf-8 -*-
from .GlobalValue import *
from abc import ABCMeta

class SingleManager(metaclass=ABCMeta):
    '''A singleton manager class.'''
    _instance = None

    def __new__(cls, *args, **kwargs):
        if HasGlobalValue(cls.__qualname__):
            return GetGlobalValue(cls.__qualname__)
        else:
            cls._instance = super().__new__(cls)
            SetGlobalValue(cls.__qualname__, cls._instance)
            cls.__init__(cls._instance, *args, **kwargs)
            cls.__init__ = lambda *args: None
            cls._instance.__init__ = lambda *args: None
            cls.__call__ = lambda *args: cls._instance
            return cls._instance

    @classmethod
    def instance(cls):
        return cls()

__all__ = ["SingleManager"]