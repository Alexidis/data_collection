# -*- coding: utf-8 -*-
import scrapy
import requests
from lxml import html
from fake_headers import Headers


class superjobSpider(scrapy.Spider):
    name = 'superjobru'
    allowed_domains = ['superjob.ru']
    start_urls = 'https://krasnodar.superjob.ru/vakansii/menedzher.html'

    def start_requests(self):
        # Получаем количество страниц
        header = Headers(headers=True).generate()
        response = requests.get(self.start_urls, headers=header)
        parsed = html.fromstring(response.text)
        pages_count = int(parsed.xpath('//*[@class="_3hkiy _30F5F _290uh _1tqyb _3PbQP _1AKho"]')[-2].xpath('./span/span')[0].text)

        for page in range(pages_count):
            url = self.start_urls + f'?page={page}'

            yield scrapy.Request(url, callback=self.parse_pages)

    def parse_pages(self, response):
        for href in response.css('div._1h3Zg._2rfUm._2hCDz._21a7u a::attr(href)').extract():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response, **kwargs):

        item = {
            'name': response.css('h1._1h3Zg.rFbjy._2dazi._2hCDz::text').extract_first(),
            'salary': response.css('span._1h3Zg._2Wp8I._2rfUm._2hCDz::text').extract(),
            'link': response.url,
            'source': 'https://superjob.ru/'
        }
        yield item