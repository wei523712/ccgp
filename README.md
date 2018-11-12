# ccgp
政府采购网失信行为信息爬取
## 前言
本文主要以http://www.ccgp.gov.cn/cr/list为例，介绍Scrapy-splash的简单使用。&ensp;本文中若存在不详细的地方欢迎各位大神网友提问，若有错误的地方，希望大家指正。谢谢！! :") :-") 
## 粗略分析
1.进入该网站可以看到主要内容是以一个表格的呈现的，每页有一百条信息，且页数为六页。
2.对于表格中的内容猜想可以通过xpath提取，而翻页则通过提取底部的页码实现。
## ![在这里插入图片描述](https://img-blog.csdnimg.cn/20181112224400385.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3h1ZTYwNTgyNjE1Mw==,size_16,color_FFFFFF,t_70)
## 程序分析
1. items
```
    company = scrapy.Field()
    social_code = scrapy.Field()
    address = scrapy.Field()
    detail = scrapy.Field()
    result = scrapy.Field()
    punishment_basis = scrapy.Field()
    punish_date = scrapy.Field()
    publication_date = scrapy.Field()
    enforcement = scrapy.Field()
```
2.spiders
##### 码前分析
点击页码时发现浏览器上的链接并不发生改变，此时打开F12，点击NETWORK。再点点击页码查看此时新加载的网页。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20181112225556511.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3h1ZTYwNTgyNjE1Mw==,size_16,color_FFFFFF,t_70)
此时可以构造出每页的链接为http://www.ccgp.gov.cn/cr/list?gp=页码。因此翻页对于我们来说不再是大问题。
##### 代码
```
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
```
刚接触splash时还常常的想，使用splash还要再单独学习一下lua脚本语言吗，我的观点是暂时不用，基本的渲染已经暂时够用了。
3. settings
此处只列出使用splash时的一些设置 ，其它设置略去。
```
SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware':100,
}
DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware':723,
    'scrapy_splash.SplashMiddleware':725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware':810,
}
SPLASH_URL = 'http://192.168.99.100:8050'   #此处别忘了写上“http://”
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'
```
4.其它
其它设置项此处不再给出。
此处只是简介写了splash的应用。下次会单独介绍一下splash。
## 再次声明
若有错误及改进之处，望大家批评指正。
