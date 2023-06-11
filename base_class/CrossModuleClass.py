# -*- coding: utf-8 -*-
'''跨模組類，無論在哪裡import，都會得到相同的類'''

from ..utils.GlobalValueUtils import *

class CrossModuleClassMeta(type):
    '''跨模組類的Meta class'''
    def __new__(cls, *args, **kwargs):
        clsName = args[0]
        if HasGlobalValue(clsName):
            return GetGlobalValue(clsName)
        else:
            thisCls = super().__new__(cls, *args, **kwargs)
            SetGlobalValue(clsName, thisCls)
            return thisCls

class CrossModuleClass(metaclass=CrossModuleClassMeta):
    '''跨模組類，無論在哪裡import，都會得到相同的類'''
    pass

__all__ = ["CrossModuleClass", "CrossModuleClassMeta"]