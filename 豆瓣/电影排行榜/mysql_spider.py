import time,random,json,requests,sys, os, openpyxl,re,pymysql
import pandas as pd
from openpyxl.styles import Font,PatternFill,Alignment
from lxml import etree
sys.path.append('../..')
from Error_handle import error_handing
# 从json数据包中提取出‘总章数’和‘全部章节API端口
# zonghenzhonwen.rollback()
try:
    douban = pymysql.Connect(
        host='127.0.0.1',
        port=3306,
        user='admin',
        password='qwe123',
        database='豆瓣',
        charset='utf8'
    )
    db = douban.cursor()
    # 第一步==》
    def get_url_urlname() -> tuple:
        # 调度器
        url = 'https://movie.douban.com/chart'
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
        }
        res = requests.get(url=url, headers=headers, timeout=3)
        # 下载器
        with open(rf'豆瓣电影排行榜首页.html', 'w+', encoding='utf-8') as f:
            f.write(res.text)
        # 解析器
        html = etree.HTML(res.text)
        url_list = html.xpath('//a[@class="nbg"]/@href')
        urlnamelist = html.xpath('//a[@class="nbg"]/@title')

        return url_list, urlnamelist

#   第二步==>提取每部电影的‘电影名称’、‘电影网址’、‘电影评分’、‘上映时间’、‘主演’、‘电影类型’、‘电影简介’
    @error_handing.get_error
    def get_data(url:str,urlname:str):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
        }
        res = requests.get(url=url, headers=headers, timeout=3)

        # 下载器
        with open(rf'{urlname}.html', 'w+', encoding='utf-8') as f:
            f.write(res.text)
        # 解析器
        html = etree.HTML(res.text)
        if(html.xpath('//strong[@property="v:average"]/text()')):
            average = html.xpath('//strong[@property="v:average"]/text()')[0]
        else:
            average = '暂无'
        Releasetime = "/".join(html.xpath('//span[@property="v:initialReleaseDate"]/text()'))
        starring = "/".join(html.xpath('//a[@rel="v:starring"]/text()'))
        gener = "/".join(html.xpath('//span[@property="v:genre"]//text()'))
        summary = html.xpath('//span[@property="v:summary"]/text()')[0].strip()

        # 存储器：mysql
        db.execute(f'create table if not exists 电影排行榜每部电影详细信息表(电影名称 varchar(25),电影网址 varchar(100),电影评分 varchar(10), 上映时间 varchar(200), 主演 varchar(300),电影类型 varchar(100), 电影简介 varchar(1000))')
        db.execute(f'insert into 电影排行榜每部电影详细信息表 values ("{urlname}","{url}","{average}","{Releasetime}","{starring}","{gener}","{summary}")')
        return res.status_code

    url_list, urlnamelist = get_url_urlname()
    for url,urlname in zip(url_list,urlnamelist):
        get_data(url=url,urlname=urlname)
        time.sleep(random.randint(1,3))
except Exception as e:
    douban.rollback()
    print(repr(e))
else:
    douban.commit()
finally:
    db.close()
    douban.close()