# 爬取天下书盟本周强推十本小说的页面
import sys
sys.path.append("..")
import requests
import time
import random
import re
from Error_handle import error_handing

# 第一步==》先爬取出天下书盟的首页静态html数据，然后从里面解析提取出‘本周强推’区域内的连接
def get_urlist_urlnamelist()->tuple:
    url = 'http://www.fbook.net/'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
    }

    res = requests.get(url=url,headers=headers)

    with open('fbook.html','w+',encoding = 'utf-8') as f:
        f.write(res.text)

    # 解析器：
    urllist = re.findall('<li><a href=".*?" class="a-link-red2" target="_blank">.*?</a> <a href="(.*?)" target="_blank">.*?</a><span class="color-hui font-size-12"> &nbsp; .*?</span></li>',res.text)
    url_namelist = re.findall(
        '<li><a href=".*?" class="a-link-red2" target="_blank">.*?</a> <a href=".*?" target="_blank">(.*?)</a><span class="color-hui font-size-12"> &nbsp; .*?</span></li>',
        res.text)

    # 可以把网址和名字进行备份：
    data = [f'{j}:{i}\n' for i, j in zip(urllist,url_namelist)]
    with open('网址备份.html','w+',encoding='utf-8') as f:
        f.writelines(data)

    return urllist,url_namelist
@error_handing.get_error
def get_data(url,urlname):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
    }
    res = requests.get(url=url,headers=headers)
    with open(f'{urlname}页面.txt','w+',encoding='utf-8') as f:
        f.write(res.text)
    return res.status_code

if __name__ == '__main__':
    urllist,url_namelist = get_urlist_urlnamelist()
    for i, j in zip(urllist,url_namelist):
        get_data(url=i,urlname=j)
        request_time = random.randint(1,3)
        time.sleep(request_time)