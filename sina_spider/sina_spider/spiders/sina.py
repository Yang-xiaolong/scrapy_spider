# -*- coding: utf-8 -*-
import scrapy
import os
from sina_spider.items import SinaSpiderItem


class SinaSpider(scrapy.Spider):
    name = "sina"
    allowed_domains = ["sina.com.cn"]
    start_urls = ['http://news.sina.com.cn/guide/']

    # 处理每一个大类下的内容
    def parse(self, response):
        items = []
        # 提取父类的标题和url
        parent_title_list = response.xpath('//div[@id="tab01"]/div/h3/a/text()').extract()
        parent_url_list = response.xpath('//div[@id="tab01"]/div/h3/a/@href').extract()

        # 提取子类的标题和url
        child_title_list = response.xpath('//div[@id="tab01"]/div/ul/li/a/text()').extract()
        child_url_list = response.xpath('//div[@id="tab01"]/div/ul/li/a/@href').extract()

        # 遍历父类的标题列表
        for parent_index, parent_item in enumerate(parent_title_list):
            parent_title = parent_item
            parent_url = parent_url_list[parent_index]
            parent_path = './data/' + parent_title

            self.exists_dir(parent_path)

            # 遍历小类的标题列表
            for child_index, child_item in enumerate(child_title_list):
                item = SinaSpiderItem()
                child_title = child_item
                child_url = child_url_list[child_index]
                item['parent_title'] = parent_title
                item['parent_url'] = parent_url

                # 判断小类和url开头和大类的url开头是否一样，一样的话在该大类下面创建小类的文件夹
                if child_url.startswith(parent_url):
                    child_path = parent_path + '/' + child_title

                    self.exists_dir(child_path)

                    item['child_title'] = child_title
                    item['child_url'] = child_url
                    item['child_path'] = child_path

                    items.append(item)

        for value in items:
            yield scrapy.Request(url=value['child_url'], meta={'data': value}, callback=self.child_parse)

    # 处理每一个子类下的内容
    def child_parse(self, response):
        items = []
        data = response.meta['data']

        son_url_list = response.xpath('//a/@href').extract()

        for son_index, son_item in enumerate(son_url_list):
            if son_item.startswith(data['child_url']) and son_item.endswith('.shtml'):
                item = SinaSpiderItem()
                item['parent_title'] = data['parent_title']
                item['parent_url'] = data['parent_url']
                item['child_title'] = data['child_title']
                item['child_url'] = data['child_url']
                item['child_path'] = data['child_path']
                item['son_url'] = son_item

                items.append(item)

        for value in items:
            yield scrapy.Request(url=value['son_url'], meta={'data': value}, callback=self.deal_parse)

    # 处理每一个文章
    def deal_parse(self, response):
        item = response.meta['data']
        if len(response.xpath('//h1[@id="artibodyTitle"]/text()').extract()):
             article_title = response.xpath('//h1[@id="artibodyTitle"]/text()').extract()[0]
        elif len(response.xpath('//h2[@id="artibodyTitle"]/text()').extract()):
            article_title = response.xpath('//h2[@id="artibodyTitle"]/text()').extract()[0]
        else:
            article_title = 'Null'
        if len(response.xpath('//div[@class="article article_16"]/p/text()').extract()):
            article_content = "\n".join(response.xpath('//div[@class="article article_16"]/p/text()').extract())
        elif len(response.xpath('//div[@class="BSHARE_POP blkContainerSblkCon clearfix blkContainerSblkCon_14"]/p/text()').extract()):
            article_content = "\n".join(response.xpath('//div[@class="BSHARE_POP blkContainerSblkCon clearfix blkContainerSblkCon_14"]/p/text()').extract())
        elif len(response.xpath('//div[@id="artibody"]/p/text()').extract()):
            article_content = '\n'.join(response.xpath('//div[@id="artibody"]/p/text()').extract())
        else:
            article_content = 'Null'
        item['article_title'] = article_title
        item['article_content'] = article_content
        return item

    # 判断目录是否存在
    def exists_dir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
