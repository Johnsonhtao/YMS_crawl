import scrapy
import os
from copy import deepcopy
import time
import re
import requests
from bs4 import BeautifulSoup
from .items import AmazonItem
item = AmazonItem()

class AmazonSpider(scrapy.Spider):
    name = 'Amazon'
    allowed_domains = ['amazon.cn']
    start_urls = ['https://www.amazon.cn/gp/site-directory/ref=nav_deepshopall_variant_fullstore_l1']
    global Dedup_url
    Dedup_url =[]

    def parse(self, response):
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

        li_list = response.xpath("//div[contains(@class,'a-spacing-top-medium')]")
            # item['a_cate'] = li.xpath(".//span[contains(@class,'sd-fontSizeL1')]/a/text()").extract()   #大分类的名
            # item['b_cate'] = li.xpath(".//span[contains(@class,'sd-fontSizeL2')]/a/text()").extract()   #中分类的名
            # item['c_href'] = li.xpath(".//span[contains(@class,'sd-fontSizeL2')]/a/@href").re()  #中分类的地址

        for url in urls:
            yield scrapy.Request(
                url='https://www.amazon.cn' + str(url),
                callback=self.parse_commodity_list,
                #meta={'item': item}
            )

    def parse_commodity_list(self, response):               #第一页
        #item = response.meta.get('item')
        li_list = response.xpath("//div[@id='mainResults'or'atfResults']/ul/li")
        url_store = []

        next_url = []
        htm=[]
        # item = {}
        for li in li_list:

                # 访问完第一页 打印
            if response.xpath("//span[@id='s-result-count']/span/a[@class='a-link-normal a-color-base a-text-bold a-text-normal']/text()") is not None:
                item["b_cate"] = response.xpath("//span[@id='s-result-count']/span/a[@class='a-link-normal a-color-base a-text-bold a-text-normal']/text()").extract()
            else:
                item["b_cate"] = response.xpath("//div[@class='a-section a-spacing-small a-spacing-top-small']/a/span[@class='a-color-base a-text-bold']/text()").extract()
            item["name"] = li.xpath(".//a[contains(@class,'s-access-detail-page')]/@title").extract()
            item["goods_url"] = li.xpath(".//a[contains(@class,'s-access-detail-page')]/@href").extract()
            item["freight"] = li.xpath(".//span[contains(@class,'a-size-small')]/text()").extract()
            item["price"] = li.xpath(".//span[contains(@class,'s-price')]/text()").extract()
            if item["name"] != []:
                # print(item)
                yield(item)
            # next_url = 'https://www.amazon.cn' + str(response.xpath("//a[@id='pagnNextLink']/@href").extract_first())
            #
            # with open('amazon/url.txt', 'a') as f:
            #     f.write(next_url + '\n')
            # if item["name"] != []:
                # print(item)
            str_fix = str(response.xpath("//a[@id='pagnNextLink']/@href").extract_first())
            if (str_fix != 'None'):
                next_url = 'https://www.amazon.cn' + str_fix
                url_store.append(next_url)  # 含有重复项的url
            # 去重之后的url
        if len(url_store) != 0:
            for i in url_store:
                if i not in Dedup_url:
                    Dedup_url.append(i)

        for url in Dedup_url:
            # print(os.path.abspath(__file__))
            print(url + '\n')
            with open('../amazon/url.txt', 'a') as f:
                f.write(url + '\n')
