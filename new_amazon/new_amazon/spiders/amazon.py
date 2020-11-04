import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class AmazonSpider(CrawlSpider):
    name = 'amazon'
    allowed_domains = ['www.amazon.cn']
    start_urls = ['https://www.amazon.cn/gp/site-directory/ref=nav_deepshopall_variant_fullstore_l1']

    # 定义提取url地址规则# LinkExtractor链接提取器，获取符合要求的url链接地址
    # callback 提取出来的url地址的response会交给callback处理
    # follow 当前url地址的相应是否重新经过Rules来提取url地址
    rules = (
        Rule(LinkExtractor(deny=(r'/b\?ie=UTF8&node=\d+&ref_=\w{20,40}')), callback='parse_item'),
    )


    def parse_item(self, response):
        # 详情第一页的的名字
        item = response.xpath(".//a[contains(@class,'s-access-detail-page')]/@title").extract()
        print(item)
