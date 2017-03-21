#! /usr/bin/env python
# coding=utf-8


import urllib
import httplib
from bs4 import BeautifulSoup

class crawl():
    header = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36"}
    def __init__(self, arg1, arg2="/"):
        self.url = arg1
        self.path = arg2

    # test if the website can be connect
    def test_connect(self):
        self.conn = httplib.HTTPConnection(self.url, 80)
        self.conn.request("GET", self.path, headers=self.header)
        self.response = self.conn.getresponse()
        if self.response.status == 200:
            return True
        else:
            return False

    def parse_html(self):
        
        html = self.response.read().decode("gbk").encode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        lists= soup.find_all('div', id='list')[0]
        soup2 = BeautifulSoup(str(lists), "html.parser")
        a_list = soup2.find_all('a')
#        print lists
#        for i in a_list:
#            print i['href'], i.text
        self.url_list = [self.path+i['href'] for i in a_list]
        self.tile = [i.text for i in a_list]


    def write_file(self):
        self.conn.request("GET", self.url_list[0], headers=self.header)
        html = self.conn.getresponse().read()
        soup = BeautifulSoup(html,"html.parser")
        title = soup.find("h1").get_text()
        print title
        content = soup.find_all("div", id="content")[0]
        print content.get_text()

if __name__ =='__main__':
    a = crawl("www.biquge.la", "/book/174/")
    if a.test_connect():
        print "connect OK!"
        a.parse_html()
        a.write_file()
    else:
        print "Connect false"
    
#    html = '<div class="aa"><div id="list"><p>aaaaaaa</p></div></div>'
#    file  = open("/Users/jiaxiaoyan/Desktop/test.html","r")
#    html = file.readall()
#    soup = BeautifulSoup(html, "html.parser")
#    lists = soup.find_all("div",id="list")
#    print lists
