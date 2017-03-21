#!/usr/bin/env python
# coding=utf-8

"""
@version 1.0
@author shinpachi8
@date 17/03/21

FOR URL COLLECTION,
暂不支持中文搜索
"""


import sys
import json
import argparse
import os
import random
import chardet
from requests import get
from urllib import quote
from bs4 import BeautifulSoup
from pprint import pprint
from time import sleep





# socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 1080)
# socket.socket = socks.socksocket



header = {
    "User-Agent" : ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3)"
        " AppleWebKit/537.36 (KHTML, like Gecko)"
        " Chrome/56.0.2924.87 Safari/537.36"),

}
# raw_input("input what you want crawl:")

path = "/search?q={}&oq={}&hl=zh"
host = "https://www.google.com"
proxy = {
    "http" : "socks5://127.0.0.1:1080",
    "https" : "socks5://127.0.0.1:1080"
}


result = {}
def check_old():
    # 检查是否有旧的result文件
    global result
    if os.path.isfile("google-crawl.json"):
        with open("google-crawl.json", "rb") as fp:
            result = json.load(fp)

def save():
    with open("google-crawl.json", "w") as fp:
        json.dump(result, fp)

def test():
    # 测试是否可以访问google
    try:
        res = get("https://www.google.com", headers=header, timeout=20, proxies=proxy)
        # pprint(res.headers)
        return True
    except Exception as e:
        pprint("timeout or cannot connect: {}".format(str(e)))


def parse(preurl, html):
    # 解析HTML
    soup = BeautifulSoup(html, "html.parser")
    try:
        h3s = soup.select("h3")
        print len(h3s)
        for h3 in h3s:
            if h3.select("a"):
                alist = h3.select("a")[0]
                result[alist.text] = alist["href"]

        pprint(result)
        tmp = soup.select(".pn")[0]
        return tmp["href"]
    except Exception as e:
        pprint("May be got the capcher. SO  wait 10s")
        pprint("{}".format(str(e)))
        sleep(10)
        return preurl


def collection(args):
    # 收集信息
    if not test():
        pprint("Sorry, Check YOU SOCKS5 PROXY")
        sys.exit(-1)


    search = args.key.decode("utf-8")
    if args.filetype:
        search += " filetype:{}".format(args.filetype)
    if args.inurl:
        search += " inurl:{}".format(args.inurl)
    print search
    tmp = path.format(quote(search), quote(search))
    print tmp

    try:
        count = 1
        while count < 200:
            res = get(host + tmp, headers=header, timeout=20, proxies=proxy)
            # pprint(res.text)

            tmp = parse(tmp, res.text)
            pprint("now, crawl {} pages".format(count))
            count += 1
            # 随机延时2，8s
            sleep(random.randint(2,8))

    except Exception as e:
        pprint("Error Happend: {}".format(str(e)))
        result["stop_url"] = tmp
        save()


def parse_param():
    parser =  argparse.ArgumentParser()
    parser.add_argument("--filetype", help="the filetype")
    parser.add_argument("--inurl", help="inurl")
    parser.add_argument("key", help="key word to search")
    try:
        args = parser.parse_args()
        return args
    except Exception as e:
        parser.print_usage()
        exit(0)
    # if args.filetype is None or args.host is None:
    #     parser.print_usage()
    #     exit(0)
    # else:
    #     return args



if __name__ == '__main__':
    # collection()
    args = parse_param()
    pprint(args)
    print chardet.detect(args.key)
    print args.filetype
    # collection(args)

