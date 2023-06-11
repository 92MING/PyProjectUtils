# -*- coding: utf-8 -*-
'''跨模組Enum，無論在哪裡import，都返回同一個Enum類。名稱不能重複'''

from ..utils.GlobalValueUtils import *
_CrossModuleEnumDict = GetOrAddGlobalValue("_CrossModuleEnumDict", dict())
from enum import Enum

class CrossModuleEnumMeta(type):
    def __new__(cls, *args, **kwargs):
        clsName = args[0]
        if clsName in _CrossModuleEnumDict:
            return _CrossModuleEnumDict[clsName]
        else:
            class ThisEnum(Enum):
                pass
            _CrossModuleEnumDict[clsName] = ThisEnum
            return ThisEnum

class CrossModuleEnum(metaclass=CrossModuleEnumMeta):
    '''跨模組Enum，無論在哪裡import，都返回同一個Enum類。名稱不能重複'''
    pass


__all__ = ["CrossModuleEnum", "CrossModuleEnumMeta"]