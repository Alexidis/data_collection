import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
import csv


class DataBasePipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.lerua_photo

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item


class LeruaPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(f'http:{img}')
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item


class CSVPipeline():
    def __init__(self):
        self.file = f'database.csv'
        with open(self.file, 'r', newline='') as csv_file:
            self.tmp_data = csv.DictReader(csv_file).fieldnames

        self.csv_file = open(self.file, 'a', newline='', encoding='UTF-8')

    def __del__(self):
        self.csv_file.close()

    def process_item(self, item, spider):
        columns = item.fields.keys()

        data = csv.DictWriter(self.csv_file, columns)
        if not self.tmp_data:
            data.writeheader()
            self.tmp_data = True
        data.writerow(item)
        return item