# -*- coding: utf-8 -*-
import random
import base64

from user_agents import agents


class ProxyMiddleware(object):
    '''
    设置代理, 有条件可以设置代理池,同理user-agent一随机
    '''
    def process_request(self, request, spider):
        proxy = '116.62.128.50:16816'
        request.meta['proxy'] = 'http://' + proxy
        proxy_user_password = 'mr_mao_hacker:sffqry9r'

        base64_user_passwd = base64.b64encode(proxy_user_password)
        request.headers['Proxy-Authorization'] = 'Basic ' + base64_user_passwd


class UserAgentMiddleware(object):
    '''
    设置随机user-angent
    '''

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', random.choice(agents))


class CookiesMiddleware(object):
    '''
    设置cookie, 有条件可以设置一个cookie池进行随机, 我这边没有太多账户就不设置了
    '''
    def process_request(self, request, spider):
        # cookies = []
        # request.cookies = {'Cookie': random.choice(cookies)}
        pass





