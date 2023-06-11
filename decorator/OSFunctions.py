# -*- coding: utf-8 -*-
'''用于跨平台的修飾器'''

import platform
from ..base_class.CrossModuleEnum import CrossModuleEnum
from ..base_class.CrossModuleClass import CrossModuleClass
import copy

class OSType(CrossModuleEnum):
    '''操作系统类型'''
    WINDOWS = 1
    MAC = 2
    LINUS = 3
    JAVA = 4
    @staticmethod
    def CurrentOS():
        '''获取当前操作系统类型'''
        if platform.system() == 'Windows':
            return OSType.WINDOWS
        elif platform.system() == 'Darwin':
            return OSType.MAC
        elif platform.system() == 'Linux':
            return OSType.LINUS
        elif platform.system() == 'Java':
            return OSType.JAVA
        else:
            return None

class OSfunction(CrossModuleClass):
    '''用于标记函数在不同操作系统下的实现'''

    _OSfunctions = {}
    def __new__(cls, OS:OSType, func):
        if func.__qualname__ in OSfunction._OSfunctions.keys():
            return OSfunction._OSfunctions[func.__qualname__]
        else:
            thisObj = super().__new__(cls)
            thisObj.funcName = func.__qualname__
            thisObj.thisFuncs = {}
            OSfunction._OSfunctions[func.__qualname__] = thisObj
            return thisObj
    def __init__(self, OS:OSType, func):
        self.thisFuncs[OS.value] = copy.copy(func)
    def __call__(self, *args, **kwargs):
        try:
            return self.thisFuncs[OSType.CurrentOS().value](*args, **kwargs)
        except KeyError:
            self.thisFuncs[OSType.CurrentOS().value] = lambda *args, **kwargs: print(f"{self.funcName} is not implemented on {OSType.CurrentOS().name}")
            return self.thisFuncs[OSType.CurrentOS().value](*args, **kwargs)
    def __get__(self, instance=None, owner=None):
        if instance is None:
            pass
        else:
            try:
                return self.thisFuncs[OSType.CurrentOS().value].__get__(instance, owner)
            except:
                self.thisFuncs[OSType.CurrentOS().value] = lambda *args, **kwargs: print(f"{self.funcName} is not implemented on {OSType.CurrentOS().name}")
                return self.thisFuncs[OSType.CurrentOS().value].__get__(instance, owner)

def WinFunction(func):
    '''装饰器，用于标记该函数在Windows下的实现'''
    return OSfunction(OSType.WINDOWS, func)
def StaticWinFunction(func):
    '''装饰器，用于标记该静态函数在Windows下的实现'''
    return staticmethod(OSfunction(OSType.WINDOWS, func))

def MacFunction(func):
    '''装饰器，用于标记该函数在Mac下的实现'''
    return OSfunction(OSType.MAC, func)
def StaticMacFunction(func):
    '''装饰器，用于标记该静态函数在Mac下的实现'''
    return staticmethod(OSfunction(OSType.MAC, func))

def LinuxFunction(func):
    '''装饰器，用于标记该函数在Linux下的实现'''
    return OSfunction(OSType.LINUS, func)
def StaticLinuxFunction(func):
    '''装饰器，用于标记该静态函数在Linux下的实现'''
    return staticmethod(OSfunction(OSType.LINUS, func))

def JavaFunction(func):
    '''装饰器，用于标记该函数在Java虚拟机下的实现'''
    return OSfunction(OSType.JAVA, func)
def StaticJavaFunction(func):
    '''装饰器，用于标记该静态函数在Java虚拟机下的实现'''
    return staticmethod(OSfunction(OSType.JAVA, func))

__all__ = ["OSType", "WinFunction", "StaticWinFunction", "MacFunction", "StaticMacFunction", "LinuxFunction", "StaticLinuxFunction", "JavaFunction", "StaticJavaFunction"]