# -*- coding: utf-8 -*-
'''多鍵字典，可以用多個鍵值查找對應的值'''

from typing import Tuple, Sequence, Dict
from ..utils.CryptoUtils import generateUUID

class MultiKeyDict:

    _objects = {} #id, object
    _idDict = {} #id, {keyName: key}
    _dicts = {} #keyName, {key: id}
    _keyNames:Tuple = None

    def __init__(self, keyNames:Sequence, *args):
        '''must provide keynames by a sequence or multiple arguments'''
        if isinstance(keyNames, str):
            self._keyNames = tuple([keyNames, *args])
        elif isinstance(keyNames, Sequence):
            self._keyNames = tuple(keyNames)
        else:
            raise ValueError(f"must provide keynames by a sequence or multiple arguments")
        self._dicts = {}
        self._objects = {}
        for keyName in self._keyNames:
            self._dicts[keyName] = {}
    @property
    def keyNames(self) -> Tuple:
        return self._keyNames

    def _hasKeyName(self, keyName:str) -> bool:
        return keyName in self._keyNames
    def _unpackKey(self, keyNameAndKey):
        if isinstance(keyNameAndKey, Sequence):
            if len(keyNameAndKey) == 2:
                keyName, key = keyNameAndKey
                return keyName, key
            elif len(keyNameAndKey) == 1:
                keyName = keyNameAndKey[0]
                return keyName, None
            else:
                raise ValueError(f"keyNameAndKey should be a tuple with length 1 or 2, but got {len(keyNameAndKey)}")
        elif isinstance(keyNameAndKey, str):
            return keyNameAndKey, None
        else:
            raise ValueError(f"keyNameAndKey should be a tuple or string, but got {type(keyNameAndKey)}")
    def __setitem__(self, keyNameAndkey, value):
        """return set(keyName, key, value)"""
        keyName, key = self._unpackKey(keyNameAndkey)
        self.set(keyName, key, value)
    def __getitem__(self, keyNameAndKey):
        """if only 1 argument, return getDict(keyName), else return get(keyName, key)"""
        keyName, key = self._unpackKey(keyNameAndKey)
        if not self._hasKeyName(keyName):
            raise KeyError(f"{keyName} is not a valid key name")
        if key is not None:
            try:
                return self._objects[self._dicts[keyName][key]]
            except KeyError:
                raise KeyError(f"{keyName} with key {key} does not exist")
        else:
            return self.getDict(keyName)
    def __contains__(self, keyNameAndKey):
        """if 2 args, return hasKey(keyName, key).
            if 1 arg, return True if keyname in all keynames"""
        keyName, key = self._unpackKey(keyNameAndKey)
        if key is None:
            if not self._hasKeyName(keyName):
                raise KeyError(f"{keyName} is not a valid key name")
            return keyName in self.keyNames
        else:
            return key in self._dicts[keyName]
    def __repr__(self):
        return f"<MultiKeyDict{self._keyNames}>"
    def __str__(self):
        return f"<MultiKeyDict{self._keyNames}>"
    def __iter__(self):
        """iter all objects, with no keys"""
        return iter(self._objects.values())
    def __len__(self):
        """return the number of objects, not keys"""
        return len(self._objects)

    def hasKey(self, keyName, key):
        """return True if key is existed in the target dict"""
        if not self._hasKeyName(keyName):
            raise KeyError(f"{keyName} is not a valid key name")
        return key in self._dicts[keyName]
    def keys(self, keyName):
        """return a tuple of keys of the target dict"""
        if not self._hasKeyName(keyName):
            raise KeyError(f"{keyName} is not a valid key name")
        return self._dicts[keyName].keys()
    def values(self, keyName=None):
        """if kayname is given, return a tuple of values of the target dict.
           else return a tuple of all values of all dicts"""
        if keyName is not None:
            if not self._hasKeyName(keyName):
                raise KeyError(f"{keyName} is not a valid key name")
            ret = []
            for key, value in self._dicts[keyName].items():
                ret.append(self._objects[value])
            return tuple(ret)
        else:
            return tuple(self._objects.values())
    def items(self, keyName):
        """return a tuple of (key, value) of the target dict"""
        if not self._hasKeyName(keyName):
            raise KeyError(f"{keyName} is not a valid key name")
        ret = {}
        for key, value in self._dicts[keyName].items():
            ret[key] = self._objects[value]
        return ret.items()
    def get(self, keyName, key, default=None):
        """if key is None, return a copy dict of {key: value},
           else return value"""
        if not self._hasKeyName(keyName):
            raise KeyError(f"{keyName} is not a valid key name")
        if key is not None:
            try:
                return self._objects[self._dicts[keyName][key]]
            except KeyError:
                return default
        else:
            return self.getDict(keyName)
    def getID(self, keyName, key):
        """return real id"""
        if not self._hasKeyName(keyName):
            raise KeyError(f"{keyName} is not a valid key name")
        try:
            return self._dicts[keyName][key]
        except KeyError:
            raise KeyError(f"{keyName} with key {key} does not exist")
    def getDict(self, keyName):
        """return a copy dict of {key: value}"""
        if not self._hasKeyName(keyName):
            raise KeyError(f"{keyName} is not a valid key name")
        ret = {}
        for _key, _id in self._dicts[keyName].items():
            ret[_key] = self._objects[_id]
        return ret
    def set(self, keyName, key, value):
        """set value by keyName and key. Key must be existed in the target dict"""
        if not self._hasKeyName(keyName):
            raise KeyError(f"{keyName} is not a valid key name")
        if key in self._dicts[keyName]:
            self._objects[self._dicts[keyName][key]] = value
        else:
            raise KeyError(f"{key} is not a valid key")
    def add(self, KeyNamesAndKeys:Dict[str, any], value):
        for keyName, key in KeyNamesAndKeys.items():
            if not self._hasKeyName(keyName):
                raise KeyError(f"{keyName} is not a valid key name")
            if key in self._dicts[keyName]:
                raise KeyError(f"{keyName}:{key} is already occupied")
        id = generateUUID()
        self._objects[id] = value
        self._idDict[id] = KeyNamesAndKeys
        for keyName, key in KeyNamesAndKeys.items():
            self._dicts[keyName][key] = id
    def setKey(self, id, keyName, key):
        """set a key to the target obj with the id"""
        if not self._hasKeyName(keyName):
            raise KeyError(f"{keyName} is not a valid key name")
        if id not in self._objects:
            raise KeyError(f"{id} is not a valid id")
        if key in self._dicts[keyName] and self._dicts[keyName][key] != id:
            raise KeyError(f"{keyName}:{key} is already occupied by {self._dicts[keyName][key]}")
        self._idDict[id][keyName] = key
        self._dicts[keyName][key] = id
    def pop(self, keyName, key):
        """will remove from all dicts having the same object"""
        if not self._hasKeyName(keyName):
            raise KeyError(f"{keyName} is not a valid key name")
        if key in self._dicts[keyName]:
            id = self._dicts[keyName].pop(key)
            for _keyName, _key in self._idDict[id].items():
                if _keyName != keyName and _key in self._dicts[_keyName]:
                    self._dicts[_keyName].pop(_key)
            return self._objects.pop(id)
        else:
            raise KeyError(f"{keyName}:{key} is not exist")
    def clear(self):
        self._dicts.clear()
        for keyName in self._keyNames:
            self._dicts[keyName] = {}

__all__ = ["MultiKeyDict"]