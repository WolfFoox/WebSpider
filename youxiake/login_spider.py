import requests

def denlu()->str:
    url = 'https://www.youxiake.com/login/verify'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    name = input('请输入用户名：')
    password = input('请输入密码：')
    data = f'loginType=1&logonId={name}&password_input={password}&geetest_challenge=&geetest_validate=&geetest_seccode='


    res = requests.post(url=url,headers=headers,data=data)

    # 解析器
    token_data = res.cookies.get('yxk_auth')
    return token_data

def data(token_data):
    # 调度器
    url = 'https://www.youxiake.com/'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        'cookie' : f'yxk_auth={token_data}'
    }

    res = requests.get(url=url,headers=headers)

    with open('游侠客登录首页页面.html','w+',encoding = 'utf-8') as f:
        f.write(res.text)


if __name__ == '__main__':
    token_data = denlu()
    data(token_data)