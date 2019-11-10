# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

"""
import sys
import os

base_path = os.path.abspath(os.path.dirname(__file__))
for i in range(3):
    base_path = os.path.dirname(base_path)
sys.path.append(base_path)
"""

from dal import RedisAccessor

class StockCrawlerPipeline(object):

    da_class = RedisAccessor

    """
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        try:
            self.client = pymongo.MongoClient(self.mongo_uri)
            self.db = self.client[self.mongo_db]
        except Exception as e:
            spider.logger.error(e)

    def close_spider(self, spider):
        self.client.close()
    """

    def open_spider(self, spider):
        try:
            self._da = self.da_class(logger=spider.logger)
        except Exception as e:
            spider.logger.error(e)
            spider.close()

    def close_spider(self, spider):
        self._da.close()

    def process_item(self, item, spider):
        # item = {
        #   'stockid': '000001',
        #   'typecode': 'bizinco',
        #   'values': {
        #       '20190630': '201222.02',
        #       '20190930': ''
        #   }
        # }
        stockid = item.get("stockid")
        typecode = item.get('typecode')
        spider.logger.info(f'StockCrawlerPipeline process item: '
                            f'stockid={stockid}, '
                            f'typecode={typecode}, '
                            f'values={item.get("values")}')
        rt = self._da.handle_mset(stockid, item.get('values'), typecode)
        if rt:
            self._da.add_to_crawl_processed_set(stockid, typecode)
        return item