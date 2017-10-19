# -*- coding: utf-8 -*-
import json
import os
import sys

import scrapy
from scrapy.pipelines.images import ImagesPipeline

from items import PeopleItem, FansItem, TweetItem
from settings import IMAGES_STORE

from savedata import MongoDatabase

reload(sys)
sys.setdefaultencoding('utf-8')


class PeopleItemPipeline(object):
    '''
    people信息存储
    '''
    def __init__(self):
        self.post = MongoDatabase('people').get_collection()

    def process_item(self, item, spider):
        if isinstance(item, PeopleItem):
            # 存入mongodb数据库
            self.post.insert(dict(item))

        return item


class TweetItemPipeline(object):
    '''
    tweet信息存储
    '''
    def __init__(self):
        self.post = MongoDatabase('tweet').get_collection()

    def process_item(self, item, spider):
        if isinstance(item, TweetItem):
            # 存入mongodb数据库
            self.post.insert(dict(item))

        return item


class FansItemPipeline(object):
    '''
    fans信息存储
    '''
    def __init__(self):
        self.post = MongoDatabase('fans').get_collection()

    def process_item(self, item, spider):
        if isinstance(item, FansItem):
            # 存入mongodb数据库
            self.post.insert(dict(item))

            # with open(DOWNLOAD_FILES_DIR + 'fans.json', 'a') as f:
            #     f.write(json.dumps(dict(item), ensure_ascii=False))
            #     f.write('\n')

        return item


class ImageItemPipeline(ImagesPipeline):
    '''
    图片存储
    '''
    def get_media_requests(self, item, info):
        url = item.get('image_url', 'Null')
        if url != 'Null':
            yield scrapy.Request(url)

    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok, x in results if ok]

        if image_path:
            os.rename(
                IMAGES_STORE + image_path[0],
                IMAGES_STORE + item.get('ID', 'test001') + '.jpg'
            )

        return item





