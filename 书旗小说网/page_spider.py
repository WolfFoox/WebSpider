# 批量爬取《科技：天后自爆恋情，我国士身份藏不住了》小说多章节的文本内容
import requests, re, json, random, time, sys
from lxml import etree
sys.path.append('..')
from Error_handle import error_handing
import execjs
# 第一步：去章节页面的静态html响应数据中提取每个章节的三个动态请求参数
def get_urllist_urlnamelist():
    url = 'https://www.shuqi.com/reader?bid=8742220&cid=1896593'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
    }
    res = requests.get(url=url, headers=headers)
    with open(r'章节页面.html', 'w+', encoding='utf-8') as f:
        f.write(res.text)
    html = etree.HTML(res.text)
    data = html.xpath('//i[@class="page-data js-dataChapters"]/text()')[0]
    data_dict = eval(html.xpath('//i[@class="page-data js-dataChapters"]/text()')[0].replace('false', 'False').replace('true', 'True').replace('null', '""'))
    with open(r'数据.json', 'w+', encoding='utf-8') as f:
        json.dump(data_dict, f, ensure_ascii=False, indent=4)
    urllist = [f'https://c13.shuqireader.com/pcapi/chapter/contentfree/{i.get("contUrlSuffix")}' for i in data_dict.get('chapterList')[0].get('volumeList')]
    urlnamelist = [i.get('chapterName') for i in data_dict.get('chapterList')[0].get('volumeList')]
    return urllist, urlnamelist

# 第二步：进行每一章的爬取，获取到响应部分
@error_handing.get_error
def get_data(url:str, url_name:str):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
    }
    res = requests.get(url=url, headers=headers)
    print(res.json())
    # 进行响应数据解码操作，得出正常的中文数据：
    with open(r'decode_js.js', 'r', encoding='utf-8') as f:
        js_data = f.read()
    data = execjs.compile(js_data)
    result = data.call('_decodeCont', res.json().get("ChapterContent"))
    with open(rf'{url_name}.html', 'w+',encoding='utf-8') as f:
        f.write(result)
    return res.status_code
urllist, urlnamelist = get_urllist_urlnamelist()
total = len(urlnamelist)
n = int(input(f'总共有{total},请问需要爬多少章：'))
for i in range(n):
    get_data(url=urllist[i], url_name = urlnamelist[i])
    # 延时装置：
    time.sleep(random.randint(1,3))