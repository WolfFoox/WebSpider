import requests, random, time, execjs, re, json, sys
from lxml import etree
from Crypto.Cipher import AES      # 导入加密模块AES或DES
from Crypto.Util.Padding import pad, unpad    # 导入填充方法和清除方法
import base64
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
    # with open(r'song_js.js', 'r', encoding='utf-8') as f:
    #     js_data = f.read()
    # js = execjs.compile(js_data)
    # reslut = js.call('asrsea', id)
    # 用python逻辑写出js的生成代码：
    id_dict = f'{{"ids":"[{id}]","level":"exhigh","encodeType":"aac","csrf_token":"5eea58d68166c0ff44bcc67bd99780d5"}}'
    g = "0CoJUm6Qyw8W8jud"
    iv = "0102030405060708"
    AES_dict = AES.new(key=g.encode('utf-8'), mode=AES.MODE_CBC, iv=iv.encode('utf-8'))
    pad_data = pad(id_dict.encode('utf-8'), AES.block_size)
    AES_en = AES_dict.encrypt(pad_data)
    AES_en_data = base64.b64encode(AES_en)
    result1 = AES_en_data.decode('utf-8')
    i = "4Tkv8GwUXc7LBAC9"
    AES_dict = AES.new(key=i.encode('utf-8'), mode=AES.MODE_CBC, iv=iv.encode('utf-8'))
    pad_data = pad(result1.encode('utf-8'), AES.block_size)
    AES_en = AES_dict.encrypt(pad_data)
    AES_en_data = base64.b64encode(AES_en)
    import urllib.parse
    encText = urllib.parse.quote(AES_en_data.decode('utf-8'))   # 把加密后的数据转为可以传输的数据
    encSecKey = "cbf9ca65faa714173aed79ac4507a2397f58c823af5eee415d4c66e98e96154aae9ebb4734682732c0d431e4bdd73a29df16eadd17f53a1e83afe25f8d2fa3519d04906b979e272fbb9d363ed5a1bd39a45027f87d55e626e2587ca7aa181208d787494fc5af9a3164e3a5218a1715d7b794e5f6c98124d656c8072f1c8cc06e"
    data = f'params={encText}&encSecKey={encSecKey}'
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