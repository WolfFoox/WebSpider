# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql


class DoubanPipeline:
    def open_spider(self, spider):
        # 进行数据库的连接：
        self.douban = pymysql.Connect(
            host='127.0.0.1',
            port=3306,
            user='admin',
            password='qwe123',
            database='douban',
            charset='utf8'
        )
        self.yb = self.douban.cursor()


    def process_item(self, item, spider):
        try:
            self.yb.execute(
                f'create table if not exists 电影排行榜每部电影详细信息表(电影名称 varchar(100), 电影网址 varchar(100),电影评分 varchar(10), 上映时间 varchar(200), 主演 varchar(300),电影类型 varchar(100), 电影简介 varchar(1000))')
            self.yb.execute(
                f'insert into 电影排行榜每部电影详细信息表 values ("{item["urlname"]}","{item["url"]}","{item["average"]}","{item["initialReleaseDate"]}","{item["starring"]}","{item["genre"]}","{item["summary"]}")')
        except Exception as e:
            self.douban.rollback()
            print(repr(e))
        else:
            self.douban.commit()
        return item
    def close_spider(self, spider):
        self.yb.close()
        self.douban.close()
