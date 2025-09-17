import requests

def search()->tuple:
    params = input('请输入搜索关键词：')
    url = f'https://www.vcg.com/creative-image/{params}/'
    header = {
        'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
    }

    res = requests.get(url=url,headers=header)

    return params,res

def downlaod(params,res):
    with open(rf'搜索_{params}页面.html','w+',encoding='utf-8') as f:
        f.write(res.text)

if __name__ == '__main__':
    params,res = search()
    downlaod(params,res)
