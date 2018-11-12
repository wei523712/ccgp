# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from ccgp.items import ShixItem

class ShixinSpider(scrapy.Spider):
    name = 'shixin'
    # allowed_domains = ['ccgp.gov.cn']
    start_urls = ['http://www.ccgp.gov.cn/cr/list?gp=1']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url,callback=self.parse,args={'wait':3},endpoint='render.html')

    def parse(self, response):
        item = ShixItem()
        bigtag = response.xpath('//table[@class="layout2 jiajigonggao"]/tbody/tr[position()>1]')
        for tag in bigtag:
            company = tag.xpath('./td[2]/a/font/text()').extract_first()
            social_code = tag.xpath('./td[3]/text()').extract_first()
            address = tag.xpath('./td[4]/text()').extract_first()
            detail = tag.xpath('./td[5]/p/@title').extract_first()
            result = tag.xpath('./td[6]/p/@title').extract_first()
            punishment_basis = tag.xpath('./td[7]/p/@title').extract_first()
            punish_date = tag.xpath('./td[8]/text()').extract_first()
            publication_date = tag.xpath('./td[9]/text()').extract_first()
            enforcement = tag.xpath('./td[10]/text()').extract_first()

            item['company'] = company if company else '暂无信息'
            item['social_code'] = social_code if social_code else '暂无信息'
            item['address'] = address if address else '暂无信息'
            item['detail'] = detail if detail else '暂无信息'
            item['result'] = result if result else '暂无信息'
            item['punishment_basis'] = punishment_basis if punishment_basis else '暂无信息'
            item['punish_date'] = punish_date if punish_date else '暂无信息'
            item['publication_date'] = publication_date if publication_date else '暂无信息'
            item['enforcement'] = enforcement if enforcement else '暂无信息'
            yield item

        for num in range(2,7):
            tourl = 'http://www.ccgp.gov.cn/cr/list?gp=' + str(num)
            yield SplashRequest(tourl,callback=self.parse,args={'wait':3},endpoint='render.html')
