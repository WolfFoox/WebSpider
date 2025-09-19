import requests,time,random,sys, re, json
import threading
from lxml import etree
sys.path.append('../..')
from Error_handle import error_handing

def get_urlcount_urlid_urlname()->tuple:
    url = 'https://bookapi.zongheng.com/api/chapter/getChapterList'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded'
    }
    data = 'bookId=1296249'
    res = requests.post(url=url, headers=headers, data=data, timeout=3)
    # 下载器
    with open(rf'从县委书记到权力巅峰目录API端口数据.json', 'w+', encoding='utf-8') as f:
        json.dump(res.json(), f, ensure_ascii=False, indent=4)
    # 解析器
    # 用字典的方式进行值的提取
    urlcount = res.json().get('result').get('chapterSum')
    urllist = [str(i.get('chapterId')) for i in res.json().get('result').get('chapterList')[0].get('chapterViewList')]
    urlnamelist = [i.get('chapterName') for i in
                   res.json().get('result').get('chapterList')[0].get('chapterViewList')]
    return urlcount, urllist, urlnamelist

# def get_url(url):
#     headers = {
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
#     }
#     res = requests.get(url=url, headers=headers, timeout=3)
#     html = etree.HTML(res.text)
#     url ='https://read.zongheng.com' + html.xpath('//a[text()="下一章"]/@href')[0]
#     return url

@error_handing.get_error
def get_data(url:str, url_name:str):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
    }
    res = requests.get(url='https://read.zongheng.com/chapter/1296249/'+url+'.html', headers=headers, timeout=3)
    html = etree.HTML(res.text)
    file_name = html.xpath('//div[@class="title_txtbox"]//text()')[0]
    # 存储器
    with open(f'{url_name}.html', 'w+', encoding='utf-8') as f:
        f.write(res.text)

    return res.status_code

if __name__ == '__main__':
    urlcount, urllist, urlnamelist = get_urlcount_urlid_urlname()
    n = int(input(f'请输入需要爬取的章节数（总共有{urlcount}章）:'))
    for i in range(0,n):
        t = threading.Thread(target=get_data,kwargs = {'url':urllist[i],'url_name':urlnamelist[i]})
        t.start()
        # 延时装置
        # time.sleep(random.randint(1,3))

