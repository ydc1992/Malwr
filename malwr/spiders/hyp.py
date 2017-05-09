# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider
from scrapy.http import Request

class HypSpider(CrawlSpider):
    name = "hyp"
    allowed_domains = ["hybrid-analysis.com"]
    start_urls = ['https://www.hybrid-analysis.com/recent-submissions?filter=file']


    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'

    custom_settings={"DEFAULT_REQUEST_HEADERS":
                         {
                          "User-Agent": USER_AGENT,
                          "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                          "Accept-Encoding":"gzip, deflate, br",
                          "Accept-Language":"zh-CN,en-US;q=0.7,en;q=0.3",
                          "Upgrade-Insecure-Requests":"1",
                          "Host":"www.hybrid-analysis.com",
                          "Connection":"keep-alive",
                          "Referer":"https://www.hybrid-analysis.com/",
                          "DNT":"1",
                          "Cookie":"PHPSESSID=71806d77c71449e88289ad21ca353b56"
                         }}

    def start_requests(self):
        yield Request(self.start_urls[0],callback=self.parse_item)
        pass

    def parse_start_url(self, response):
        pass

    def parse_item(self,response):
        pass