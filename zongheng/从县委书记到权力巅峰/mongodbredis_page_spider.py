import re

import requests,time,random,sys, pymongo, redis
from lxml import etree
sys.path.append('../..')
from Error_handle import error_handing_scrapy

# 纵横中文网 小说在的多页爬取
'''
 爬虫程序结构：
    1.调度器
    2.下载器
    3.解析器
    4.存储器
'''
# 存储器：
# redis数据库的存储：存放url
def redis_wait_to_cramlw_urllist(url:str):
    # 在redis数据库中创建【带爬取url列表，并存放url进去】
    redis_client.rpush('wait_to_cramlw_urllist',url)
def redis_add_new_url(urllist:list):
    if urllist:
        for url in urllist:
            redis_wait_to_cramlw_urllist(url)
def get_new_url()->str:
    new_url = redis_client.lpop('wait_to_cramlw_urllist')
    # 创建一个【已爬取的url列表】来存放所有被爬取成功的url
    redis_client.rpush('cramlwed_list', new_url)
    return new_url     # 返回给调度器
def mongodb_save_data(data_list):
    collection.insert_many(data_list)
# 下载器：
def downloader_start(start_url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = 'bookId=1296249'
    start_res = requests.post(url=start_url, headers=headers, data=data, timeout=3)
    return start_res   # 返回给调度器
@error_handing_scrapy.get_error
def downloader(url:str):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
    }
    res = requests.get(url=url, headers=headers, timeout=3)
    return res   # 返回给装饰器函数
# 解析器
def start_parser(start_res)->tuple:
    urllist = [f'https://read.zongheng.com/chapter/1296249/{i.get("chapterId")}.html' for i in
               start_res.json().get('result').get('chapterList')[0].get('chapterViewList')]
    urlcount = start_res.json().get('result').get('chapterSum')
    return urllist, urlcount
def parser(res)->tuple:
    html = etree.HTML(res.text)
    chaptername = html.xpath('//div[@class="title_txtbox"]//text()')[0]
    bookcontent = '\n'.join(html.xpath('//div[@class="content"]//text()'))
    return chaptername, bookcontent
# 调度器：
def scheduler(start_url):
    data_list = []
    try:
        # 设置连接下载器、解析器和存储器的运行代码
        # 把第一个url进行redis的存放
        redis_wait_to_cramlw_urllist(start_url)
        start_url = get_new_url()
        start_res = downloader_start(start_url)
        urllist, urlcount = start_parser(start_res)
        redis_add_new_url(urllist)
        n = int(input(f'请输入需要爬取的章节数（总共有{urlcount}章）:'))

        while redis_client.llen('cramlwed_list') <n:
            time.sleep(random.randint(1, 3))
            url = get_new_url()
            res = downloader(url=url)
            chaptername, bookcontent = parser(res)
            datas = {}
            datas['chaptername'] = chaptername
            datas['url'] = url
            datas['bookcontent'] = bookcontent
            data_list.append(datas)
    except Exception as e:
        print(repr(e))
    mongodb_save_data(data_list)

if __name__ == '__main__':
    redis_client = redis.Redis(host='127.0.0.1',port=6379, decode_responses=True)
    mongodb_client = pymongo.MongoClient(host='127.0.0.1',port=27017)
    db = mongodb_client['纵横中文网']
    collection = db['从县委书记到权力巅峰']
    # 启动爬虫程序
    scheduler(start_url='https://bookapi.zongheng.com/api/chapter/getChapterList')



