import scrapy, requests
from lxml import etree
from ..items import DoubanItem


class DoubanSpiderSpider(scrapy.Spider):
    name = "douban_spider"
    # allowed_domains = ["movie.douban.com"]
    # start_urls = ["https://movie.douban.com"]
    def start_requests(self):
        url = 'https://movie.douban.com/chart'
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
        }
        res = requests.get(url=url, headers=headers)
        html = etree.HTML(res.text)
        url_list = html.xpath('//a[@class="nbg"]/@href')
        urllist = []
        for url in url_list:
            urllist.append(scrapy.Request(url=url))
        return urllist

    def parse(self, response):
        item = DoubanItem()
        item['url'] = response.url
        item['urlname'] = response.xpath('//span[@property="v:itemreviewed"]/text()').getall()[0]
        item['average'] = response.xpath('//strong[@property="v:average"]/text()').getall()[0]
        item['initialReleaseDate'] = "/".join(response.xpath('//span[@property="v:initialReleaseDate"]/text()').getall())
        item['starring'] = "/".join(response.xpath('//a[@rel="v:starring"]/text()').getall())
        item['genre'] = "/".join(response.xpath('//span[@property="v:genre"]//text()').getall())
        item['summary'] = response.xpath('//span[@property="v:summary"]/text()').getall()[0].strip()
        yield item
