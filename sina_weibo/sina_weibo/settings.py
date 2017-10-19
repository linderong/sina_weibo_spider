# -*- coding: utf-8 -*-


import os


BOT_NAME = 'sina_weibo'

SPIDER_MODULES = ['sina_weibo.spiders']
NEWSPIDER_MODULE = 'sina_weibo.spiders'

DOWNLOAD_DELAY = 2

PROJECT_DIR = os.path.dirname(__file__)

# DOWNLOAD_FILES_DIR = os.path.join(PROJECT_DIR, 'Download/')
# if not os.path.exists(DOWNLOAD_FILES_DIR):
#     os.mkdir(DOWNLOAD_FILES_DIR)

IMAGES_STORE = os.path.join(PROJECT_DIR, 'Images/')
if not os.path.exists(IMAGES_STORE):
    os.mkdir(IMAGES_STORE)

COOKIES_ENABLED = False

DEFAULT_REQUEST_HEADERS = {
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': '_T_WM=39b37994a8d15b390ab5f4c2bfeb076f; ALF=1510196241; SCF=AkBPJqClbQu2LQzg1CpMR7Z4YDOIJTWrJnnsWpFopalbECFaPgU6kOP1474sJxyu-a1GHbJ3KalMktpYKd8zl0k.; SUB=_2A2502EdPDeThGeNG4lQT9inOwz2IHXVUI2kHrDV6PUJbktBeLUzjkW1QfMg_-wERJUH5scmTOG0bjge5jg..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFp6x9EWLv9JPOBgJUPB9uU5JpX5K-hUgL.Fo-R1KqESoME1h22dJLoI7YLxKqL1--L1KU2MJpaUJ-t; SUHB=0y0JuIJ286Q5_F; SSOLoginState=1507604255',
    'Referer': 'http://www.weibo.com/5896267281/profile?filter=1&page=1&is_all=1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
}

DOWNLOADER_MIDDLEWARES = {
    'sina_weibo.middlewares.CookiesMiddleware': 543,
    'sina_weibo.middlewares.UserAgentMiddleware': 300,
    'sina_weibo.middlewares.ProxyMiddleware': 200,
}

ITEM_PIPELINES = {
    'sina_weibo.pipelines.ImageItemPipeline': 500,
    'sina_weibo.pipelines.PeopleItemPipeline': 400,
    'sina_weibo.pipelines.FansItemPipeline': 300,
    'sina_weibo.pipelines.TweetItemPipeline': 200,
}

# MONGODB 主机环回地址127.0.0.1
MONGODB_HOST = '127.0.0.1'
# 端口号，默认是27017
MONGODB_PORT = 27017
# 设置数据库名称
MONGODB_DBNAME = 'weibo_db'
# 存放本次数据的表名称
MONGODB_DOCNAME = dict(
    people = 'people_collection',
    fans = 'fans_collection',
    tweet = 'tweet_collection',
)
