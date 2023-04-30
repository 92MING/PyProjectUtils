# -*- coding: utf-8 -*-
import platform
from .SingleEnum import SingleEnum
from .SingleClass import SingleClass
import copy

class OSType(SingleEnum):
    win = 1
    mac = 2
    linux = 3
    java = 4
    @staticmethod
    def CurrentOS():
        if platform.system() == 'Windows':
            return OSType.win
        elif platform.system() == 'Darwin':
            return OSType.mac
        elif platform.system() == 'Linux':
            return OSType.linux
        elif platform.system() == 'Java':
            return OSType.java
        else:
            return None

class OSfunction(SingleClass):
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
    return OSfunction(OSType.win, func)
def StaticWinFunction(func):
    return staticmethod(OSfunction(OSType.win, func))

def MacFunction(func):
    return OSfunction(OSType.mac, func)
def StaticMacFunction(func):
    return staticmethod(OSfunction(OSType.mac, func))

def LinuxFunction(func):
    return OSfunction(OSType.linux, func)
def StaticLinuxFunction(func):
    return staticmethod(OSfunction(OSType.linux, func))

def JavaFunction(func):
    return OSfunction(OSType.java, func)
def StaticJavaFunction(func):
    return staticmethod(OSfunction(OSType.java, func))

__all__ = ["OSType", "WinFunction", "StaticWinFunction", "MacFunction", "StaticMacFunction", "LinuxFunction", "StaticLinuxFunction", "JavaFunction", "StaticJavaFunction"]