# -*- coding:utf-8 -*-
from urllib import request
import os
import re

BASE_URL = 'http://mm.taobao.com/json/request_top_list.htm'
START_PAGE = 6
END_PAGE = 10
PATH = './MM/'

class TBMMSpider:
    def __init__(self):
        self.base_url = BASE_URL
        self.start_page = START_PAGE
        self.end_page = END_PAGE
        self.path = PATH
    
    def get_page(self, page):
        url = self.base_url + '?page=' + str(page)
        req = request.Request(url)
        resp = request.urlopen(req)
        return resp.read().decode('gbk')
        
    def get_contents(self, page):
        page_code = self.get_page(page)
        pattern = re.compile('<a.*?class="lady-avatar">.*?<img src="(.*?)".*?<a class="lady-name".*?>(.*?)</a>.*?<em><strong>(.*?)</strong>.*?<span>(.*?)</span>.*?<em>(.*?)</em>', re.S)
        items = re.findall(pattern, page_code)
        contents = []
        for item in items:
            contents.append([item[0], item[1], item[2], item[3], item[4]])
        return contents
    
    def makedir(self, name):
        dir_path = self.path + name + '/'
        exists = os.path.exists(dir_path)
        if not exists:
            print('create directory: %s' % dir_path)
            os.makedirs(dir_path)
        return dir_path
        
    def get_extension(self, img_url):
        return img_url.split('.')[-1]
    
    def save_avatar(self, avatar_url, file_path):
        resp = request.urlopen(avatar_url)
        img = resp.read()
        with open(file_path, 'wb') as f:
            f.write(img)
        print('save avatar under: %s' % file_path)
        
    def save_info(self, content, file_path):
        info = 'name: %s\nage: %s\ncity: %s\ncareer: %s\n' % (content[1], content[2], content[3], content[4])
        with open(file_path, 'w') as f:
            f.write(info)
        print('save infos of %s at: %s' % (content[1], file_path))
        
    def run(self):
        print('Spider start runing')
        for p in range(self.start_page, self.end_page+1):
            print('fetch page%s' % p)
            contents = self.get_contents(p)
            for content in contents:
                dir_path = self.makedir(content[1])
                if dir_path:
                    avatar_url = 'https:' + content[0]
                    avatar_path = dir_path + content[1] + '.' + self.get_extension(avatar_url)
                    self.save_avatar(avatar_url, avatar_path)
                    info_path = dir_path + content[1] + '.txt'
                    self.save_info(content, info_path)
        print('completed')
        
spider = TBMMSpider()
spider.run()
        
        