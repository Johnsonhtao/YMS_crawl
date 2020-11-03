import scrapy
from .items import AmazonItem
from copy import deepcopy
l = []
d=0

# with open('amazon/url.txt', 'r') as f:
#     l = [x.strip() for x in f if x.strip() != '']
class AmoazonNewSpider(scrapy.Spider):
    name = 'Amoazon_new'
    allowed_domains = ['www.amazon.cn']

        # for line in f:
        #     l.append(line)
    # start_urls = [l[d]]

    start_urls = ['https://www.amazon.cn/s?rh=n%3A1885879071&page=2']

    def parse(self, response):

        detail_li = response.xpath("//div[@class='a-section a-spacing-medium']")

        for li in detail_li:
            item = {}
            # 判断能否拿到 标签名 “鞋类
            if response.xpath(
                    "//div[@class='a-section a-spacing-small a-spacing-top-small']/a/span/text()") is not None:
                # 拿到 细分的标签  ”女鞋
                item["b_cate"] = response.xpath(
                    "//div[@class='a-section a-spacing-small a-spacing-top-small']/span[@class='a-color-state a-text-bold']/text()").extract()
            else:
                item["b_cate"] = response.xpath(
                    "//div[@class='a-section a-spacing-small a-spacing-top-small']/a/span[@class='a-color-base a-text-bold']/text()").extract()

            # 一页中商品 名字 第一个div
            item["name"] = li.xpath(
                ".//div[@class='a-section a-spacing-none a-spacing-top-small'][1]/h2/a/span[@class='a-size-base-plus a-color-base a-text-normal']/text()").extract()

            # 一页中的 价格  第二个div
            item["price"] = li.xpath(
                ".//div[@class='a-section a-spacing-none a-spacing-top-small'][2]/span[@class='a-price']/span[@class='a-offscreen']/text()").extract()

            print(item)

        global d
        d=d+1
        yield scrapy.Request(
            l[d],
            callback=self.parse,
            meta={"item": item}
            )
