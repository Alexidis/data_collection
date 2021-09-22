BOT_NAME = 'Lesson_6'

SPIDER_MODULES = ['Lesson_6.spiders']
NEWSPIDER_MODULE = 'Lesson_6.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

ITEM_PIPELINES = {
   'Lesson_6.pipelines.DataBasePipeline': 1,
   'Lesson_6.pipelines.LeruaPhotosPipeline': 1,
}

FILES_STORE = r'downloaded'
DOWNLOAD_DELAY = 0

LOG_ENABLED = True
LOG_LEVEL = 'DEBUG'
