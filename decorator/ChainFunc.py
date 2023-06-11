# -*- coding: utf-8 -*-
'''連鎖function，返回自己，可以自定義before和final。連鎖前調用before，連鎖後調用final。主要用於數據庫操作'''

from types import FunctionType
from ..base_class import CrossModuleClass
class ChainFunc(CrossModuleClass):
    '''連鎖function，返回自己，可以自定義before和final。連鎖前調用before，連鎖後調用final。主要用於數據庫操作'''

    _FinalFuncs = {} # {className: func}
    _BeforeFuncs = {} # {className: {funcName: func}}

    _currentChainFuncs = []
    _currentObj = None
    _counter = 0

    class Chain:
        '''單個Chain'''
        def __new__(cls, *args, **kwargs):
            obj = super().__new__(cls)
            ChainFunc._counter += 1
            obj.counter = ChainFunc._counter
            return obj
        def __call__(self, *args, **kwargs):
            lastFunc = ChainFunc._currentChainFuncs.pop()
            ChainFunc._currentChainFuncs.append(lambda: lastFunc(ChainFunc._currentObj, *args, **kwargs))
            return self
        def __getattr__(self, item):
            return getattr(ChainFunc._currentObj, item)
        def __del__(self):
            '''刪除時，如何沒有下一個Chain，則調用所有連鎖函數'''
            if self.counter == ChainFunc._counter: # end of chain func
                currentClsName = ChainFunc._currentObj.__class__.__qualname__
                if currentClsName in ChainFunc._BeforeFuncs:
                    ChainFunc._BeforeFuncs[currentClsName](ChainFunc._currentObj)
                for func in ChainFunc._currentChainFuncs:
                    func()
                if currentClsName in ChainFunc._FinalFuncs:
                    ChainFunc._FinalFuncs[currentClsName](ChainFunc._currentObj)
                ChainFunc._counter = 0
                ChainFunc._currentChainFuncs = []
                ChainFunc._currentObj = None

    def final(func):
        '''連鎖結束時調用，注意註冊的函數名稱必須不能重複，且必須在類中'''
        if not isinstance(func, FunctionType):
            raise Exception('ChainFunc.final can only be used on functions')
        names = func.__qualname__.split('.')
        if len(names) < 2:
            raise Exception('ChainFunc.final can only be used within a class')
        if func.__code__.co_argcount != 1:
            raise Exception('ChainFunc.final can only be used on functions with "self" as the only argument')
        className, funcName = names[-2:]
        if className not in ChainFunc._FinalFuncs:
            ChainFunc._FinalFuncs[className] = func
        else:
            raise Exception('ChainFunc.final can only be used once in a class')
        return func
    def before(func):
        '''連鎖開始前調用，注意註冊的函數名稱必須不能重複，且必須在類中'''
        if not isinstance(func, FunctionType):
            raise Exception('ChainFunc.before can only be used on functions')
        names = func.__qualname__.split('.')
        if len(names) < 2:
            raise Exception('ChainFunc.before can only be used within a class')
        if len(func.__code__.co_varnames) != 1:
            raise Exception('ChainFunc.before can only be used on functions with "self" as the only argument')
        className, funcName = names[-2:]
        if className not in ChainFunc._BeforeFuncs:
            ChainFunc._BeforeFuncs[className] = func
        else:
            raise Exception('ChainFunc.before can only be used once in a class')
        return func
    def __new__(cls, func):
        obj= super().__new__(cls)
        names = func.__qualname__.split('.')
        if len(names) < 2:
            raise Exception('ChainFunc can only be used within a class')
        obj.func = func
        return obj
    def __get__(self, instance, owner):
        if instance is None:
            raise Exception('ChainFunc can only be used within the an instance')
        if ChainFunc._currentObj is None:
            ChainFunc._currentObj = instance
        else:
            if instance != ChainFunc._currentObj:
                print("ChainFunc: instance", instance, "and currentObj", ChainFunc._currentObj, "are not the same!!")
                raise Exception('ChainFunc can only be used within the same object')
        ChainFunc._currentChainFuncs += [self.func]
        return ChainFunc.Chain()

__all__ = ['ChainFunc']