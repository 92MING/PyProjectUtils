# -*- coding:utf-8 -*-
'''時間相關工具'''

import time, aiohttp
from datetime import datetime
from typing import Union

def GetTimeStamp()->float:
    '''獲取當前時間戳'''
    return time.time()

def GetDateTimeFromTimeStamp(timeStamp:float)->datetime:
    '''獲取時間戳對應的日期時間'''
    return datetime.fromtimestamp(timeStamp)

def GetCurrentTime(strfFormat:str=None)->Union[datetime,str]:
    '''獲取當天日期時間。 如果strfFormat不為None, 則返回格式化後的字符串'''
    if strfFormat is None:
        return datetime.now()
    else:
        return datetime.now().strftime(strfFormat)
def GetCurrentTime_YYYYMMDD_HHMMSS(withSigns = True)->str:
    '''獲取當天日期時間，格式為YYYYMMDDHHMMSS. withSigns為True時，返回帶有分隔符的字符串，否則返回不帶分隔符的字符串'''
    if withSigns:
        return GetCurrentTime('%Y-%m-%d %H:%M:%S')
    else:
        return GetCurrentTime('%Y%m%d%H%M%S')
def GetCurrentTime_YYYYMMDD(withSigns=True)->str:
    '''獲取當天日期時間，格式為YYYYMMDD, withSigns為True時，返回帶有分隔符的字符串，否則返回不帶分隔符的字符串'''
    if withSigns:
        return GetCurrentTime('%Y-%m-%d')
    else:
        return GetCurrentTime('%Y%m%d')
def GetCurrentTime_HHMMSS(withSigns=True)->str:
    '''獲取當天日期時間，格式為HHMMSS, withSigns為True時，返回帶有分隔符的字符串，否則返回不帶分隔符的字符串'''
    if withSigns:
        return GetCurrentTime('%H:%M:%S')
    else:
        return GetCurrentTime('%H%M%S')

async def GetNetworkTimeStamp():
    '''獲取網絡時間戳'''
    async with aiohttp.ClientSession() as session:
        async with session.get('https://script.google.com/macros/s/AKfycbzaqY4cumh2rRJhLtrVH0T_wOA8MBTTNU0sbKep2e1KHzsMaORR-usrQ2vVYdyrTGt4gA/exec') as resp:
            time = await resp.text()
            return float(time)

__all__ = [ 'GetTimeStamp', 'GetDateTimeFromTimeStamp', 'GetCurrentTime', 'GetCurrentTime_YYYYMMDD_HHMMSS', 'GetCurrentTime_YYYYMMDD', 'GetCurrentTime_HHMMSS' ]
