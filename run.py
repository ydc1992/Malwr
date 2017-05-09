from  scrapy.crawler import CrawlerProcess

from scrapy.settings import Settings


from malwr.spiders.basic import BasicSpider
from malwr.spiders.hyp import HypSpider


settings = Settings()

settings.set("DEFAULT_REQUEST_HEADERS",
              {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0"
               })

process = CrawlerProcess(settings)


# process.crawl(HypSpider)
process.crawl(BasicSpider)


process.start()