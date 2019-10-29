# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BianimgspiderItem(scrapy.Item):

    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class NetBianSpiderItem(scrapy.Item):

    img_url = scrapy.Field()
    img_title = scrapy.Field()
    img_html_url = scrapy.Field()
