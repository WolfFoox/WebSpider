import requests

#爬虫架构设计：
# 调度器：设置请求包，发送请求包，获取响应数据，返回给下载器
def search()->tuple:
    params = input('请输入搜索关键词：')
    url = f'https://www.baidu.com/s?wd={params}'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        'referer': 'https://www.google.com.hk/',
        'cookie': 'BIDUPSID=4A1FC7E31CF17ED10F24EB91B6054291; PSTM=1744722507; BAIDUID=4A1FC7E31CF17ED1E56E7D3A73726B4C:FG=1; BD_UPN=12314753; H_PS_PSSID=61027_62325_62849_62867_62883_62886_62926_62917_62920_62913_62968_62930_62976; BA_HECTOR=25858k0h8ka4ag24a4a0052g29e2kn1k01u8m22; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BAIDUID_BFESS=4A1FC7E31CF17ED1E56E7D3A73726B4C:FG=1; delPer=0; BD_CK_SAM=1; PSINO=1; ZFY=CGG0nUPB:AJPSCys9XDZIfj0JqfSCPa6YwWYYnaa8pbo:C; channel=google; COOKIE_SESSION=0_0_1_1_0_2_1_0_1_1_5_1_0_0_0_0_0_0_1744894258%7C1%230_0_1744894258%7C1; ab_sr=1.0.1_MzIyM2IzZWExODYzNzE4ZTBkMGFjOTRiMjE0OWQxMzYwNzJhNzllZjZiNGE4Mzc2NTdlMTYzYTlkZThiNTk0M2Y0MzJmZDhiNjE3ZTM0YTQzZDMzY2VkMGJkZDU1ZWRmOGJiMTM1Y2UzNjEzMzNmZmM5YTU1MGZkMjRlMTEwYzM1YzJkMzI2MTkwMGI4NzA0MTUxMzMwZGU4MWRlODNkOQ==; H_PS_645EC=d8a5EwJD0Z4aAwuPNlAsmfX%2BoWtto3xjizyl3PUeOOlEHUAHDVbljFY8dSI; baikeVisitId=2608886f-28e6-4c3d-bafd-07268144f2df'
    }
    res = requests.get(url=url, headers=headers)
    print(res.status_code)
    return params,res

# 下载器：把收到的调度器的数据进行对应的下载
def downlaod(params, res):
    with open(rf'搜索-{params}页面.html','w+',encoding='utf-8') as f:
        f.write(res.text)

    # 解析器：写从整个静态页面中提取出来的具体数据的正则解析代码或xpath解析代码等
    # 模块过滤器：可以让执行语句只在自己这个模块内执行，不会导入到其他文件中去自动执行

if __name__ == '__main__':
    params, res = search()
    downlaod(params,res)
