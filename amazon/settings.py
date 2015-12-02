# -*- coding: utf-8 -*-
 
# Scrapy settings for amazon project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
 
BOT_NAME = 'amazon'
 
SPIDER_MODULES = ['amazon.spiders']
NEWSPIDER_MODULE = 'amazon.spiders'
 
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'amazon (+http://www.yourdomain.com)'
 
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.54 Safari/536.5'
 
FEED_URI = 'review.jl'
FEED_FORMAT = 'json'

LOG_FILE = 'review.log'
LOG_STDOUT = True

ITEM_PIPELINES = {
    'amazon.pipelines.EmptyItemPipeline': 300,
    #'amazon.pipelines.JsonWriterPipeline': 1000
}
