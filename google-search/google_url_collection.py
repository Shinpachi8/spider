#!/usr/bin/env python
# coding=utf-8

"""
@version 1.1
@author shinpachi8
@date 17/03/26

v1.0: FOR URL COLLECTION,暂不支持中文搜索
v1.1: 修改支持为中文, 多线程。但是测试10个线程跑一次后会被BAN。。。。
"""


import sys
import json
import argparse
import os
import random
import time
import re
import threading
from Queue import Queue
from requests import get
from bs4 import BeautifulSoup
from pprint import pprint
from time import sleep



reload(sys)
sys.setdefaultencoding('utf-8')

header = {
    "User-Agent" : ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3)"
        " AppleWebKit/537.36 (KHTML, like Gecko)"
        " Chrome/56.0.2924.87 Safari/537.36"),
    "Referer" :  "https://www.google.com/",

}
# raw_input("input what you want crawl:")

path = "/search?q={}&filter=0&start="
host = "https://www.google.com"
proxy = {
    "http" : "socks5://127.0.0.1:1080",
    "https" : "socks5://127.0.0.1:1080"
}
lock = threading.Lock()

class GoogleSpider(threading.Thread):
    """docstring for GoogleSpider"""
    def __init__(self, queue, filename):
        super(GoogleSpider, self).__init__()
        threading.Thread.__init__(self)
        self._url_queue = queue
        self._filename = filename

    def run(self):
        while not self._url_queue.empty():
            url = self._url_queue.get()

            self.spider(url)
            sleep(random.randint(5,10))
            pass



    def parse(self, preurl, html):
        # 解析HTML
        soup = BeautifulSoup(html, "lxml")
        try:
            h3s = soup.select("h3")
            print "<=------=>got a page: {}".format(len(h3s))
            assert len(h3s) != 0 # 判断是否被google判断为爬虫
            for h3 in h3s:
                if h3.select("a"):
                    alist = h3.select("a")[0]
                    if lock.acquire(True): # 写文件时保证线程安全，加锁
                        line = "{:<40}\t:\t{:<100}\t:\n".format(alist.text, alist["href"])
                        pprint(line)
                        self._write_file(self._filename, line)
                        lock.release()
                    # result[alist.text.encode("utf-8")] = alist["href"]

            # 写入文件
        except Exception as e:
            pprint("May be got the capcher. SO  wait 10s")
            pprint("{}".format(str(e)))
            sleep(10)
            return preurl


    def spider(self, url):
        # URL： 等解析URL
        try:
            res = get(url, headers=header, proxies=proxy)
            html = res.text  # 得到
            url = self.parse(url, html)
            if url:
                pass
        except Exception, e:
            print "[-] Spider Error Happend: {}".format(e)
            pass


    def _write_file(filename, line):
        with open(filename, "a") as fp:
            fp.write(line)


def test():
    # 测试是否可以访问google
    try:
        res = get("https://www.google.com", headers=header, timeout=10, proxies=proxy)
        # pprint(res.headers)
        return True
    except Exception as e:
        pprint("timeout or cannot connect: {}".format(str(e)))



def parse_param():
    parser =  argparse.ArgumentParser()
    parser.add_argument("--filetype", help="the filetype")
    parser.add_argument("--inurl", help="inurl")
    parser.add_argument("key", help="key word to search")
    parser.add_argument("-o", "--output", help="output file, default key+time.txt")
    try:
        args = parser.parse_args()
        return args
    except Exception as e:
        parser.print_usage()
        exit(0)


def main(args):
    if not test():
        pprint("Sorry, Check YOU SOCKS5 PROXY")
        sys.exit(-1)


    search = args.key
    if args.filetype:
        search += " filetype%3A{}".format(args.filetype)
    if args.inurl:
        search += " inurl%3A{}".format(args.inurl)
    if args.output:
        filename = args.output
    else:
        filename = args.key + time.strftime("%Y-%m-%d") + ".txt"
    print "filename: {}".format(filename)

    # 默认只爬取前100页。
    queue = Queue()
    threads = []
    thread_count = 3
    # 调整线程数
    for i in range(0, 91, 10):
        print "search: {}".format(host + path.format(search) + str(i)).replace(" ", "+")
        queue.put((host + path.format(search) + str(i)).replace(" ", "+"))

    for i in xrange(thread_count):
        threads.append(GoogleSpider(queue, filename))

    for thread in threads:
        thread.start()
        sleep(random.randint(5,8))

    for thread in threads:
        if thread.is_alive():
            thread.join()


if __name__ == '__main__':
    # collection()
    args = parse_param()
    pprint(args)
    print args.filetype
    main(args)

