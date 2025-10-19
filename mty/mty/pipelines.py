# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class MtyPipeline:
    # 写出默认的open_spider函数出来进行自定义存储器的创建，这个函数会在启动项目时自动调用一次
    def open_spider(self, spider):
        # 写出文件的创建或打开代码：
        self.f = open(r'云南酒店名称和评论总数统计.txt', 'w+', encoding='utf-8')

    def process_item(self, item, spider):
        url_namelist = item['url_namelist']
        total_list = item['total_list']
        locationIdlist = item['locationIdlist']
        datalist = [f'{x}(评论id为{z})==> {y}\n' for x, y, z in zip(url_namelist, total_list, locationIdlist)]
        self.f.writelines(datalist)
        return item

    # 写出默认的close_spider函数出来进行自定义存储器的关闭
    def close_spider(self, spider):
        self.f.close()
