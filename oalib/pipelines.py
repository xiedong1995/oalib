# -*- coding: utf-8 -*-

import pymongo
import pymysql
import logging
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.files import FilesPipeline


logger = logging.getLogger(__name__)


class OalibPipeline(object):
    def process_item(self, item, spider):
        return item

class MongoDBPipeline():
    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db= crawler.settings.get('MONGO_DB')
        )

    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self,item,spider):
        self.db[item.collection].insert(dict(item))
        return item


    def close_spidr(self,spider):
        self.client.close()

class MysqlPipeline():
    def __init__(self,host,user,password,database,port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port


    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            user=crawler.settings.get("MYSQL_USER"),
            password=crawler.settings.get("MYSQL_PASSWORD"),
            port=crawler.settings.get("MYSQL_PORT"),
        )

    def open_spider(self,spider):
        self.db = pymysql.connect(self.host,self.user,self.password,self.database,self.port,charset='utf8')
        self.cursor = self.db.cursor()


    def close_spider(self,spider):
        self.db.close()

    def process_item(self,item,spider):
        data = dict(item)
        keys = ','.join(data.keys())
        values = ','.join(['%s']*len(data))
        sql = 'insert into %s (%s) values (%s)'%(item.table,keys,values)
        self.cursor.execute(sql,tuple(data.values()))
        self.db.commit()
        return item


class DownloadFilePipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None):
        url = request.url
        file_name = url.re_first('(\d+)')+'.pdf'
        return file_name

    def item_completed(self, results, item, info):
        file_path = [x['path'] for ok,x in results if ok]
        if not file_path:
            raise DropItem('File Downloaded Filed')
        return item

    def get_media_requests(self, item, info):
        yield Request(item['full_link'])





