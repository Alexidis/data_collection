from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from Lesson_5 import settings
from Lesson_5.spiders.hhru import HhruSpider
from Lesson_5.spiders.superjobru import superjobSpider


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(HhruSpider)
    process.crawl(superjobSpider)
    process.start()
