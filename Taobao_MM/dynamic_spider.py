from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from urllib import request
from urllib.error import HTTPError
from tool.tool import Tool
import re, os, threading

BASE_URL = 'http://mm.taobao.com/json/request_top_list.htm'
PATH = './MM/'

class Spider:

    def __init__(self, start_page, end_page):
        self.base_url = BASE_URL
        self.start_page = start_page
        self.end_page = end_page
        self.client = webdriver.PhantomJS()
        self.tool = Tool()
        self.path = PATH
        
    def get_index_page(self, page):
        url = self.base_url + '?page=' + str(page)
        req = request.Request(url)
        resp = request.urlopen(req)
        return resp.read().decode('gbk')
        
    def get_index_content(self, page):
        page_html = self.get_index_page(page)
        pattern = re.compile('<a.*?class="lady-avatar">.*?<img src="(.*?)".*?<a class="lady-name" href="(.*?)" target="_blank">(.*?)</a>.*?<em><strong>(.*?)</strong>.*?<span>(.*?)</span>.*?<em>(.*?)</em>', re.S)
        items = re.findall(pattern, page_html)
        contents = []
        for item in items:
            mm_page_url = 'https:' + item[1]
            avatar_url = 'https:' + item[0]
            contents.append([avatar_url, mm_page_url, item[2], item[3], item[4], item[5]])
        return contents
        
    def get_infos_url(self, url):
        self.client.get(url)
        try:
            element = self.client.find_element_by_class_name('mm-p-domain-info').find_element_by_tag_name('li')
            text = element.text
            return re.sub('域名地址', 'https', text)
        except NoSuchElementException as e:
            return None
            
    def get_infos_page(self, url):
        resp = request.urlopen(url)
        page_html = resp.read().decode('gbk')
        return page_html
        
    def get_infos_describe(self, page_html):
        pattern = re.compile('<div class="mm-aixiu-content" id="J_ScaleImg">(.*?)<input', re.S)
        item = re.search(pattern, page_html)
        if not item:
            return None
        # remove duplicate urls
        desc = self.tool.replace(item.group(1))
        return desc
        
    def get_imgs_url(self, page_html):
        pattern = re.compile('<img style=".*? src="(.*?)"')
        items = re.findall(pattern, page_html)
        urls = items[0:(len(items)//2)]
        return urls
        
    def makedir(self, name):
        dir_path = self.path + name + '/'
        exists = os.path.exists(dir_path)
        if not exists:
            print('create directory: %s' % dir_path)
            os.makedirs(dir_path)
        return dir_path
        
    def get_extension(self, img_url):
        return img_url.split('.')[-1]
    
    def save_img(self, img_url, file_path):
        resp = request.urlopen(img_url)
        img = resp.read()
        with open(file_path, 'wb') as f:
            f.write(img)
        print('save img under: %s' % file_path)
        
    def save_info(self, content, file_path):
        info = 'name: %s\nage: %s\ncity: %s\ncareer: %s\n' % (content[2], content[3], content[4], content[5])
        with open(file_path, 'w') as f:
            f.write(info)
        print('save infos of %s at: %s' % (content[2], file_path))
        
    def save_describe(self, desc, file_path):
        with open(file_path, 'w') as f:
            f.write(desc)
        print('save discribe at: %s' % file_path)
        
    def run(self):
        for i in range(self.start_page, self.end_page+1):
            contents = self.get_index_content(i)
            for content in contents:
                dir_path = self.makedir(content[2])
                avatar_url = content[0]
                avatar_path = dir_path + content[2] + '.' + self.get_extension(content[0])
                self.save_img(avatar_url, avatar_path)
                info_path = dir_path + content[2] + 'infos.txt'
                self.save_info(content, info_path)
                url = self.get_infos_url(content[1])
                if not url:
                    print('domain not found')
                    continue
                print('domain: ' + url)
                page_html = self.get_infos_page(url)
                desc = self.get_infos_describe(page_html)
                if desc:
                    desc_path = dir_path + content[2] + 'description.txt'
                    self.save_describe(desc, desc_path)
                else:
                    print('No Description')
                img_urls = self.get_imgs_url(page_html)
                if img_urls:
                    imgs_path = dir_path+'imgs/'
                    if not os.path.exists(imgs_path):
                        os.makedirs(imgs_path)
                    count = 1
                    for img_url in img_urls:
                        img_path = imgs_path + str(count) + '.' + self.get_extension(img_url)
                        img_url = 'https:' + img_url
                        try:
                            self.save_img(img_url, img_path)
                            count += 1
                        except HTTPError as e:
                            print(e.code)
                            print(e.msg)
        
spider1 = Spider(1, 1)
spider2 = Spider(2, 2)
t1 = threading.Thread(target=spider1.run)
t2 = threading.Thread(target=spider2.run)
t1.start()
t2.start()
t1.join()
t2.join()
print('Completed')