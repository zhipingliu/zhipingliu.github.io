# -*- coding: utf-8 -*-
import re
import urllib2
import thread
import time

class QSBK:
    
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent' : self.user_agent}
        self.stories = []
        self.enable = False
    def getPage(self,pageIndex):
        try:
            url = 'http://www.qiushibaike.com/8hr/page/' + str(pageIndex)
            request = urllib2.Request(url,headers=self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode('utf-8')
            return pageCode

        except urllib2.URLError,e:
            if hasattr(e,'reason'):
                print u'cannot be linked to qsbk',e.reason
                return None
    def getPageItems(self,pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print 'page cannot be loaded'
            return None
        pattern = re.compile('<div.*?class="author.*?>.*?<a.*?</a>.*?<a.*?>.*?2>(.*?)<.*?2>.*?</a>'+
                         '.*?<div.*?class="content">(.*?)<!--.*?</div>'+
                         '(.*?)'+
                         '<div class="stats">.*?<.*?"stats-vote".*?class="number">(.*?)</i>'+
                         '.*?<.*?"stats-comments".*?class="number">(.*?)</i>',re.S)
        items = re.findall(pattern,pageCode)
        pageStories = []
        for item in items:
            haveImg = re.search('img',item[2])
            if not haveImg:
                pageStories.append([item[0].strip(),item[1].strip(),item[3].strip(),item[4].strip()])
        return pageStories

    def loadPage(self):
        if self.enable == True:
            if len(self.stories) < 2:
                pageStories = self.getPageItems(self.pageIndex)
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex += 1
                    
    def getOneStory(self,pageStories,page):
        for story in pageStories:
            input = raw_input()
            self.loadPage()
            if input == 'q':
                self.enable = False
                return
            print u'第%d页\t发布人：%s\n发布内容：%s\n获赞数：%s\t 评论数：%s\n'%(page,story[0],story[1],story[2],story[3])
            
    def start(self):
        print u'正在读取糗事百科，按回车查看新段子，q为退出'
        self.enable = True
        self.loadPage()
        nowPage = 0
        while self.enable:
            if len(self.stories)>0:
                pageStories = self.stories[0]
                nowPage += 1
                del self.stories[0]
                self.getOneStory(pageStories,nowPage)   

spider = QSBK()
spider.start()

