import os
import socket
import platform

# 这里要更新局域网hosts的主机名称 key对应的是主机名称 value 对应的是ip对应的host的名称

targetSvrHost = {"THINK-YANG":"mws.com",'mwsvm0': 'mwsvm0'}


targetSvrName = set(targetSvrHost)
# windows 的默认hosts路径


hostsPath = "C:/Windows/System32/drivers/etc/hosts"
flushdns = "ipconfig /flushdns"
nameIpTable = {}


def platformAdapter():
    if ("Linux" ==  platform.system()):
        hostsPath ="/etc/hosts"
        # CentOS需要提前安装 nscd
        flushdns = "nscd -i hosts"


def findSvrIpByName():
    for svrName in targetSvrName:
        try:
            svrIp = socket.gethostbyname(svrName)
            print("host: " + svrName + " IP: " + svrIp)
            nameIpTable[svrIp] = svrName
        except:
            print("host: " + svrName + " IP not found")


def udpateHostInfo():
    if not bool(nameIpTable):
        print('nameIpTable is null')
        os.system.exit()

    updatedHostIp = set()
    newHostContents = ""
    for svrIp, svrName in nameIpTable.items():
        # waitReplaceStr = ip+" "+hostname + "\n"
        with open(r''+hostsPath, 'r', encoding='UTF-8') as filerReader:
            line = filerReader.readline()
            # waitAddStr = ip+" "+hostname + "\n"
            for inline in line:
                if (inline.find(svrName) > 0):
                    inline = inline.replace(inline, svrIp+" "+targetSvrHost[svrName] + "\n")
                    newHostContents += inline
                    updatedHostIp.add(svrIp)

    readyAddHostIP = set(nameIpTable) - updatedHostIp
    for svrIp, svrName in nameIpTable.items():
        if(svrIp in readyAddHostIP):
            if(bool(newHostContents)):
                newHostContents += svrIp+" "+targetSvrHost[svrName] + "\n"
            else:
                newHostContents += "\n"+svrIp+" "+targetSvrHost[svrName] + "\n"
    with open(r''+hostsPath, 'w', encoding='UTF-8') as fileWriter:
        fileWriter.write(newHostContents)


# 打印文本已替换
platformAdapter()
findSvrIpByName()
udpateHostInfo()
print("hosts is update")
os.system(flushdns)
os.system('pause')

