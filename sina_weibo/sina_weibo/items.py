# -*- coding: utf-8 -*-


import scrapy


class PeopleItem(scrapy.Item):
    '''
    个人信息
    '''
    ID = scrapy.Field() # id
    nickname = scrapy.Field() # 昵称
    gender = scrapy.Field() # 性别
    signature = scrapy.Field() # 简介
    area0 = scrapy.Field() # 省
    area1 = scrapy.Field() # 市

    profile_url = scrapy.Field() # 主页url
    follow_count = scrapy.Field() # 关注数量
    fans_count = scrapy.Field() # 粉丝数量
    tweet_count = scrapy.Field() # 微博数量
    image_url = scrapy.Field() # 头像ｕｒｌ

class FansItem(scrapy.Item):
    '''
    个人粉丝和关注人
    '''
    ID = scrapy.Field() # 用户ID
    fans = scrapy.Field() # 用户粉丝
    follow = scrapy.Field() # 用户关注

class TweetItem(scrapy.Item):
    '''
    个人微博
    '''
    ID = scrapy.Field() # 用户ID
    tweet_id = scrapy.Field() # 微博id
    content = scrapy.Field() # 微博内容
    transpond_count = scrapy.Field() # 转发量
    comment_count = scrapy.Field() # 评论数量
    praise_count = scrapy.Field() # 点赞数量
    # image_url = scrapy.Field() # 图片链接
    release_time = scrapy.Field() # 写微博时间
    spider_time = scrapy.Field() # 爬取微博时刻




