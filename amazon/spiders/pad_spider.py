# -*- coding: utf-8 -*-
from scrapy import Spider, Selector
from scrapy.http import Request
from amazon.items import PadItem
 
 
class PadSpider(Spider):
    name = "pad"
    allowed_domains = ["amazon.com"]
 
    start_urls = []
    u1 = 'http://www.amazon.com/s/ref=sr_pg_'
    u2 = '?rh=n%3A7141123011%2Cn%3A7147441011%2Cn%3A1040658%2Cn%3A2476517011%2Cn%3A1045642%2Cp_6%3AATVPDKIKX0DER&page='#?rh=n%3A7141123011%2Cn%3A7147441011%2Cn%3A1040658%2Cn%3A2476517011%2Cn%3A1045624%2Cp_6%3AATVPDKIKX0DER&page='
    u3 = '&bbn=2476517011&ie=UTF8&qid=1448984126'#&bbn=2476517011&ie=UTF8&qid=1448965490'
    for i in range(119):
        url = u1 + str(i+1) + u2 + str(i+1) + u3
        start_urls.append(url)
 
    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//li[@class="s-result-item  celwidget "]')
        #items = []
        for site in sites:
            item = PadItem()
            item['sno'] = site.xpath('@data-asin').extract()[0]
            print item['sno']
            try:
                item['price'] = site.xpath('//span[@class="a-size-base a-color-price s-price a-text-bold"]/text()').extract()[0][1:]
            # 索引异常，说明是新品
            except IndexError:
                item['price'] = site.xpath('ul/li/a/span/text()').extract()[0]
            #items.append(item)
        #return items
