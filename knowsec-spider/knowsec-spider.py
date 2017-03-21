#! /usr/bin/env python2
# coding=utf-8

import threading
import re
import urllib2
import sqlite3
import logging
import argparse




"""
看到了知道创宇的一个爬虫，就尝试着写了一下，算是第一版本吧
还需要再改进一下，但是写的时间太长了...还得重新看一下....

"""
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", help="the url to start")
    parser.add_argument("-d", default=3, help="the deepth want to crawl")
    parser.add_argument("-l", default=1, help="log level, \
        the bigger, the more")
    parser.add_argument("-f", default="spider.log", help="file to save log")
    parser.add_argument("--thread", default=10, help="the \
        thead number, default 10")
    parser.add_argument("--dbfile", help="db file to save result")
    parser.add_argument("--key", help="the keyword that html contain")
    args = parser.parse_args()
    return args


class db_deal(object):
    """
    this class is about deal
    the db operation
    """
    def __init__(self, path, table):
        """
        create the db
        and set the cursor
        """
        try:
            self.conn = sqlite3.connect(path)
            self.cur = self.conn.cursor()
            self.table = table
        except Exception as e:
            print "connect/cur error for reason {}".format(str(e))
            exit(0)

    def create_db(self):
        """
        create table in db
        each crawl has a special table
        """
        try:
            self.cur.execute(" \
                CREATE TABLE IF NOT EXISTS {} (id INTEGER PRIMARY \
                KEY AUTOINCREMENT,Data VERCHAR(40), \
                url VARCHAR(50))".format(self.table))
            self.conn.commit()
            print "create table done!"
        except Exception as e:
            print "create table error the reason is {}".format(str(e))
            exit(0)

    def insert_data(self, data):
        try:
            self.cur.execute("\
                insert into {}(Data, url) \
                values (?, ?)".format(self.table), data)
            self.conn.commit()
            print "insert Done!"
        except Exception as e:
            print "insert data error.  the reason is {}".format(str(e))
            exit(0)


class MyThread(threading.Thread):
    """ work thread"""
    def __init__(self, workQueue, timeout=30):
        threading.Thread.__init__(self)
        self.workQueue = workQueue
        self.timeout = timeout
        self.setDaemon(True)
        self.start()

    def run(self):
        while True:
            try:
                # TODO  线程锁定
                callable, args = self.workQueue.get(timeout=self.timeout)
                res = callable(*args)
            # 队列空了就退出
            except Queue.Empty:
                break
            except Exception as e:
                print "callable error. the reason is {}".format(str(e))
                exit(0)


class ThreadPool:
    """ write our own threadpool"""
    def __init__(self, num_of_thread):
        self.workQueue = Queue.Queue()
        self.threads = []
        self._createThreadPool(num_of_thread)

    def _createThreadPool(num_of_thread):
        for i in range(num_of_thread):
            thread = MyThread(self.workQueue)
            self.threads.append(thread)

    def wait_for_complete(self):
        while(len(self.threads)):
            thread = self.threads.pop()
            if thread.is_alive():
                thread.join()

    def add_job(self, callable, *args):
        self.workQueue.put(callable, args)



def my_log(level_num, filename):
    """
    create a logger case
    that can be use in anywhere
    """
    level_dict = {"1": "CRITICAL",
        "2": "ERROR",
        "3": "WARNING",
        "4": "INFO",
        "5": "DEBUG"}
    level = level_dict[level_num]
    log_format = '%(filename)s [line:%(lineno)d] [time:%(asctime)s]\
    [level:%(levelname)s] msg: %(message)s'
    logging.basicConfig(filename=filename,
        format = log_format, level = level)
    # logger_name = "example"
    logger = logging.getLogger()
    return logger

class Crawl(object):
    """
    crawl the website
    """
    def __init__(self, tp, table args):
        self.url = args.u
        self.deep = args.d
        self.table = table
        self.key = args.key




if __name__ == '__main__':
    args = parse_args()
    print args.u
    logger = my_log("5", "test.log")
    logger.debug("test debug")
    # db = db_deal("test1.db", "test_table")
    # db.create_db()
    # db.insert_data(("10-14","http://www.baidu.com"))
