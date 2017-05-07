# -*- coding:utf-8 -*-
from urllib import request as urllib2
import re
import threading
import time

class QSBK:
    def __init__(self):
        self.page_index = 1
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent': self.user_agent}
        self.stories = []
        self.enable = False
        
    def get_html(self, page_index):
        try:
            url = 'http://www.qiushibaike.com/8hr/page/' + str(page_index)
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            html = response.read().decode('utf-8')
            return html
        except urllib2.URLError as e:
            print('connect failed ')
            if hasattr(e, 'code'):
                print(e.code)
            elif hasattr(e, 'reason'):
                print(e.reason)
            return None
    
    def get_page_content(self, page_index):
        html = self.get_html(page_index)
        if not html:
            print('page load failed ')
            return None
        pattern = re.compile(r'<div.*?author clearfix">.*?<h2>(.*?)</h2>.*?<div class="content">.*?<span>(.*?)</span>(.*?)<span class="stats-vote"><i class="number">(.*?)</i>.*?<i class="number">(.*?)</i>', re.S)
        items = re.findall(pattern, html)
        page_stories = []
        for item in items:
            hasimg = bool(re.search('img', item[2]))
            if not hasimg:
                tab = re.compile('<br/>')
                text = re.sub(tab, '\n', item[1])
                page_stories.append([item[0].strip(), text.strip(), item[3].strip(), item[4].strip()])
        return page_stories
    
    def load_page(self):
        if self.enable:
            if len(self.stories) < 2:
                page_stories = self.get_page_content(self.page_index)
                if page_stories:
                    self.stories.append(page_stories)
                    self.page_index += 1
    
    def get_one_story(self, page_stories, page):
        for story in page_stories:
            page_input = input()
            self.load_page()
            if page_input == 'Q':
                self.enable = False
                return
            try:
                print(u'Page: %d\nAuthor: %s\nStory: %s\nLike: %s\nComments: %s' % (page, story[0], story[1], story[2], story[3]))
            except:
                print('Error: ')
                #print(story)
                
    def start(self):
        print('QSBK Q: Exit')
        self.enable = True
        self.load_page()
        page_now = 0
        while self.enable:
            if len(self.stories) > 0:
                page_stories = self.stories[0]
                page_now += 1
                del self.stories[0]
                self.get_one_story(page_stories, page_now)
                
spider = QSBK()
spider.start()
                
        
