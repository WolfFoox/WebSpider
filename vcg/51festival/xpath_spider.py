import requests,sys,time,random
sys.path.append('../..')
from Error_handle import error_handing
from lxml import etree

def get_urllist_urlnamelist(param)->tuple:
    url = f'https://www.vcg.com/creative-image/{param}/'
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
    }

    res = requests.get(url=url, headers=header)

    with open(rf'搜索_{param}页面.html', 'w+', encoding='utf-8') as f:
        f.write(res.text)

    html = etree.HTML(res.text)
    url_list = html.xpath('//img[@class="lazyload_hk "]/@data-src')[:20]
    url_list = ['https:'+i for i in url_list]
    urlname_list = html.xpath('//a[@class="imgWaper"]/@title')[:20]

    data = [f'{j}:{i}\n' for i, j in zip(url_list,urlname_list)]

    with open('网址备份.txt', 'w+', encoding='utf-8') as f:
        f.writelines(data)
    return url_list,urlname_list

@error_handing.get_error
def get_img(url,urlname):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
    }
    res = requests.get(url=url,headers=headers,timeout=3)
    with open(f'{urlname}.jpg','wb+') as f:
        f.write(res.content)
    return res.status_code

if __name__ == '__main__':
    param = input('请输入搜索关键词：')
    url_list,urlname_list = get_urllist_urlnamelist(param)
    for i in range(20):
        get_img(url=url_list[i],urlname=urlname_list[i])
        time.sleep(random.randint(1,3))

