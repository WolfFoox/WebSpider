import time,random,json,requests,sys, os, openpyxl, threading
import pandas as pd
from openpyxl.styles import Font,PatternFill,Alignment
from lxml import etree
sys.path.append('../..')
from Error_handle import error_handing
# 第一步：爬取所有酒店的名称，评论总数
def get_urlnamelist_totallist():
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
    pageUrllist = [i.get('pageUrl') for i in res.json().get('result').get('hits')]
    # 存储器： 把酒店名称、评论总数备份到txt里面去
    # datalist = [f'{x}==> {y}\n' for x,y in zip(url_namelist, total_list)]
    # with open(rf'云南酒店名称和评论总数统计.txt','w+',encoding='utf-8') as f:
    #     f.writelines(datalist)
    # excel存储器：
    global filename, wt
    filename = r'云南酒店详细数据表格.xlsx'
    if os.path.exists(filename) == False:
        wt = pd.ExcelWriter(filename)
    data = {'酒店名称': url_namelist, '酒店评论id': locationIdlist, '评论总数': total_list, '酒店网址':pageUrllist}
    df = pd.DataFrame(data)
    df.to_excel(wt,sheet_name='云南酒店网址信息备份',index=False)
    return url_namelist,locationIdlist
# 第二步：每个酒店的评论区数据爬取
@error_handing.get_error
def get_data(url:int,url_name:str):
    data_url = 'https://api.tripadvisor.cn/restapi/soa2/20997/getList'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
        'content-type': 'application/json;charset:utf-8;'
    }
    data = {"frontPage":"USER_REVIEWS","locationId":url,"selected":{"airlineIds":[],"airlineSeatIds":[],"langs":["zhCN"],"ratings":[],"seasons":[],"tripTypes":[],"airlineLevel":[]},"pageInfo":{"num":1,"size":10}}
    res = requests.post(url=data_url,headers=headers,json=data)
    # 下载器：
    # if os.path.exists(rf'{url_name}') == False:
    #     os.mkdir(rf'{url_name}')
    # with open(rf'{url_name}\评论区数据.json','w+',encoding='utf-8') as f:
    #     json.dump(res.json(),f,ensure_ascii=False,indent=4)

    titlelist = [i.get('title') for i in res.json().get('details')]
    contentlist = [i.get('content') for i in res.json().get('details')]

    # 存储器：
    # datalist = [f'{x}-->{y}\n' for x,y in zip(titlelist,contentlist)]
    # with open(rf'{url_name}\第{i}页评论.txt','w+',encoding='utf-8') as f:
    #     f.writelines(datalist)
    # excel存储器：
    # existing_data = pd.read_excel(filename, sheet_name=f'{url_name}具体评论')
    data = {'评论标题': titlelist, '评论主体': contentlist}
    df = pd.DataFrame(data)
    df.to_excel(wt, sheet_name=f'{url_name}具体评论', index=False)
    return res.status_code
# https://api.tripadvisor.cn/restapi/soa2/20997/getList

if __name__ == '__main__':
    url_namelist,locationIdlist = get_urlnamelist_totallist()
    threads = []
    for url_name, id in zip(url_namelist,locationIdlist): # 不同酒店
        t = threading.Thread(target=get_data,kwargs = {'url' : id,'url_name':url_name})
        threads.append(t)
        t.start()
        # time.sleep(random.randint(1,3))
    for i in threads:
        i.join()
    wt._save()
    wb = openpyxl.load_workbook(filename)
    sheet1 = wb['云南酒店网址信息备份']
    sheet1.column_dimensions['A'].width = 30
    sheet1.column_dimensions['D'].width = 140
    for i, j, h, k in zip(sheet1['A'], sheet1['B'], sheet1['C'], sheet1['D']):
        i.font = Font(bold=True)
        j.alignment = Alignment(horizontal='center', vertical='center')
        h.font = Font(color='ff1111')
        k.font = Font(color='0000ff')
    for i in wb:
        if i != wb['云南酒店网址信息备份']:
            i.column_dimensions['B'].width = 300
            for j in i['A']:
                j.font = Font(bold=True)
    wb.save(filename)
    wb.save(filename)