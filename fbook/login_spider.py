import requests

def get_img_url():
    url = 'http://www.fbook.net/Member/Login'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
    }

    res = requests.get(url=url,headers=headers,verify=False)

    img_url = 'http://www.fbook.net'+'/Member/Captcha?t=636232940022839332'

    return  img_url

def download_img(img_url)->str:
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
    }

    res = requests.get(url=img_url,headers=headers,verify=False)

    with open('验证码.jpg','wb+') as f:
        f.write(res.content)

    captcha = input('请输入验证码：')
    return captcha

def denlu(captcha)->str:
    url = 'http://www.fbook.net/Member/Login'

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8'
    }

    data = f'loginName=13378838824&loginPass=pyspider&captcha={captcha}'
    res = requests.post(url=url,headers=headers,data=data,verify=False)

    token = res.cookies.get('max')

    return token

def data(token):
    url = 'http://www.fbook.net/'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        'cookie': f'max={token}'
    }
    res = requests.get(url=url,headers=headers,verify=False)

    with open('天下书盟首页登录页面.html','w+',encoding='utf-8') as f:
        f.write(res.text)


if __name__ == '__main__':
    img_url = get_img_url()
    captcha = download_img(img_url)
    token = denlu(captcha)
    data(token)