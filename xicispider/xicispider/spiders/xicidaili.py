# -*- coding: utf-8 -*-
import scrapy
from xicispider.items import XicispiderItem


class XicidailiSpider(scrapy.Spider):
    name = 'xicidaili'
    # allowed_domains = ['xicidaili.com']
    start_urls = ['https://www.xicidaili.com/nn']
    def parse(self, response):
        item = XicispiderItem()
        selectors = response.xpath('//tr')
        # 提取ip地址及对应的端口
        for selector in selectors:
            ip = selector.xpath('./td[2]/text()').get()
            port = selector.xpath('./td[3]/text()').get()
            if ip and port:
                item['ip'] = ip
                item['port'] = port
                yield item

        #获取翻页地址并翻页
        next_page = response.xpath("//a[@class='next_page']/@href").get()
        # if int(next_page.split('/')[-1]) <= 5:
        #     next_url = response.urljoin(next_page)
        #     time.sleep(5)
        #     yield scrapy.Request(next_url, callback=self.parse)
        next_url = response.urljoin(next_page)
        yield scrapy.Request(next_url, callback=self.parse)