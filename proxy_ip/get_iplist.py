import requests, json,threading


def get_iplist()->list:
    url = 'https://www.proxy-list.download/api/v2/get?l=en&t=http'
    # url = 'https://www.proxy-list.download/HTTP'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
    }
    res = requests.get(url=url, headers=headers)
    # 下载器：把响应数据存储为json格式
    with open(r'ip_list.json','w+',encoding='utf-8') as f:
        json.dump(eval(res.text),f,ensure_ascii=False,indent=4)
    # 解析器：提取代理ip地址和ip端口号
    ip_list= [f'{i.get("IP")}:{i.get("PORT")}' for i in eval(res.text).get('LISTA')]
    return ip_list

# 第二步==》检测每一个代理ip是否有效，进行筛选有效的ip存储到本地
def check_ip(ip:str):
    # 设置代理ip:
    proxy = {
        'http':f'http://{ip}',
        'http':f'http://{ip}',
    }
    # 使用代理ip
    try:
        url = 'https://www.baidu.com'
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
        }
        res = requests.get(url=url,headers=headers,proxies=proxy,timeout=3)
    except Exception as e:
        ip_list.remove(ip)

ip_list = get_iplist()
ip_list2 = ip_list.copy()
threads = []
for ip in ip_list2:
    t = threading.Thread(target=check_ip,args = (ip,))
    threads.append(t)
    t.start()

for i in threads:
    i.join()

# 存储器：把有效的代理ip存储到本地文件中
with open(r'ip_list.txt','a+', encoding='utf-8') as f:
    for i in ip_list:
        f.write(f'{i}\n')