import  requests
# 第一步：先模拟登录动作，发送用户名和密码等用户信息进行认证证书
# 然后从这个爬虫程序中获取到的响应部分中提取出‘身份令牌’数据

def denlu()->str:
    # 调度器
    url = 'https://www.vcg.com/graphql/login'
    headers = {
        'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        'Content-Type' : 'application/json' # 这个字段只要在请求标头中发现必须要写上
        # 它是用来告诉浏览器我们提交的请求体部分的数据是什么类型的，服务端得知类型后才能做出处理
    }
    data = {"username":"13378838824","password":"pyspider","host": "www.vcg.com",
                    "ip": "10.12.220.140"}
    res = requests.post(url=url,headers=headers,json=data)
    # 解析器
    token_data = res.json().get('data').get('token')
    return token_data

# 第二步：携带；身份令牌‘数据去爬取登录后的任意页面数据
# 在请求包的请求标头的’cookie'字段中进行携带
def data(token_data):
    # 调度器：
    url = 'https://www.vcg.com/'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        'cookie' : f'api_token={token_data}'
    }
    res = requests.get(url=url,headers=headers)
    # 下载器
    with open(rf'vcg登录后首页页面.html','w+',encoding='utf-8') as f:
        f.write(res.text)

if __name__ == '__main__':
    token_data = denlu()
    data(token_data)

