# -*- coding: utf-8 -*-
'''常用的類型相關函數，例如類型檢查等'''

from typing import *

def simpleSubClassCheck(smallerCls, largerCls):
    '''檢查smallerCls是否是largerCls的子類，支持Union、Optional、Sequence、Iterable、Mapping、Callable等類型。'''
    def _checkTypes(smallerTypes, largerTypes):
        if Any in largerTypes:
            return True
        for smallerType in smallerTypes:
            ok = False
            for largerType in largerTypes:
                if simpleSubClassCheck(smallerType, largerType):
                    ok = True
                    break
            if not ok:
                return False
        return True
    if largerCls == Any:
        return True
    elif smallerCls == Any:
        return False
    smallerTypeOrigin = get_origin(smallerCls)
    largerTypeOrigin = get_origin(largerCls)
    if smallerTypeOrigin is None and largerTypeOrigin is None:
        return issubclass(smallerCls, largerCls)
    elif smallerTypeOrigin is not None and largerTypeOrigin is None:
        return issubclass(smallerTypeOrigin, largerCls)
    elif smallerTypeOrigin is None and largerTypeOrigin is not None:
        if not issubclass(smallerCls, largerTypeOrigin):
            return False
        if len(get_args(largerCls)) == 0:
            return True
        return False
    else:
        if smallerTypeOrigin in (Union, Optional):
            if largerTypeOrigin not in (Union, Optional):
                return False
            smallerTypes = get_args(smallerCls)
            largerTypes = get_args(largerCls)
            return _checkTypes(smallerTypes, largerTypes)
        else:
            if not issubclass(smallerTypeOrigin, largerTypeOrigin):
                return False
            if issubclass(smallerTypeOrigin,Sequence) or issubclass(smallerTypeOrigin, Iterable):
                smallerArgType = get_args(smallerCls)[0]
                largerArgType = get_args(largerCls)[0]
                return simpleSubClassCheck(smallerArgType, largerArgType)
            elif issubclass(smallerTypeOrigin, Mapping):
                smallerKeyType, smallerValueType = get_args(smallerCls)
                largerKeyType, largerValueType = get_args(largerCls)
                return simpleSubClassCheck(smallerKeyType, largerKeyType) and simpleSubClassCheck(smallerValueType, largerValueType)
            elif issubclass(smallerTypeOrigin, Callable):
                smallerClsArgs = get_args(smallerCls)
                largerClsArgs = get_args(largerCls)
                smallerAgrTypes, smallerReturnType = smallerClsArgs[0], smallerClsArgs[-1]
                largerArgTypes, largerReturnType = largerClsArgs[0], largerClsArgs[-1]
                if len(smallerAgrTypes) != len(largerArgTypes):
                    return False
                return _checkTypes(smallerAgrTypes, largerArgTypes) and simpleSubClassCheck(smallerReturnType, largerReturnType)
            else:
                raise Exception('unsupported types--- smaller:', smallerTypeOrigin, ' larger:',largerTypeOrigin)

def simpleTypeCheck(value, targetType):
    '''檢查value是否是targetType的實例，支持Union、Optional、Sequence、Iterable、Mapping、Callable等類型。'''
    if get_origin(targetType) is None:
        return isinstance(value, targetType)
    else:
        argTypes = get_args(targetType)
        origin = get_origin(targetType)
        if origin == Union or origin == Optional:
            for argType in argTypes:
                if simpleTypeCheck(value, argType):
                    return True
            return False
        else:
            if not isinstance(value, origin):
                return False
            if issubclass(origin, Sequence):
                for i, argType in enumerate(argTypes):
                    if not simpleTypeCheck(value[i], argType):
                        return False
                return True
            elif issubclass(origin, Mapping):
                keyType, valueType = argTypes
                for key, val in value.items():
                    if not simpleTypeCheck(key, keyType) or not simpleTypeCheck(val, valueType):
                        return False
                return True
            elif issubclass(origin, Callable):
                callArgTypes, returnType = *argTypes[:-1], argTypes[-1]
                valueArgTypes = get_type_hints(value)
                varNames = value.__code__.co_varnames
                for varName in varNames:
                    if varName not in valueArgTypes:
                        continue # ignore unlabeled arguments
                    if not simpleSubClassCheck(valueArgTypes[varName], callArgTypes[varNames.index(varName)]):
                        return False
                if 'return' in valueArgTypes:
                    if not simpleSubClassCheck(valueArgTypes['return'], returnType):
                        return False
                return True
            else:
                raise Exception('not supported checking type: ' + str(origin))

__all__ = ['simpleSubClassCheck', 'simpleTypeCheck']
