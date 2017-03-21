# python web spider
> 看到了知道创宇的一个道spider题，准备动手写一下。

# 要求

``` 
spider.py -u url -d deep -f logfile -l loglevel(1-5)  --testself --thread number --dbfile  filepath  --key=”HTML5”

# 其中 -u 是url
#      -d 是爬取的深度
#      -f 是日志文件
#      -l 是日志等级
#      -- testself 程序自测
#      -- thread 线程数  要求是用线程池
#      --dbfile  数据库文件
#      --key  关键字

```

# 具体要求

   1.  指定网站爬取指定深度的页面，将包含指定关键词的页面内容存放到sqlite3数据库文件中
   2. 10秒在屏幕上打印进度信息
   3. 并发爬取网页
   4. 自己需要深刻理解该程序所涉及到的各类知识点
   5. 需要自己实现线程池

