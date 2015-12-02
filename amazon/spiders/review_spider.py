# -*- coding: utf-8 -*-
from scrapy import Spider, Selector
from scrapy.http import Request
from amazon.items import ReviewItem
import urllib2
 
class ReviewSpider(Spider):
    name = "review"
    allowed_domains = ["amazon.com"]
 
    start_urls = []
    u1 = 'http://www.amazon.com/s/ref=sr_pg_'
    u2 = '?rh=n%3A7141123011%2Cn%3A7147441011%2Cn%3A1040658%2Cn%3A2476517011%2Cn%3A1045624%2Cp_6%3AATVPDKIKX0DER&page='
    u3 = '&bbn=2476517011&ie=UTF8&qid=1448965490'
    for i in range(119):
        url = u1 + str(i+1) + u2 + str(i+1) + u3
        start_urls.append(url)
 
    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//li[@class="s-result-item  celwidget "]')
        for site in sites:
            item = ReviewItem()
            item['item'] = site.xpath('@data-asin').extract()[0]
            item_url = site.xpath('div/div[2]/div[1]/a/@href').extract()[0]
            yield Request(url=item_url, meta={'item': item}, callback=self.parse_item_page)

    def parse_item_page(self, response):
        sel = Selector(response)
        item = response.meta['item']

        review_urls = sel.xpath('//a[@class="a-link-emphasis a-text-bold"]/@href').extract()
        if review_urls:
            this_review_url = review_urls[0]

            while True:
                yield Request(url=this_review_url, meta={'item': item}, callback=self.parse_review_content_page)
                response = urllib2.urlopen(this_review_url)
                this_review_url_sel = Selector(text=response.read())
                next_review_urls = this_review_url_sel.xpath('//li[@class="a-last"]/a/@href').extract()
                if next_review_urls:
                    this_review_url = next_review_urls[0]
                else:
                    break
        else:
            yield Request(url=response.url, meta={'item': item}, callback=self.return_invalid_review)

    def return_invalid_review(self, response):
        return ReviewItem()


    def parse_review_page(self, response):
        sel = Selector(response)
        item = response.meta['item']

        #this page
        self.logger.error('this review page url :' + response.url)
        yield Request(url=response.url, meta={'item': item}, callback=self.parse_review_content_page)
        #next page
        #next_review_urls = sel.xpath('//li[@class="a-last"]/a/@href').extract()
        #if next_review_urls:
            #self.logger.error('next review page url :'.join(next_review_urls))
            #yield Request(url=next_review_urls[0], meta={'item': item}, callback=self.parse_review_content_page)

    def parse_review_content_page(self, response):
        sel = Selector(response)
        item_id = response.meta['item']['item']
        items = []

        reviews = sel.xpath('//div[@class="a-section review"]')
        for review in reviews:
            item = ReviewItem()
            item['item'] = item_id
            item['rate'] = review.xpath('div[2]/a[1]/i/span/text()').extract()[0][0]

            user_url = review.xpath('div[3]/span[1]/a/@href').extract()[0]
            #/gp/pdp/profile/AVH8RKFH1JMNF/ref=cm_cr_pr_pdp?ie=UTF8
            strs = user_url.split('/')
            item['user'] = strs[4]

            item['time'] = review.xpath('div[3]/span[last()]/text()').extract()[0][3:]

            item['text'] = ''.join(review.xpath('div[5]/span/text()').extract())
            items.append(item)

        return items
