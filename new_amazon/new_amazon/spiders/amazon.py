import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import requests
from bs4 import BeautifulSoup


class AmazonSpider(CrawlSpider):
    name = 'amazon'
    allowed_domains = ['www.amazon.cn']
    start_urls = ['https://www.amazon.cn/gp/site-directory?ie=UTF8&ref_=nav_shopall_btn']

    rules = (
        Rule(LinkExtractor(allow=r'(\/b\)?(([^%83 ]*))'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        #收集去掉乱码的url
        urls = []
        res = requests.get(self.start_urls[0])
        text = res.text
        soup = BeautifulSoup(text, "html.parser")
        a_herf = soup.find_all('a')
        for h in a_herf:
            if "href" in h.attrs:
                if len(h.attrs['href']) < 512:
                    if (not h.attrs['href'].startswith('http://')) and (not h.attrs['href'].startswith('https://')):
                        urls.append(h.attrs['href'])

        item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        return item
