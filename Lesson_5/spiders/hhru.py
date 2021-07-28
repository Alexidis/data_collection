# -*- coding: utf-8 -*-
import scrapy
import requests
from lxml import html
from fake_headers import Headers


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = 'https://krasnodar.hh.ru/search/vacancy?clusters=true&enable_snippets=true&salary=&st=searchVacancy&text=python'

    def start_requests(self):
        # Получаем количество страниц
        header = Headers(headers=True).generate()
        response = requests.get(self.start_urls, headers=header)
        parsed = html.fromstring(response.text)
        pages_count = int(parsed.xpath('//*[@class="pager-item-not-in-short-range"]')[-1].xpath('./a/span')[0].text)

        for page in range(pages_count):
            url = self.start_urls + f'&page={page}'

            yield scrapy.Request(url, callback=self.parse_pages)

    def parse_pages(self, response):
        for href in response.css('div.vacancy-serp div.vacancy-serp-item div.vacancy-serp-item__row_header div.vacancy-serp-item__info span span span a.bloko-link::attr(href)').extract():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response, **kwargs):

        item = {
            'name': response.css('div.vacancy-title h1.bloko-header-1::text').extract_first(),
            'salary': response.css('div.vacancy-title p.vacancy-salary span.bloko-header-2_lite::text').extract(),
            'link': response.url,
            'source': 'https://hh.ru/'
        }
        yield item




