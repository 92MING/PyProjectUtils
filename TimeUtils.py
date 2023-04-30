import time
from datetime import datetime

def GetTimeStamp()->float:
    return time.time()

def GetDateTimeFromTimeStamp(timeStamp:float):
    return datetime.fromtimestamp(timeStamp)

__all__ = [ 'GetTimeStamp', 'GetDateTimeFromTimeStamp' ]
