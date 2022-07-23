import os
import platform

import requests
from requests import exceptions

# key对应的是映射后的url(保持唯一性) value 对应的是节点名称(也就是服务名称)

ENHANCE_GITHUB_URL = "https://gitlab.com/ineo6/hosts/-/raw/master/next-hosts"
# 备用地址
ENHANCE_GITHUB_URL_BAK = "https://raw.hellogithub.com/hosts"

new_url_ip_dic = {}
HOSTS_PATH = "C:/Windows/System32/drivers/etc/hosts"
DNS_FLUSH = "ipconfig /flushdns"

node_name_ip_dict = {}


def platformAdapter():
    if ("Linux" == platform.system()):
        HOSTS_PATH = "/etc/hosts"
        # CentOS需要提前安装 nscd
        DNS_FLUSH = "nscd -i hosts"


def load_github_hosts():
    resp_context = ""
    try:
        resp_context = requests.session().get(ENHANCE_GITHUB_URL).text
    except exceptions.HTTPError as e:
        # 备用地址
        print(e)
        resp_context = requests.session().get(ENHANCE_GITHUB_URL_BAK).text
    except exceptions.Timeout as ee:
        print(ee)
    if bool(resp_context):
        context_lines = resp_context.split("\n")
        for line in context_lines:
            if (bool(line)) and not line.startswith("#"):
                ip_url_list = line.split()
                new_url_ip_dic[ip_url_list[1]] = ip_url_list[0]
            else:
                continue
        print(new_url_ip_dic)


updated_url = []


def update_hosts():
    if not bool(new_url_ip_dic):
        print('new_url_ip_dic is null')
        os.system.exit()
    newHostContents = ""
    with open(r'' + HOSTS_PATH, 'r', encoding='UTF-8') as filerReader:
        lines = filerReader.readlines()
        for currLine in lines:
            hosts_old_ip_url = currLine.split(" ")
            old_url = hosts_old_ip_url[1].strip('\n')
            if (old_url in new_url_ip_dic.keys()):
                currLine = currLine.replace(currLine, new_url_ip_dic[old_url] + " " + old_url + "\n")
                updated_url.append(old_url)
            newHostContents += currLine
    # 对待添加的IP进行添加
    ready_add_url_ip = new_url_ip_dic.keys() - updated_url
    if not bool(ready_add_url_ip):
        for curr_url in ready_add_url_ip:
            newHostContents += new_url_ip_dic[curr_url] + " " + curr_url + "\n"
            print(new_url_ip_dic[curr_url] + " " + curr_url + "is added")
    with open(r'' + HOSTS_PATH, 'w', encoding='UTF-8') as fileWriter:
        fileWriter.write(newHostContents)


if __name__ == '__main__':
    platformAdapter()
    load_github_hosts()
    update_hosts()
    os.system(DNS_FLUSH)
    print("hosts is update")
    os.system('pause')
