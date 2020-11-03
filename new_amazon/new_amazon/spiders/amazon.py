import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class AmazonSpider(CrawlSpider):
    name = 'amazon'
    allowed_domains = ['www.amazon.cn']
    start_urls = ['https://www.amazon.cn/gp/site-directory/ref=nav_deepshopall_variant_fullstore_l1']

    rules = (
        Rule(LinkExtractor(allow='\/[^%s]*\_\=\w{20,40}'), callback='parse_item'),
    )

    def parse_item(self, response):
        item= response.xpath(".//a[contains(@class,'s-access-detail-page')]/@title").extract()
        print(item)
