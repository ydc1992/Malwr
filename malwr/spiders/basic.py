# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from malwr.items import MalwrItem
from scrapy.selector import Selector

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

import urlparse,re

def get_cookie():
        loginurl = 'https://malwr.com/account/login/'
        driver = webdriver.Ie()
        driver.get(loginurl)

        WebDriverWait(driver,3).until(lambda x:x.find_element_by_link_text('Logout'))
        cookies = driver.get_cookies()
        driver.close()
        return cookies

class BasicSpider(CrawlSpider):
    name = "basic"
    allowed_domains = ["malwr.com"]
    strat_urls = ['https://malwr.com/analysis/?page=1']

    custom_settings = {"COOKIES":get_cookie(),
                      'ITEM_PIPELINES':{'malwr.pipelines.MalwrPipeline':1},
                       "FILES_STORE":"E:\\Virus\\Malwr"}

    def start_requests(self):
        url = self.strat_urls[0]
        # cookiejar  cookie传递
        yield  Request(url,cookies=self.custom_settings['COOKIES'],callback=self.parse_item,meta = {'cookiejar' : 1})

    def parse_item(self,response):
        url = response.xpath("//td/a/@href").extract()
        for u in url:
            url = urlparse.urljoin("https://malwr.com",u.encode("utf-8"))
            yield Request(url,self.parse_downurl,meta={'cookiejar': response.meta['cookiejar']})
        # 下一页
        nextpage = response.xpath("//a[contains(text(),'Next')]/@href").extract()[0].encode('utf-8')
        url = urlparse.urljoin("https://malwr.com",nextpage)
        yield Request(url,self.parse_item, meta={'cookiejar': response.meta['cookiejar']})

    # 解析下载地址
    def parse_downurl(self,response):
        try:
            antivirus1 =response.css("#static_antivirus").extract()[0]
            antivirus = Selector(response).css("#static_antivirus").extract()[0]
            # 从Static Analysis ------ Antivirus的结果页
            antiresult  = re.findall("((Microsoft|Kaspersky|ESET\-NOD32)</td>\n\s*<td>\n\s*<span class=\"text\-error\")",antivirus.encode("utf-8"),re.S)
            # 如果返回的列表为空，则表示这个样本eset、卡巴斯基和微软不报，不入库，直接返回。
            if antiresult == []:
                return
            # 提取点击下载按钮的下载地址
            url = response.xpath("//a[contains(@class,'btn-primary')]/@href").extract()[0].encode('utf-8')
            url = urlparse.urljoin("https://malwr.com",url)

            item = MalwrItem()
            item['file_urls'] = [url]
            return item
        except Exception,e:
            pass
        return