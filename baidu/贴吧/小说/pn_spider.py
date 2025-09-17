import requests,time,random,sys, re
from lxml import etree
sys.path.append('../../..')
from Error_handle import error_handing
def get_count()->int:
    url = 'https://tieba.baidu.com/f?kw=%E5%B0%8F%E8%AF%B4&ie=utf-8&pn=0'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
    }
    res = requests.get(url=url, headers=headers, timeout=3)
    with open('小说贴吧首页.html','w+',encoding='utf-8') as f:
        f.write(res.text)
    count = int(re.findall('&pn=(.*?)" class="last pagination-item " >尾页</a>',res.text)[0])
    count = int(count/50 + 1)
    return count
@error_handing.get_error
def get_data(url,urlname):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
    }
    res = requests.get(url=url,headers=headers,timeout=3)
    with open(f'第{urlname+1}页.html','w+',encoding='utf-8') as f:
        f.write(res.text)

    return res.status_code

if __name__ == '__main__':
    count = get_count()
    n = int(input(f'总共有{count}页，请输入需要爬取的页数：'))
    for i in range(n):
        url = f'https://tieba.baidu.com/f?kw=%E5%B0%8F%E8%AF%B4&ie=utf-8&pn={i*50}'
        get_data(url=url,urlname=i)
        time.sleep(random.randint(1,3))
