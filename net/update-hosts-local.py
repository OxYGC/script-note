import os
import socket
import platform

# 这里要更新局域网hosts的主机名称 key对应的是你目标主机名称
# key对应的是映射后的url(保持唯一性) value 对应的是节点名称(也就是服务名称)

url_node_dict = {'nas.com':'YGC-NAS',
                 'mws.com':'THINK-YANG',
                 'mwsvm0.com': 'mwsvm0'}


node_name_list = url_node_dict.values()
# windows 的默认hosts路径


HOSTS_PATH = "C:/Windows/System32/drivers/etc/hosts"
flushdns = "ipconfig /flushdns"
node_nameip_dict = {}


def platformAdapter():
    if ("Linux" ==  platform.system()):
        hostsPath ="/etc/hosts"
        # CentOS需要提前安装 nscd
        flushdns = "nscd -i hosts"


def findSvrIpByName():
    for node_name in node_name_list:
        try:
            node_ip = socket.gethostbyname(node_name)
            print("host: " + node_name + " IP: " + node_ip)
            node_nameip_dict[node_name] = node_ip
        except:
            print("node: " + node_name + " IP not found")



def udpateHostInfo():
    if not bool(node_nameip_dict):
        print('node_nameip_dict is null')
        os.system.exit()

    updatedHostIp = set()
    newHostContents = ""
    with open(r''+ HOSTS_PATH, 'r', encoding='UTF-8') as filerReader:
        lines = filerReader.readlines()
        for currLine in lines:
            hosts_old_ip_url = currLine.split(" ")
            old_url = hosts_old_ip_url[1].strip('\n')
            if (old_url in url_node_dict.keys()):
                currLine = currLine.replace(currLine, node_nameip_dict[url_node_dict[old_url]]+" "+ old_url + "\n")
            newHostContents += currLine
    with open(r''+ HOSTS_PATH, 'w', encoding='UTF-8') as fileWriter:
        fileWriter.write(newHostContents)


# 打印文本已替换
platformAdapter()
findSvrIpByName()
udpateHostInfo()

os.system(flushdns)
print("hosts is update")
os.system('pause')
