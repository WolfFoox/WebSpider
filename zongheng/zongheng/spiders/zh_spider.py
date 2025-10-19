# import scrapy, requests
# from ..items import ZonghengItem
#
#
# class ZhSpiderSpider(scrapy.Spider):
#     name = "zh_spider"
#     # allowed_domains = ["www.zongheng.com"]
#     # start_urls = ["https://www.zongheng.com"]
#     def start_requests(self):
#         url = 'https://bookapi.zongheng.com/api/chapter/getChapterList'
#         headers = {
#             'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
#             'content-type': 'application/x-www-form-urlencoded'
#         }
#         data = 'bookId=1296249'
#         res = requests.post(url=url, headers=headers, data=data)
#         urlcount = res.json().get('result').get('chapterSum')
#         urllist = [f'https://read.zongheng.com/chapter/1296249/{i.get("chapterId")}.html' for i in
#                    res.json().get('result').get('chapterList')[0].get('chapterViewList')]
#         n = int(input(f'请输入需要爬取的章节数（总共有{urlcount}章）:'))
#         url = []
#         for i in range(0, n):
#             url.append(scrapy.Request(url=urllist[i]))
#         return url
#
#     def parse(self, response):
#         item = ZonghengItem()
#         item['chapter_name'] = response.xpath('//div[@class="title_txtbox"]//text()').getall()[0]
#         item['chapter_count'] = response.xpath('//span[contains(text(), "本章字数：")]/i/text()').getall()[0]
#         item['chapter_content'] = "".join(response.xpath('//div[@class="content"]//text()').getall()[1:-2])
#         yield item


# 分段爬取
import scrapy, requests
from ..items import ZonghengItem


class ZhSpiderSpider(scrapy.Spider):
    name = "zh_spider"
    # allowed_domains = ["www.zongheng.com"]
    # start_urls = ["https://www.zongheng.com"]
    def start_requests(self):
        url = 'https://bookapi.zongheng.com/api/chapter/getChapterList'
        headers = {
            'content-type': 'application/x-www-form-urlencoded'
        }
        data = {'bookId':'1296249'}  # 注意：formdata参数是按照表单的形式去接收数据的，必须是键值对的格式

        return [scrapy.FormRequest(url=url, headers=headers, method='POST', formdata=data)]

    def parse(self, response):
        urlcount = response.json().get('result').get('chapterSum')
        urllist = [f'https://read.zongheng.com/chapter/1296249/{i.get("chapterId")}.html' for i in
                   response.json().get('result').get('chapterList')[0].get('chapterViewList')]
        n = int(input(f'请输入需要爬取的章节数（总共有{urlcount}章）:'))
        for i in range(0, n):
            yield scrapy.Request(url=urllist[i], callback=self.next_parse)

    def next_parse(self, response):
        item = ZonghengItem()
        item['chapter_name'] = response.xpath('//div[@class="title_txtbox"]//text()').getall()[0]
        item['chapter_count'] = response.xpath('//span[contains(text(), "本章字数：")]/i/text()').getall()[0]
        item['chapter_content'] = "".join(response.xpath('//div[@class="content"]//text()').getall()[1:-2])
        yield item


