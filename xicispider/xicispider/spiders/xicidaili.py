# -*- coding: utf-8 -*-
import scrapy
import time

class XicidailiSpider(scrapy.Spider):
    name = 'xicidaili'
    # allowed_domains = ['xicidaili.com']
    start_urls = ['https://www.xicidaili.com/nn']

    def parse(self, response):
        selectors = response.xpath('//tr')
        # 提取ip地址及对应的端口
        for selector in selectors:
            ip = selector.xpath('./td[2]/text()').get()
            port = selector.xpath('./td[3]/text()').get()
            if ip and port:
                items = {
                    'ip': ip,
                    'port': port
                }
                with open('./Proxy.txt', 'a') as p:
                    p.write(items['ip'] + ":" + items['port'] + '\n')
        #获取翻页地址并翻页
        next_page = response.xpath("//a[@class='next_page']/@href").get()
        if int(next_page.split('/')[-1]) <= 5:
            next_url = response.urljoin(next_page)
            time.sleep(5)
            yield scrapy.Request(next_url, callback=self.parse)
