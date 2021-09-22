from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from Lesson_6 import settings
from Lesson_6.spiders.leroymerlinru import LeruaSpider\


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeruaSpider, mark='Обои')
    process.start()
