import requests, random, time, execjs, re, json, sys
from lxml import etree
sys.path.append('..')
from Error_handle import error_handing
# 第一步==》 去‘飙升榜’的页面静态html数据中提取每首歌的id号和名称
def get_songidlist_songnamelist()->tuple:
    url = 'https://music.163.com/discover/toplist'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
    }
    res = requests.get(url=url, headers=headers)
    with open(r'飙升榜歌曲目录.html', 'w+',encoding='utf-8') as f:
        f.write(res.text)
    html = etree.HTML(res.text)
    songidlist = [i.split('=')[1] for i in html.xpath('//ul[@class="f-hide"]//a/@href')]
    songnamelist = html.xpath('//ul[@class="f-hide"]//a/text()')
    return songidlist, songnamelist

# 第二步==》从每首歌的动态数据中提取出音频的url网址
def get_songurl(id, songname)->str:
    url = 'https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token=5eea58d68166c0ff44bcc67bd99780d5'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded'
    }
    with open(r'song_js.js', 'r', encoding='utf-8') as f:
        js_data = f.read()
    js = execjs.compile(js_data)
    reslut = js.call('asrsea', id)
    data = f'params={reslut["encText"]}&encSecKey={reslut["encSecKey"]}'
    res = requests.post(url=url, headers=headers, data=data)
    with open(rf'{songname}.json','w+', encoding='utf-8') as f:
        json.dump(res.json(), f, ensure_ascii=False, indent=4)
    song_url = res.json().get('data')[0].get('url')
    return song_url

# 第三步==》进行具体的音频请求爬取下载为歌曲文件
@error_handing.get_error
def get_data(url, url_name)->str:
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
    }
    res = requests.get(url=url, headers=headers)
    with open(rf'{url_name}.m4a','wb+') as f:
        f.write(res.content)
    return res.status_code

songidlist, songnamelist = get_songidlist_songnamelist()
n = int(input(f"请输入需要爬取歌曲的数目（总共{len(songnamelist)}首）："))
for i in range(n):
    song_url = get_songurl(songidlist[i], songnamelist[i])
    if song_url is None:
        n = n + 1
        continue
    get_data(url=song_url, url_name=songnamelist[i])
    time.sleep(random.randint(1, 3))