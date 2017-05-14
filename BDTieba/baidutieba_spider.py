# -*- coding:utf-8 -*-
from urllib import request
import re
from tool.tool import Tool 

class BDTieba:
    def __init__(self, base_url, see_lz, floor_tag):
        self.base_url = base_url
        self.see_lz = '?see_lz=' + str(see_lz)
        self.floor_tag = floor_tag
        self.floor = 1
        self.file_title = 'baidutieba.txt'
        self.tool = Tool()
        
    def get_page(self, page_num):
        try:
            url = self.base_url + self.see_lz + '&pn=' + str(page_num)
            req = request.Request(url)
            resp = request.urlopen(req)
            return resp.read().decode('utf-8')
        except request.URLError as e:
            print('Connect failed:')
            if hasattr(e, 'code'):
                print(e.code)
            elif hasattr(e, 'reason'):
                print(e.reason)
            return None
    
    def get_page_title(self):
        page = self.get_page(1)
        if not page:
            print('Get Title Failed')
            return None
        pattern = re.compile('<title>(.*?)_.*?</title>', re.S)
        title = re.search(pattern, page)
        print(title.group(1))
        if title:
            return title.group(1)
        return None
        
    def get_page_count(self):
        page = self.get_page(1)
        if not page:
            print('Get Page Count Failed')
            return None
        pattern = re.compile('</span>回复贴，共<span class="red">(.*?)</span>', re.S)
        count = re.search(pattern, page)
        if count:
            return count.group(1)
        return None
    
    def get_page_content(self, page):
        page = self.get_page(page)
        if not page:
            print('Get Content Failed')
            return None
        pattern = re.compile('<div.*?class="d_post_content j_d_post_content ">(.*?)</div>', re.S)
        items = re.findall(pattern, page)
        return items
        #for item in items:
        #    print(item)
            
    def write_content(self, page):
        contents = self.get_page_content(page)
        with open(self.file_title, 'a') as f:
            for content in contents:
                post = '\n' + self.tool.replace(content) + '\n'
                if self.floor_tag:
                    f.write('\n------------------------------------------------------------------------\n')
                f.write('page: %s\nfloor: %d' % (page, self.floor))
                f.write(post)
                self.floor += 1
    
    def start(self):
        title = self.get_page_title()
        count = self.get_page_count()
        if title:
            self.file_title = title + '.txt'
        if not count:
            print('Invalid URL')
            return
        with open(self.file_title, 'w') as f:
            f.write('Title: %s\nCount: %s\n' % (self.file_title, count))
        try:
            print('Writing File')
            for i in range(1, int(count)+1):
                self.write_content(i)
        except IOError as e:
            print('Exception by writing')
        finally:
            print('Completed')

base_url = 'https://tieba.baidu.com/p/3138733512'    
spider = BDTieba(base_url, 1, 1)
spider.start() 
