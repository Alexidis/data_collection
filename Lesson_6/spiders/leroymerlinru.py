from urllib.parse import urljoin
import scrapy
from scrapy.http import HtmlResponse
from ..items import LeruaItem


class LeruaSpider(scrapy.Spider):
    name = 'Lerua'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, mark):
        self.start_urls = [f'https://leroymerlin.ru/search/?q={mark}']

    def parse(self, response: HtmlResponse):
        ads_links = response.xpath('//a[@class="bex6mjh_plp b1f5t594_plp iypgduq_plp nf842wf_plp"]/@href').extract()
        for link in ads_links:
            link = urljoin(response.url, link)
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        name = response.css ('h1.header-2::text').extract_first()

        photos = response.xpath('//div[contains(@class, "container detailed-view-inner container--fronton")]//uc-pdp-media-carousel//img/@src').extract()
        # Название характеристик
        char_keys = response.xpath('//section[@class="pdp-section pdp-section--product-characteristicks"]//div[@class="def-list__group"]//dt//text()').extract()
        # Значение характеристик
        char_vals = response.xpath('//section[@class="pdp-section pdp-section--product-characteristicks"]//div[@class="def-list__group"]//dd//text()').extract()

        # Сводим список названий со списком значений что бы получить словарь характеристик
        characteristics = {char[0]: char[1].replace('\n', '').strip() for char in zip(char_keys, char_vals)}

        yield LeruaItem(name=name, photos=photos, characteristics=characteristics)
