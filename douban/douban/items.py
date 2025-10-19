# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    urlname = scrapy.Field()
    average = scrapy.Field()
    initialReleaseDate = scrapy.Field()
    starring = scrapy.Field()
    genre = scrapy.Field()
    summary = scrapy.Field()

