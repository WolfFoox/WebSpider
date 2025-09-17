import requests,time,random,sys, re
from lxml import etree
sys.path.append('../..')
from Error_handle import error_handing
def get_count()->int:
    url = 'https://www.vcg.com/creative-image/guoqing/'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
    }
    res = requests.get(url=url, headers=headers, timeout=3)
    with open('vcg国庆首页.html','w+',encoding='utf-8') as f:
        f.write(res.text)
    count = int(re.findall('class="page-link">(.*?)</a>',res.text)[-1])
    return count

def get_data(url,urlname):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
    }
    res = requests.get(url=url,headers=headers,timeout=3)
    with open(f'第{urlname}页.html','w+',encoding='utf-8') as f:
        f.write(res.text)

    html = etree.HTML(res.text)
    url_list = html.xpath('//a[@class="imgWaper"]/img/@data-src')[:4]
    url_list = ['https:' + i for i in url_list]
    urlname_list = html.xpath('//a[@class="imgWaper"]/@title')[:4]

    data = [f'{j}:{i}\n' for i, j in zip(url_list, urlname_list)]

    with open('网址备份.txt', 'w+', encoding='utf-8') as f:
        f.writelines(data)
    return url_list, urlname_list

@error_handing.get_error
def get_img(url,urlname,page):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
    }
    res = requests.get(url=url, headers=headers, timeout=3)
    with open(f'第{page}页{urlname}.jpg', 'wb+') as f:
        f.write(res.content)
    return res.status_code

if __name__ == '__main__':
    count = get_count()
    n = int(input(f'总共有{count}页，请输入需要爬取的页数：'))
    for i in range(1,n+1):
        url = f'https://www.vcg.com/creative-image/guoqing/?page={i}'
        url_list,urlname_list = get_data(url=url,urlname=i)
        for a, b in zip(url_list,urlname_list):
            get_img(url=a,urlname=b,page=i)
            time.sleep(random.randint(1,3))
