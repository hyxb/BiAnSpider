# -*- coding: utf-8 -*-
from selenium import webdriver
from urllib import parse
from scrapy.http import Request
from ..items import NetBianSpiderItem
import re
import scrapy
import time

driverFile = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'

class NetbianSpider(scrapy.Spider):
    name = 'netbian'
    allowed_domains = ['http://pic.netbian.com/']
    start_urls = ['http://pic.netbian.com']
    # 小图的RE规则
    img_small_match = '/uploads/.*?.jpg'
    # img页面url的RE规则
    img_url_match = '/.*?.html'
    def parse(self, response):
        '''
        根据起始url，获取下一个分页url
        :param response:
        :return:
        '''
        #获取下一页的url
        next_url = parse.urljoin(self.start_urls[0],
                                 response.xpath('//div[@class="page"]/a[contains(text(),"下一页")]/@href').extract()[0])
        print(response.url)
        print(next_url)
        yield Request(response.url,
                      meta={'next_url':next_url},
                      callback=self.page_parse,
                      dont_filter=True)
        #
        # if next_url:
        #     pass

    def page_parse(self,response):
        '''
        根据当前分页，获取图片详情页的url
        :param response:
        :return:
        '''
        # 获取图片详情页的html元素信息列表
        img_list = response.xpath('//ul[@class="clearfix"]/li/a/@href').extract()
        next_url = response.meta['next_url']
        print('next_url:'+next_url)
        for url in img_list:
            img_html_url = parse.urljoin(self.start_urls[0],url)
            print(img_html_url)
            yield Request(img_html_url,callback=self.img_url_parse,dont_filter=True)

        yield Request(next_url,callback=self.parse,dont_filter=True)
        #
        # for element in img_list:
        #     img_html_url = re.findall(self.img_url_match, element)[0]
        #     next_url = parse.urljoin(self.start_urls[0], img_html_url)
        #     yield Request(next_url, callback=self.img_url_parse, meta={}, dont_filter=True)

    def img_url_parse(self,response):
        '''
        进入图片详情页，爬取大图url
        获取标题
        :param response:
        :return:
        '''
        # 实例化item对象
        item = NetBianSpiderItem()
        print('img_url_parse is running')
        img_big_url = response.xpath('//div[@class="photo-pic"]/a/img/@src').extract()[0]
        title = response.xpath('//div[@class="photo-pic"]/a/img/@alt').extract()[0].strip()
        title_list = title.split()
        #定义图片标题
        img_title = ''
        img_title = img_title.join(title_list) + '.jpg'
        #拼接img_url
        img_url = parse.urljoin(self.start_urls[0],img_big_url)
        item['img_url'] = [img_url]
        item['img_title'] = [img_title]
        item['img_html_url'] = [response.url]

        yield item
        # yield Request(img_url,callback=self.img_download,dont_filter=True)

    # def img_download(self,response):
    #
    #     # print(response.url)
    #     # item['img_url'] = response.url
    #     item['img_url'] = [response.url]
    #
    #     yield item
    #
