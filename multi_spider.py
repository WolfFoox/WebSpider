import requests, random, time
from Error_handle import error_handing
# 不同网站的批量爬取
@error_handing.get_error
def get_data(url,name):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
    }
    res = requests.get(url=url,headers=headers,timeout=3)
    # res.apparent_encoding = res.encoding
    with open(rf'{name}首页页面.html','w+',encoding='utf-8') as f:
        f.write(res.text)

    return res.status_code

# 设置批量爬取机制
name = ['baidu','vcg','youxiake']
url_list = ['https://www.baidu.com','https://www.vcg.com/','https://www.youxiake.com']
i = 0
for url in url_list:
    get_data(url = url,name = name[i])
    i = i+1
    # 设置延迟机制，每一次爬取的间隔
    requests_time = random.randint(1,3)
    time.sleep(requests_time)