# -*- coding: utf-8 -*-
'''事件类，用于实现事件机制。比PYQT原生Signal輕量，不需要QObject'''

from types import FunctionType, MethodType
from typing import Callable, Iterable

class Event:
    def __init__(self, *args):
        for arg in args:
            if not isinstance(arg, type):
                raise Exception("Event's arg must be type")
        self.args = tuple(args)
        self._events = []

    def __iadd__(self, other):
        self.addListener(other)
        return self

    def __isub__(self, other):
        self.removeListener(other)
        return self

    @property
    def events(self)->tuple:
        '''return a tuple of events'''
        return tuple(self._events)

    @property
    def events_iter(self)->Iterable:
        '''return a iterator of events'''
        return iter(self._events)

    def addListener(self, listener:Callable):
        '''add a listener to event'''
        if isinstance(listener,FunctionType):
            argLength = listener.__code__.co_argcount
        elif isinstance(listener,MethodType):
            argLength = listener.__code__.co_argcount - 1
        else:
            raise Exception("Listener must be function or method")
        if len(self.args) != argLength:
            raise Exception("Listener's arg length not match")
        self._events.append(listener) if listener not in self.events else None

    def removeListener(self, listener:Callable):
        '''remove a listener from event'''
        self._events.remove(listener)

    def invoke(self, *args):
        '''invoke all listeners'''
        if len(args) < len(self.args):
            argNeeded = self.args[len(args):]
            outputStr = ""
            for arg in argNeeded:
                outputStr += f"{arg.__qualname__}, "
            outputStr = outputStr[:-2]
            raise Exception(f"Parameter: {outputStr[:-2]} are not provided")
        elif len(args) > len(self.args):
            raise Exception(f"Too many parameters")
        for i,arg in enumerate(args):
            if type(arg) is not self.args[i]:
                raise Exception(f"Parameter: {arg} is not {self.args[i].__qualname__}")
        for event in self.events:
            event(*args)

    def eventsCount(self):
        '''return the count of events'''
        return len(self._events)

    def clear(self):
        '''clear all events'''
        self._events.clear()

__all__ = ["Event"]