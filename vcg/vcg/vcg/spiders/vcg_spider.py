import scrapy, json


class VcgSpiderSpider(scrapy.Spider):
    name = "vcg_spider"
    # allowed_domains = ["www.vcg.com"]
    # start_urls = ["https://www.vcg.com"]
    # 如果爬取的网站的请求方法是post模式，那么就需要单独把start_requests函数写出来修改请求方法

    def start_requests(self):
        # post请求：把默认的get方法的请求函数中写出method参数,更改请求方法名
        # 情况一：当请求体数据是json格式时，就是使用默认的scrapy.Request()打包就行

        url = 'https://www.vcg.com/graphql/login'
        headers = {
            'Content-Type': 'application/json'
        }
        data = {"username": "13378838824", "password": "pyspider", "host": "www.vcg.com",
                "ip": "10.12.220.140"}
        return [scrapy.Request(url=url, headers=headers, method='POST', body=json.dumps(data))]
        # 情况二：当请求体的数据是【除了json】以外的【其他格式】时
        # 就要把默认的scrapy.Request()改成scrapy.FormRequest()函数来打包
        # url = 'https://www.youxiake.com/login/verify'
        # headers = {
        #     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        # }
        # name = input('请输入用户名：')
        # password = input('请输入密码：')
        # data = f'loginType=1&logonId={name}&password_input={password}&geetest_challenge=&geetest_validate=&geetest_seccode='
        # return [scrapy.FormRequest(url=url, headers=headers, method='POST', formdata=data)]

    def parse(self, response):
        url = 'https://www.vcg.com/'
        headers = {
            'Cookie':f'api_token={response.json().get("data").get("token")}'
        }
        yield scrapy.Request(url=url, headers=headers, callback=self.next_parse)

    def next_parse(self,response):
        with open(rf'vcg登录后首页页面.html', 'w+', encoding='utf-8') as f:
            f.write(response.text)

