import requests, json,pymysql, time, random
from lxml import etree

# 从json数据包中提取出‘总章数’和‘全部章节API端口

# zonghenzhonwen.rollback()
try:
    zonghenzhonwen = pymysql.Connect(
        host='127.0.0.1',
        port=3306,
        user='admin',
        password='qwe123',
        database='zonghenzhonwen',
        charset='utf8'
    )
    yb = zonghenzhonwen.cursor()


    def get_url_urlname() -> tuple:
        # 调度器
        url = 'https://bookapi.zongheng.com/api/chapter/getChapterList'
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
            'content-type': 'application/x-www-form-urlencoded'
        }
        data = 'bookId=1296249'
        res = requests.post(url=url, headers=headers, data=data, timeout=3)
        # 下载器
        with open(rf'从县委书记到权力巅峰目录API端口数据.json', 'w+', encoding='utf-8') as f:
            json.dump(res.json(), f, ensure_ascii=False, indent=4)
        # 解析器
        # 用字典的方式进行值的提取
        urllist = [f'https://read.zongheng.com/chapter/1296249/{i.get("chapterId")}。html' for i in
                   res.json().get('result').get('chapterList')[0].get('chapterViewList')]
        urlnamelist = [i.get('chapterName') for i in
                       res.json().get('result').get('chapterList')[0].get('chapterViewList')]
        # 存储器：用myaql数据库来进行存储
        yb.execute('create table if not exists 从县委书记到权力巅峰网址备份表格(章节标题 varchar(25), 章节网址 varchar(100))')
        for i in zip(urlnamelist, urllist):
            yb.execute(f'insert into 从县委书记到权力巅峰网址备份表格 values {i}')


    get_url_urlname()

except Exception as e:
    zonghenzhonwen.rollback()
    print(repr(e))
else:
    zonghenzhonwen.commit()
finally:
    yb.close()
    zonghenzhonwen.close()