# 爬取vcg网站首页5张图片
import requests,sys,time,random,re
sys.path.append('../..')
from Error_handle import error_handing
from proxy_ip import get_iplist
# 使用本地存储的ip
with open(r'ip_list.txt','r',encoding='utf-8') as f:
    ip_list = f.readlines()
def get_urllist_urlnamelist()->tuple:
    url = f'https://www.vcg.com/'
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
    }

    res = requests.get(url=url, headers=header)

    with open(rf'vcg首页.html', 'w+', encoding='utf-8') as f:
        f.write(res.text)

    url_list = re.findall('<picture class="_2t2n7" style="background-image:url\((.*?)\)"></picture>',res.text)[:5]
    urlname_list = re.findall('<span class="_3lx_6">(.*?)</span>',res.text)[:5]

    data = [f'{j}:{i}\n' for i, j in zip(url_list,urlname_list)]

    with open('vcg首页5张图片网址备份.txt', 'w+', encoding='utf-8') as f:
        f.writelines(data)
    return url_list,urlname_list

@error_handing.get_error
def get_img(url,urlname):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
    }
    # 设置代理ip:
    ip = random.choice(ip_list)
    proxy = {
        'http':f'http://{ip}',
        'https':f'http://{ip}'
    }
    res = requests.get(url=url,headers=headers,proxies=proxy, timeout=6)
    with open(f'{urlname}.jpg','wb+') as f:
        f.write(res.content)
    return res.status_code

if __name__ == '__main__':
    url_list,urlname_list = get_urllist_urlnamelist()
    for i in range(5):
        get_img(url=url_list[i],urlname=urlname_list[i])
        time.sleep(random.randint(1,3))