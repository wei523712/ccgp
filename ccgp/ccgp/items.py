# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy



class ShixItem(scrapy.Item):
    # number = scrapy.Field()
    company = scrapy.Field()
    social_code = scrapy.Field()
    address = scrapy.Field()
    detail = scrapy.Field()
    result = scrapy.Field()
    punishment_basis = scrapy.Field()
    punish_date = scrapy.Field()
    publication_date = scrapy.Field()
    enforcement = scrapy.Field()

