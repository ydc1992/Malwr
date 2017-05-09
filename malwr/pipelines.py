# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.http import Request
from scrapy.pipelines.files import FilesPipeline


class MalwrPipeline(FilesPipeline):
    cookies = []
    def __init__(self, store_uri, download_func=None, settings=None):
        super(MalwrPipeline,self).__init__(store_uri, download_func,settings)
        self.cookies = settings.getlist("COOKIES")

    # 开始下载文件
    def get_media_requests(self, item, info):
        for file_url in item['file_urls']:
            yield Request(file_url,cookies=self.cookies)

    def media_downloaded(self, response, request, info):
        super(MalwrPipeline, self).media_downloaded(response, request, info)