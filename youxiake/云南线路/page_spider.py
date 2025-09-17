import requests,time,random,sys
from lxml import etree
sys.path.append('../..')
from Error_handle import error_handing
@error_handing.get_error
def get_data(url,urlname):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
    }
    res = requests.get(url=url,headers=headers,timeout=3)
    with open(f'云南路线{urlname}页.html','w+',encoding='utf-8') as f:
        f.write(res.text)

    return res.status_code

if __name__ == '__main__':
    for i in range(1,5):
        url = f'https://www.youxiake.com/search/results/0-2791-0-0-0-0.html?keyword=&spm=&page={i}'
        get_data(url=url,urlname=i)
        time.sleep(random.randint(1,3))
