import time,random,sys,requests
sys.path.append('../..')
from Error_handle import error_handing
from lxml import etree

def get_urllist_urlnamelist()->tuple:
    url = 'http://www.fbook.net/top'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
    }
    res = requests.get(url=url,headers=headers)
    with open('小说排行榜页面.html','w+',encoding='utf-8') as f:
        f.write(res.text)
    html = etree.HTML(res.text)
    url_list = html.xpath('//h2[text()="武侠小说排行榜"]/parent::div//following-sibling::ul//a/@href')[:5]
    urlname_list = html.xpath('//h2[text()="武侠小说排行榜"]/parent::div//following-sibling::ul//a/@title')[:5]
    data = [f'{j}:{i}\n' for i, j in zip(url_list,urlname_list)]
    with open('武侠小说网址备份.txt','w+',encoding='utf-8') as f:
        f.writelines(data)
    return url_list,urlname_list

@error_handing.get_error
def get_data(url,urlname):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
    }
    res = requests.get(url=url,headers=headers)
    with open(f'{urlname}.html','w+',encoding='utf-8') as f:
        f.write(res.text)
    return res.status_code

if __name__=='__main__':
    url_list,urlname_list = get_urllist_urlnamelist()
    for i, j in zip(url_list,urlname_list):
        get_data(url=i,urlname=j)
        time.sleep(random.randint(1,3))