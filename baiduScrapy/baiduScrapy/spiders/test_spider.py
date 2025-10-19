import scrapy


class TestSpiderSpider(scrapy.Spider):
    name = "test_spider"
    # allowed_domains = ["www.baidu.com"]   # 设置只能爬取的域名
    # 单个url提供：
    # start_urls = ["https://www.baidu.com"]
    # 多个url提供：
    # start_urls = [f'https://tieba.baidu.com/f?kw=%E5%B0%8F%E8%AF%B4&ie=utf-8&pn={(i-1)*50}' for i in range(1,6)]
    def start_requests(self):
        # 单个url提供：
        requests_data = [scrapy.Request(url=f'https://www.baidu.com')]   # 这里是默认的git方法构建请求对象

        # 多个url提供：
        requests_datalist = []
        for i in range(1,6):
            # requests_data = scrapy.Request(url=f'https://tieba.baidu.com/f?kw=%E5%B0%8F%E8%AF%B4&ie=utf-8&pn={(i-1)*50}')
            requests_datalist.append(requests_data)
        return requests_data
    url_name = 0     # 创建类属性来控制下载的文件名字
    def parse(self, response):
        # with open(r'百度首页.html', 'w+', encoding='utf-8') as f:
        #     f.write(response.text)

        with open(fr'百度贴吧第{self.url_name}页.html', 'w+', encoding='utf-8') as f:
            f.write(response.text)
        self.url_name += 1   # 示例对象调用类属性跟着这个p
        '''
        response.text==> 获取响应数据的字符串文本（html）
        response.body==> 获取响应数据的二进制数据
        response.json()==> 获取响应数据的json数据
        :param response:
        :return:
        '''
        # scrapy框架自带xpath解析，使用方式如下：
        # response.xpath('xpath表达式')
        '''
        从xpath解析出来的对象提取具体的数据：
            - response.xpath('xpath表达式').getall()==> 提取所有的属性值；   
            - response.xpath('xpath表达式').get()==> 提取第一个属性值；   
        '''
