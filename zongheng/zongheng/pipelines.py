# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql


class ZonghengPipeline:
    def open_spider(self, spider):
        # 进行数据库的连接：
        self.zongheng = pymysql.Connect(
            host='127.0.0.1',
            port=3306,
            user='admin',
            password='qwe123',
            database='zongheng',
            charset='utf8'
        )
        self.yb = self.zongheng.cursor()

    def process_item(self, item, spider):
        try:
            self.yb.execute(
                f'create table if not exists 从县委书记到权力巅峰_章节内容表(章节名称 varchar(100), 章节字数 varchar(6),正文内容 varchar(9000))')
            self.yb.execute(
                f'insert into 从县委书记到权力巅峰_章节内容表 values ("{item["chapter_name"]}","{item["chapter_count"]}","{item["chapter_content"]}")')
        except Exception as e:
            self.zongheng.rollback()
            print(repr(e))
        else:
            self.zongheng.commit()
        return item

    def close_spider(self, spider):
        self.yb.close()
        self.zongheng.close()
