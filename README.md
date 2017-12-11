# sina_weibo
新浪 微博爬虫
这是一个爬取新浪用户信息，粉丝，关注，微博内容和评论，用户头像的爬虫

运行环境在python2.7下

使用scrapy + reids + MongoDB 主要是改写了start_request 加入redis中的set数据结构来作为指纹的去重并且记录， 不会因为暂停而要重新爬取

使用前记得去savedata.py模块里面改改 自己需要保持的数据库名称就可以了

技术交流可以加微信/qq：897603022
