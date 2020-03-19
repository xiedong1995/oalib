# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field,Item


class OalibItem(Item):
    collection = table = 'oalib'
    periodical_id = Field()
    source = Field()
    datetime = Field()
    title = Field()
    doi = Field()
    authors = Field()
    abstract = Field()
    views = Field()
    downloads = Field()
    full_link = Field()




