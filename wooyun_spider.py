# -*- coding: utf-8 -*-

import threading
import requests
import sys
from lxml import etree
import re
import os

requests.adapters.DEFAULT_RETRIES = 5

reload(sys)
sys.setdefaultencoding('utf-8')

url_root = "http://www.wooyun.org"
path_root = 'D:\wooyun'
url_corps = "http://www.wooyun.org/corps/page/"


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
}


class MyThread(threading.Thread):
    def __init__(self, func, args):
        threading.Thread.__init__(self)
        self.args = args
        self.func = func

    def run(self):
        apply(self.func, self.args)


def download_detail(url, title, path, status):
    # 漏洞详情
    if status == u'已确认':
        return
    path = path + '\%s' % title
    if os.path.exists(path):
        return
    print "保存" + path
    os.makedirs(path)
    s_dd = requests.session()
    detail = s_dd.get(url, headers=headers).text
    match = re.compile('<hr align="center"/>(.*?)<hr align="center"/>', re.S)
    detail = re.findall(match, detail)[0]
    select_dd = etree.HTML(detail)
    l_img = select_dd.xpath('//img/@src')
    for i in range(len(l_img)):
        url_img = l_img[i]
        if url_img[0] == '/':
            url_img = url_root + url_img
        detail = detail.replace(l_img[i], "./%s.jpg" % i)
        # print detail
        req_img = s_dd.get(url_img, headers=headers)
        img = open("%s/%s.jpg" % (path, i), "wb")
        img.write(req_img.content)
        img.close()
    html = open('%s/%s.html' % (path, title), 'a+')
    html.write('<meta charset="utf-8">')
    html.write(detail)
    html.close()

def holes(url, name, path):
    # 厂商漏洞
    print url
    path = path + '\%s' % name
    print "保存" + path
    if not os.path.exists(path):
        os.makedirs(path)
    req_holes = s.get(url + '/page/1', headers=headers).text
    match_page_holes = re.compile(u', (.*?) 页')
    page = int(re.findall(match_page_holes, req_holes)[0])
    for i in range(page):
        req = requests.get(url + '/page/' + str(i+1), headers=headers)
        print "爬取第%s页，共%s页" % ((i+1), page)
        # print req.text
        select = etree.HTML(req.text)
        list_link = select.xpath('//body/div[5]/table[2]/tbody/tr/td/a/@href')      #漏洞链接
        list_name = select.xpath('//body/div[5]/table[2]/tbody/tr/td/a/text()')     #漏洞名称
        list_status = select.xpath('//body/div[5]/table[2]/tbody/tr/th[2]/a/text()')
        # print len(list_link), list_link
        # print len(list_name), list_name
        # print len(list_status), list_status
        for names in range(len(list_name)):
            # 文件夹命名错误规避（/\*?<>:|）
            list_name[names] = list_name[names].replace('/', 'or').replace('\\', 'or').replace('*', '').replace('?', '').replace(':', '').replace('<', '').replace('>', '').replace('|', '').replace('"', '').strip()
            # ../ 规避
            if list_name[names][-1] == '.':
                list_name[names] = list_name[names].replace('.', '。')
            # print list_name[names]
        # 多线程爬！！
        try:
            threadList = [MyThread(download_detail, (url_root+list_link[j], list_name[j], path, list_status[j])) for j in range(len(list_link))]
            for t in threadList:
                t.setDaemon(True)
                t.start()
            for k in threadList:
                k.join()
        except:
            erro = open('D:\wooyun\erro.txt', 'a+')
            erro.write('%s%s\n' % (name, i+1))
            erro.close()

        # 单线程
        # for j in range(len(list_link)):
        #     download_detail(url_root+list_link[j], list_name[j].replace('/', 'or'), path)

s = requests.session()
req_corps = s.get(url_corps + '1', headers=headers).text
match_page_corps = re.compile(u', (.*?) 页')
page = int(re.findall(match_page_corps, req_corps)[0])
# print page
for i in range(16, page):
    req_corps = s.get(url_corps + str(i+1), headers=headers).text
    select_corps = etree.HTML(req_corps)
    corps_link = select_corps.xpath('//div[@class="content"]/table/tbody/tr/td[2]/a/@href')     #厂商链接
    corps_name = select_corps.xpath('//div[@class="content"]/table/tbody/tr/td[2]/a/text()')    #厂商名称
    # print requests.get(url_root+corps_link[0], headers=headers).text
    # break
    # print corps_link
    # print corps_name
    for j in range(len(corps_link)):
        holes(url_root+corps_link[j], corps_name[j].strip(), path_root)




