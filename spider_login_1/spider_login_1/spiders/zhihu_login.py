# -*- coding: utf-8 -*-
import scrapy


class ZhihuLoginSpider(scrapy.Spider):
    name = "renren_login"
    allowed_domains = ["renren.com"]
    start_urls = ['http://www.renren.com/PLogin.do']

    def start_requests(self):
        return [scrapy.FormRequest(
            url=self.start_urls[0],
            formdata={'email': '18535013098', 'password': '1234567890'},
            callback=self.parse_page
        )]

    def parse_page(self, response):
        print('*'*30)
        with open('renren.html', 'w') as f:
            f.write(response.body)
        yield scrapy.Request(url='http://matter.renren.com/', callback=self.parse_)

    def parse_(self, response):
        print('_' * 30)
        with open('renren_.html', 'w') as f:
            f.write(response.body)
