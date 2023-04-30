import socket, requests
import netifaces

def getLocalIp():
    # 获取本机ip地址和主机名
    hostname = socket.gethostname()
    # 获取IP地址
    return socket.gethostbyname(hostname)

def getGlobalIp():
    # 获取外网ip地址
    url = 'https://api.ipify.org'
    response = requests.get(url)
    return response.text

def getSubMask():
    ip_address = getLocalIp()
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

__all__ = ["getLocalIp", "getSubMask", "checkIpInSameSubnet", "getGlobalIp"]
