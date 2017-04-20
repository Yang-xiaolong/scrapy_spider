# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class SinaSpiderPipeline(object):
    def process_item(self, item, spider):
        file_name = item['child_path'] + '/' + item['article_title'] + '.txt'
        with open(file_name, 'w') as f:
            f.write(item['article_content'])
        return item
