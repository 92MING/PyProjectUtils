import socket, requests
import netifaces

def getLocalIP():
    # 获取IP地址
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

def getGlobalIP():
    # 获取外网ip地址
    url = 'https://api.ipify.org'
    response = requests.get(url)
    return response.text

def getSubMask():
    ip_address = getLocalIP()
    # 遍历所有网卡获取子网掩码
    for interface in netifaces.interfaces():
        addrs = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addrs:
            for addr in addrs[netifaces.AF_INET]:
                if addr['addr'] == ip_address:
                    return addr['netmask']
    return None

def checkIpInSameSubnet(ip1, ip2, submask):
    # 检查两个ip是否在同一个子网
    ip1 = [int(i) for i in ip1.split('.')]
    ip2 = [int(i) for i in ip2.split('.')]
    submask = submask.split('.')
    for i in range(4):
        if (ip1[i] & int(submask[i])) != (ip2[i] & int(submask[i])):
            return False
    return True

import stun
from .SingleEnum import SingleEnum
class NATtype(SingleEnum):
    Unknown = 0
    Blocked = 1
    OpenInternet = 2
    FullCone = 3
    SymmetricUDPFirewall = 4
    RestricNAT = 5
    RestricPortNAT = 6
    SymmetricNAT = 7
def get_globalIP_and_NATtype()->(str, NATtype):
    # 获取NAT类型
    natType, ip, _ = stun.get_ip_info()
    if natType==stun.Blocked:
        natType = NATtype.Blocked
    elif natType==stun.OpenInternet:
        natType = NATtype.OpenInternet
    elif natType==stun.FullCone:
        natType = NATtype.FullCone
    elif natType==stun.SymmetricUDPFirewall:
        natType = NATtype.SymmetricUDPFirewall
    elif natType==stun.RestricNAT:
        natType = NATtype.RestricNAT
    elif natType==stun.RestricPortNAT:
        natType = NATtype.RestricPortNAT
    elif natType==stun.SymmetricNAT:
        natType = NATtype.SymmetricNAT
    else:
        natType = NATtype.Unknown
    return ip, natType

__all__ = ["getLocalIP", "getSubMask", "checkIpInSameSubnet", "getGlobalIP", "get_globalIP_and_NATtype", "NATtype"]
