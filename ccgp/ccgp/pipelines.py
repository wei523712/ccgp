# -*- coding: utf-8 -*-
import pymysql
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class CcgpPipeline(object):
    def open_spider(self,spider):
        self.conn = pymysql.Connect(host='127.0.0.1',port=3306,user='root',password='123456',db='ccgp',charset='utf8')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        sql = "INSERT INTO shixin(company,social_code,address,detail,result,punishment_basis,punish_date,publication_date,enforcement) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (item['company'],item['social_code'],item['address'],item['detail'],item['result'],item['punishment_basis'],item['punish_date'],item['publication_date'],item['enforcement'])

        try:
            self.cursor.execute(sql)
            # 提交
            self.conn.commit()
            # print(self.cursor.fetchall())
        except Exception as e:
            print(e)
            self.conn.rollback()
        return item

    def close_spider(self,spider):
        self.cursor.close()
        self.conn.close()