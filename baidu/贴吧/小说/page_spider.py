import requests,time,random,sys, re
from lxml import etree
sys.path.append('../../..')
from Error_handle import error_handing
from proxy_ip import  get_iplist
# 使用本地存储的ip
# with open(r'F:\document\personal\codepractice\python\workpackage\python_xin\WebSpider\proxy_ip\ip_list.txt','r',encoding='utf-8') as f:
#     ip_list = f.readlines()
def get_count()->int:
    url = 'https://tieba.baidu.com/f?kw=%E5%B0%8F%E8%AF%B4&ie=utf-8&pn=0'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        'cookie': 'BIDUPSID=4A1FC7E31CF17ED10F24EB91B6054291; PSTM=1744722507; BAIDUID=4A1FC7E31CF17ED1E56E7D3A73726B4C:FG=1; BAIDUID_BFESS=4A1FC7E31CF17ED1E56E7D3A73726B4C:FG=1; BAIDU_WISE_UID=wapp_1747206086208_943; arialoadData=false; ZFY=1B40Rs:BWjOzZ0Ss67DD2mTIiRLYFMV7Du0YHMU:AopP8:C; H_PS_PSSID=63142_63327_64648_64701_64818_64811_64841_64911_64981_65007_65002_65022_65077_65085_65131_65142_65139_65137_65159_65194_65204_64624_65230_65242_65257_65144_65269_65301_65373; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_WISE_SIDS=63142_63327_64648_64701_64818_64811_64841_64911_64981_65007_65002_65077_65085_65131_65142_65139_65137_65159_65194_65204_64624_65230_65242_65257_65144_65269_65301_65373; Hm_lvt_292b2e1608b0823c1cb6beef7243ef34=1758204702,1758249756; Hm_lpvt_292b2e1608b0823c1cb6beef7243ef34=1758249756; HMACCOUNT=AF7BA5E5A557E26C; USER_JUMP=-1; video_bubble0=1; XFI=4cba8210-9502-11f0-ae9f-077e1375aa3b; BA_HECTOR=a58ga18ga085a421a12g810485258n1kcpgos24; ariaappid=c890648bf4dd00d05eb9751dd0548c30; ariauseGraymode=false; ab_sr=1.0.1_MzY3MGU2NWQzNWVmODA3MDdkMjUyMWZkZTVjZWY4MTdlYTYxODljYzQ2MDJkOGFhYWI4ZDcyOTZiZTlkNjk1NWJmYzM1Y2M5YWVhZTYzNjdmMGQxYjA1NTgyNWU1NDYwNDc0ZjQ5NDNiZDk1ZmQxYjc2MmE5OTI3ZTdjNTZkZTFmZTc4MTdjOWMyZWY4Mzk3ZDA1MGNmYzFmMDA5YTRjNA==; st_data=ef2d19b9c9d44e661ce5f1a763c570b7f573d50fd3d71647874bc7ca83fac731fd6ba193226f336f2377e3d5d5f4976773a85d573099332cd49dae519a889a4ff6663b6b1a77633891a5b56a22cf7db12b48a2e57a7033b13227ee6de59c52775434394152d523bfc23888343cce4c224fa70be6a8d9eb05166ef6922c6d0d829aaf428c25b4ce63a177819fdb2d5891; st_key_id=17; st_sign=2f75cb74; XFCS=0A5848D6C6B3F4D8F816A9ACED2E0E3ACBD0CDB54667C25B766045ACDA23FA36; XFT=xmPFT+pjlkPzEbbKWL7FA0CEzE7u+tn9s7lmUkGJH5s='
    }
    res = requests.get(url=url, headers=headers, timeout=3)
    with open('小说贴吧首页.html','w+',encoding='utf-8') as f:
        f.write(res.text)
    count = int(re.findall('&pn=(.*?)" class="last pagination-item " >尾页</a>',res.text)[0])
    count = int(count/50 + 1)
    return count
@error_handing.get_error
def get_data(url,urlname):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
    }
    # 设置代理ip
    ip = random.choice(get_iplist.ip_list)
    proxy = {
        'http':f'http//{ip}',
        'https':f'http://{ip}',
    }
    res = requests.get(url=url,headers=headers,proxies=proxy,timeout=6)
    with open(f'第{urlname+1}页.html','w+',encoding='utf-8') as f:
        f.write(res.text)

    return res.status_code

if __name__ == '__main__':
    count = get_count()
    n = int(input(f'总共有{count}页，请输入需要爬取的页数：'))
    for i in range(n):
        url = f'https://tieba.baidu.com/f?kw=%E5%B0%8F%E8%AF%B4&ie=utf-8&pn={i*50}'
        get_data(url=url,urlname=i)
        time.sleep(random.randint(1,3))
