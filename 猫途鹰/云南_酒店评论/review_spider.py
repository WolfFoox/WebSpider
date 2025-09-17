import time,random,json,requests,sys, os
from lxml import etree
sys.path.append('../..')
from Error_handle import error_handing
# 第一步：爬取所有酒店的名称，评论总数
def get_urlnamelist__totallist():
    url = 'https://api.tripadvisor.cn/restapi/soa2/21221/globalSearch'
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
        'content-type' : 'application/json;charset:utf-8;'
    }
    data = {"keywords":"云南","pageNo":1,"pageSize":30,"lat":"","lon":""}
    res = requests.post(url=url, headers=headers,json=data)
    # 下载器：
    with open(rf'云南搜索首页-酒店数据.json','w+',encoding='utf-8') as f:
        json.dump(res.json(),f,ensure_ascii=False, indent=4)
    # 解析器：从响应数据中提取出所有酒店的名称、评论总数
    url_namelist = [i.get('name') for i in res.json().get('result').get('hits')]
    total_list = [i.get('totalComments') for i in res.json().get('result').get('hits')]
    locationIdlist = [i.get('taId') for i in res.json().get('result').get('hits')]
    # 存储器： 把酒店名称、评论总数备份到txt里面去
    datalist = [f'{x}==> {y}\n' for x,y in zip(url_namelist, total_list)]
    with open(rf'云南酒店名称和评论总数统计.txt','w+',encoding='utf-8') as f:
        f.writelines(datalist)
    return url_namelist,locationIdlist
# 第二步：每个酒店的评论区数据爬取
@error_handing.get_error
def get_data(url:int,url_name:str):
    data_url = 'https://api.tripadvisor.cn/restapi/soa2/20997/getList'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
        'content-type': 'application/json;charset:utf-8;'
    }
    data = {"frontPage":"USER_REVIEWS","locationId":url,"selected":{"airlineIds":[],"airlineSeatIds":[],"langs":["zhCN"],"ratings":[],"seasons":[],"tripTypes":[],"airlineLevel":[]},"pageInfo":{"num":i,"size":10}}
    res = requests.post(url=data_url,headers=headers,json=data)
    # 下载器：
    if os.path.exists(rf'{url_name}') == False:
        os.mkdir(rf'{url_name}')
    with open(rf'{url_name}\评论区数据.json','w+',encoding='utf-8') as f:
        json.dump(res.json(),f,ensure_ascii=False,indent=4)

    titlelist = [i.get('title') for i in res.json().get('details')]
    contentlist = [i.get('content') for i in res.json().get('details')]

    # 存储器：
    datalist = [f'{x}-->{y}\n' for x,y in zip(titlelist,contentlist)]
    with open(rf'{url_name}\第{i}页评论.txt','w+',encoding='utf-8') as f:
        f.writelines(datalist)
    return res.status_code
# https://api.tripadvisor.cn/restapi/soa2/20997/getList

if __name__ == '__main__':
    url_namelist,locationIdlist = get_urlnamelist__totallist()
    for url_name, id in zip(url_namelist,locationIdlist): # 不同酒店
        for i in range(1,6): # 5页爬取
            get_data(url = id,url_name=url_name)
            time.sleep(random.randint(1,3))

