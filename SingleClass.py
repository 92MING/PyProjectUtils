# -*- coding: utf-8 -*-
from .GlobalValue import *

class SingleClssMeta(type):
    def __new__(cls, *args, **kwargs):
        clsName = args[0]
        if HasGlobalValue(clsName):
            return GetGlobalValue(clsName)
        else:
            thisCls = super().__new__(cls, *args, **kwargs)
            SetGlobalValue(clsName, thisCls)
            return thisCls

class SingleClass(metaclass=SingleClssMeta):
    pass

__all__ = ["SingleClass"]