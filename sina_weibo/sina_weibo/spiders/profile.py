#! /usr/bin/env python3
# coding:utf-8
import re
import sys
import time

from scrapy.spiders import CrawlSpider
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from sina_weibo.items import PeopleItem, FansItem, TweetItem

from sina_weibo.savedata import DataRedis

reload(sys)
sys.setdefaultencoding('utf-8')


class SinaWeiboSpider(CrawlSpider):
    name = 'weibo'
    start_ids = [
        2456764664L, 3637354755L, 1940087047, 5508473104L,
        1004454162, 2930327837L, 1874608417, 5379621155L,
        1720664360, 2714280233L, 3769073964L, 5624119596L,
        2754904375L, 5710151998L, 5331042630L, 5748179271L,
        2146132305,
    ]

    def __init__(self, *args, **kwargs):
        super(SinaWeiboSpider, self).__init__(*args, **kwargs)
        self.db = DataRedis()

        done_id = self.db.smembers('done')
        for ID in self.start_ids:
            if ID not in done_id:
                self.db.sadd('do_id', ID)

        '''
        下面是对应存储信息的正则匹配对象
        '''
        self.tweet_count_pattern = re.compile(r'微博\[(\d*?)\]')
        self.follow_count_pattern = re.compile(r'关注\[(\d*?)\]')
        self.fans_count_pattern = re.compile(r'粉丝\[(\d*?)\]')

        self.ID_pattern = re.compile(r'cn/(.+?)/info')
        self.fans_id_pattern = re.compile(r'cn/u/(.+)/?')
        self.nickname_pattern = re.compile(ur'昵称:(.*?)}')
        self.gender_pattern = re.compile(ur'性别:(.*?)}')
        self.signature_pattern = re.compile(ur'简介:(.*?)}')
        self.area_pattern = re.compile(ur'地区:(.*?)}')

        self.tweet_id_pattern = re.compile(ur'id="M_(.*?)"')
        self.transpond_pattern = re.compile(r'转发\[(\d*?)\]')
        self.comment_pattern = re.compile(r'评论\[(\d*?)\]')
        self.praise_pattern = re.compile(r'赞\[(\d*?)\]')

    def start_requests(self):
        while self.db.scard('do_id'):
            ID = str(self.db.spop('do_id'))
            self.db.sadd('done', ID)

            profile_url = 'https://weibo.cn/{}/profile'.format(ID)
            fans_url = 'https://weibo.cn/{}/fans'.format(ID)

            yield Request(
                profile_url,
                meta={'ID': ID},
                callback=self.parse_profile,
            )

            yield Request(
                fans_url,
                meta={'ID': ID},
                callback=self.parse_fans,
            )


    def parse_profile(self, response):
        '''
        解析主页的微博数, 关注数, 粉丝数
        '''
        selector = Selector(response)
        ID = response.meta.get('ID')
        content = response.body
        tweet_id_list = self.tweet_id_pattern.findall(content)

        for tweet_id in tweet_id_list:
            tweet_item = TweetItem()
            tweet_item['ID'] = ID
            tweet_item['tweet_id'] = tweet_id
            tweet_url = 'https://weibo.cn/comment/{}'.format(tweet_id)
            yield Request(
                tweet_url,
                meta={'tweet_item': tweet_item},
                callback=self.parse_tweet,
            )

        next_page_url = selector.xpath('//div[@id="pagelist"]//a/@href').extract()
        world = selector.xpath('//div[@id="pagelist"]//a/text()').extract()
        if next_page_url and world[0] == [u'\u4e0b\u9875']:
            next_url = 'https://weibo.cn{}'.format(next_page_url[0])
            yield Request(
                next_url,
                callback=self.parse_tweet_id,
            )
        else:
            people_item = PeopleItem()
            people_item['ID'] = ID

            tweet_count = self.tweet_count_pattern.findall(content)
            follow_count = self.follow_count_pattern.findall(content)
            fans_count = self.fans_count_pattern.findall(content)

            image_url = selector.xpath('//img[@class="por"]/@src').extract()

            people_item['tweet_count']  = tweet_count[0] if tweet_count else '0'
            people_item['follow_count']  = follow_count[0] if follow_count else '0'
            people_item['fans_count']  = fans_count[0] if fans_count else '0'
            people_item['profile_url'] = response.url
            people_item['image_url'] = image_url[0] if image_url else 'Null'

            info_url = 'https://weibo.cn/{}/info'.format(ID)
            yield Request(
                info_url,
                meta={'people_item': people_item},
                callback=self.parse_info,
            )

    def parse_info(self, response):
        '''
        解析个人信息
        '''
        selector = Selector(response)
        people_item = response.meta.get('people_item')

        content = '}'.join(selector.xpath('//div[@class="c"]/text()').extract())
        gender = self.gender_pattern.findall(content)
        nickname = self.nickname_pattern.findall(content)
        signature = self.signature_pattern.findall(content)

        people_item['gender'] = gender[0] if gender else 'Null'
        people_item['nickname'] = nickname[0] if nickname else 'Null'
        people_item['signature'] = signature[0] if signature else 'Null'

        area = self.area_pattern.findall(content)
        area = area[0].split() if area else []
        people_item['area0'] = area[0] if area else 'Null'
        people_item['area1'] = area[1] if area.__len__() > 1 else 'Null'

        yield people_item

    def parse_fans(self, response):
        '''
        获取粉丝id
        '''
        fans_item = response.meta.get('fans_item')
        if fans_item is None:
            fans_item = FansItem()
            fans_item['ID'] = response.meta.get('ID', 'Null')

        selector = Selector(response)
        url_list = selector.xpath('//tr/td[2]/a[1]/@href').extract()

        fans_set = set(fans_item.get('fans', set()))
        for url in url_list:
            ID = self.fans_id_pattern.findall(url)
            if ID:
                fans_set.add(ID[0])
                if ID[0] not in self.db.smembers('done_id'):
                    self.db.sadd('do_id', ID[0])

        next_page_url = selector.xpath('//div[@id="pagelist"]//a/@href').extract()
        world = selector.xpath('//div[@id="pagelist"]//a/text()').extract()
        fans_item['fans'] = list(fans_set)

        if next_page_url and world[0] == [u'\u4e0b\u9875']:
            fans_next_url = 'https://weibo.cn{}'.format(next_page_url[0])
            yield Request(
                fans_next_url,
                meta={'fans_item': fans_item},
                callback=self.parse_fans,
            )
        else:
            follow_url = 'https://weibo.cn/{}/follow'.format(fans_item['ID'])
            yield Request(
                follow_url,
                meta={'fans_item': fans_item},
                callback=self.parse_follow
            )

    def parse_follow(self, response):
        '''
        获取关注id
        '''
        fans_item = response.meta.get('fans_item')
        selector = Selector(response)
        url_list = selector.xpath('//tr/td[2]/a[1]/@href').extract()

        follow_set = set()
        for url in url_list:
            ID = self.fans_id_pattern.findall(url)
            if ID:
                follow_set.add(ID[0])
                if ID[0] not in self.db.smembers('done_id'):
                    self.db.sadd('do_id', ID[0])

        next_page_url = selector.xpath('//div[@id="pagelist"]//a/@href').extract()
        world = selector.xpath('//div[@id="pagelist"]//a/text()').extract()
        fans_item['follow'] = list(follow_set)

        if next_page_url and world[0] == [u'\u4e0b\u9875']:
            follow_next_url = 'https://weibo.cn{}'.format(next_page_url[0])
            yield Request(
                follow_next_url,
                meta={'fans_item': fans_item},
                callback=self.parse_fans,
            )
        else:
            yield fans_item

    def parse_tweet_id(self, response):
        '''
        获取微博id
        '''
        selector = Selector(response)
        ID = response.meta.get('ID')
        html = response.body
        tweet_id_list = self.tweet_id_pattern.findall(html)

        for tweet_id in tweet_id_list:
            tweet_item = TweetItem()
            tweet_item['ID'] = ID
            tweet_item['tweet_id'] = tweet_id
            tweet_url = 'https://weibo.cn/comment/{}'.format(tweet_id)
            yield Request(
                tweet_url,
                meta={'tweet_item': tweet_item},
                callback=self.parse_tweet,
            )

        next_page_url = selector.xpath('//div[@id="pagelist"]//a/@href').extract()
        world = selector.xpath('//div[@id="pagelist"]//a/text()').extract()
        if next_page_url and world[0] == [u'\u4e0b\u9875']:
            next_url = 'https://weibo.cn{}'.format(next_page_url[0])
            yield Request(
                next_url,
                callback=self.parse_tweet_id,
            )

    def parse_tweet(self, response):
        '''
        获取微博信息
        '''
        selector = Selector(response)
        tweet_item = response.meta.get('tweet_item')
        content = selector.xpath('//div[@id="M_"]/div[1]/span[@class="ctt"]/text()').extract()
        tweet_item['content'] = ''.join(content) if content else 'Null'

        release_time = selector.xpath('//span[@class="ct"]/text()').extract()
        tweet_item['release_time'] = ''.join(release_time[0] if release_time else [])
        tweet_item['spider_time'] = time.ctime()

        html = response.body
        transpond = self.transpond_pattern.findall(html)
        tweet_item['transpond_count'] = transpond[0] if transpond else '0'

        comment = self.comment_pattern.findall(html)
        tweet_item['comment_count'] = comment[0] if comment else '0'

        praise = self.praise_pattern.findall(html)
        tweet_item['praise_count'] = praise[0] if praise else '0'

        yield tweet_item




















