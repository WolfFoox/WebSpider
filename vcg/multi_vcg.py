import requests
import time
import error_handing
import random

@error_handing.get_error
def search_data(params)->tuple:
    # params = input('请输入搜索关键词：')
    url = f'https://www.vcg.com/creative-image/{params}/'
    header = {
        'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
    }

    res = requests.get(url=url,headers=header)

    with open(rf'搜索_{params}页面.html','w+',encoding='utf-8') as f:
        f.write(res.text)

    return res.status_code



if __name__ == '__main__':
    param_list = input('请输入关键词（可输入多个，并用英文逗号隔开）：').split(',')
    for param in param_list:
        search_data(params=param)

        request_time = random.randint(1,3)
        time.sleep(request_time)