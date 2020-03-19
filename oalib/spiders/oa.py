# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from oalib.items import OalibItem
import re


class OaSpider(CrawlSpider):
    name = 'oa'
    allowed_domains = ['www.oalib.com']
    start_urls = ['http://www.oalib.com/journal/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//div[@class='paperlist']//h3/a") ,callback="parse_item",follow=True),
        Rule(LinkExtractor(restrict_xpaths="//span[@id='pagespace_down']/a[last()-1]"))
    )

    """
    来源：source：//div[@class='contents']/div[1]/div[1]/a/text()
    时间：datetime ：//div[@class='contents']/div[1]/div/text()
    标题：title: //div[@class='contents']/h1/text()
    DOI:DOI : //p[@class='doi'][1]/a/u
    作者：authors: //div[@class='contents']/div[@id='author']/a/text()
    查看量：views：//span[@id='views']/text()
    下载量：downloads： //span[@id='downloads']/text()
    下载链接：Full_Text : //p[@class='resetHref']/a[1]/@href 

    摘要：Abstract：//div[@class='contents']/span[*]/div/p/text()

    """


    def parse_item(self,response:HtmlResponse):
        item = OalibItem()
        item['periodical_id'] = int(response.xpath("//p[@class='resetHref']/a[1]/@href").re_first('(\d+)'))
        item['source'] = response.xpath("//div[@class='contents']/div[1]/div[1]/a/text()").extract_first()
        item['datetime'] = ''.join(response.xpath("//div[@class='contents']/div[1]/div/text()").extract()).strip()
        item['title'] = response.xpath("//div[@class='contents']/h1/text()").extract_first()
        item['doi'] = response.xpath("//p[@class='doi'][1]/a/u/text()").extract_first()
        item['authors'] = ''.join(response.xpath("//div[@class='contents']/div[@id='author']/a/text()").extract())
        item["abstract"] = ''.join(response.xpath("//div[@class='contents']/span[*]/div/p/text()").extract()).strip()
        if not item["abstract"]:
            item["abstract"] = ''.join(response.xpath("//div[@class='contents']/span[1]/div/div/text()").extract()).strip()
        item['views'] = response.xpath("//div[@class='shadowTable']//span[@id='views']/text()").extract_first()
        item['downloads'] = response.xpath("//div[@class='shadowTable']/table[2]/tbody/tr[@class='even']/td[2]//text()").extract_first()
        item['full_link'] = response.xpath("//p[@class='resetHref']/a[1]/@href").extract_first()
        yield item
