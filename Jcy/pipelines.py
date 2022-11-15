# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import codecs
import json

from itemadapter import ItemAdapter
from xlwt import Workbook
import openpyxl
from openpyxl.styles import Font
wb = openpyxl.Workbook()
sheet = wb.active

class JcyPipeline:
    def __init__(self):
        self.file=codecs.open(filename='Jcy.xml',mode='w+',encoding='utf-8')
    def open_spider(self, spider):  # 在启动一个spider的时候自动运行
        pass

    def close_spider(self, spider):  # 在关闭一个spider的时候自动运行
        self.file.close()


"""
# 这个方法的声明不能动!!! 在spider返回的数据会自动的调用这里的process_item方法. 
    # 你把它改了. 管道就断了
"""


def process_item(self, item, spider):
    res=dict(item)
    str=json.dumps(res,ensure_ascii=False)
    self.file.write(str)
    self.file.write(',\n')
    if spider.name == 'ssq':
        self.f.write(f"{item['url'].strip()},{','.join(item['date'])},{item['title']}\n")
    return item



