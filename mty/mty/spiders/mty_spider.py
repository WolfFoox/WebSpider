import json

import scrapy
from ..items import MtyItem


class MtySpiderSpider(scrapy.Spider):
    name = "mty_spider"
    # allowed_domains = ["api.tripadvisor.cn"]
    # start_urls = ["https://api.tripadvisor.cn"]
    def start_requests(self):
        url = 'https://api.tripadvisor.cn/restapi/soa2/21221/globalSearch'
        headers = {
            'content-type': 'application/json;charset:utf-8;'
        }
        data = {"keywords": "云南", "pageNo": 1, "pageSize": 30, "lat": "", "lon": ""}
        return [scrapy.Request(url=url, headers=headers,method='POST', body=json.dumps(data))]

    def parse(self, response):
        url_namelist = [i.get('name') for i in response.json().get('result').get('hits')]
        total_list = [i.get('totalComments') for i in response.json().get('result').get('hits')]
        locationIdlist = [i.get('taId') for i in response.json().get('result').get('hits')]
        # 数据传递：实例化数据结构类，再给这个对象进行字典键值对的发送
        item = MtyItem()
        item['url_namelist'] = url_namelist
        item['total_list'] = total_list
        item['locationIdlist'] = locationIdlist
        yield item
