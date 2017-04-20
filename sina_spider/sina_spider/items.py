# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SinaSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 大类的标题和URL
    parent_title = scrapy.Field()
    parent_url = scrapy.Field()

    # 子类的标题和URL
    child_title = scrapy.Field()
    child_url = scrapy.Field()

    # 子类的存储路径
    child_path = scrapy.Field()

    # 子类下面文章的URL
    son_url = scrapy.Field()

    # 每个文章的标题和内容
    article_title = scrapy.Field()
    article_content = scrapy.Field()

