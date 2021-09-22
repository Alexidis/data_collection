# 1. Написать программу, которая собирает входящие письма из своего или тестового почтового ящика,
# и сложить информацию о письмах в базу данных (от кого, дата отправки, тема письма, текст письма).

# 2. Написать программу, которая собирает «Хиты продаж» с сайтов техники М.видео, ОНЛАЙН ТРЕЙД и складывает данные в БД.
# Магазины можно выбрать свои. Главный критерий выбора: динамически загружаемые товары.

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin
from pymongo import MongoClient
from pathlib import Path

path_to_driver = Path('..') / 'operadriver_win32\operadriver.exe'

client = MongoClient('localhost', 27017)
data_collection_base = client.data_collection


def get_emails():
    e_letters = []
    
    driver.get('https://mail.ru/')
    # заполняем логин и домен
    login = driver.find_element_by_name('login')
    login.send_keys('07tnp01')
    Select(driver.find_element_by_name('domain')).select_by_value('@bk.ru')
    login.send_keys(Keys.ENTER)
    
    # заполняем пароль
    password = driver.find_element_by_name('password')
    driver.implicitly_wait(1)
    password.send_keys('0701')
    password.send_keys(Keys.ENTER)
    
    # получаем ссылки на письма
    letters_url = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class="dataset__items"]//a[contains(@class, "js-letter-list-item")]')))
    
    # преобразуем в статичный массив урлов
    urls = [urljoin(driver.current_url, l_url.get_attribute('href')) for l_url in letters_url]
    
    for url in urls:
        # переходим к письму
        driver.get(url)
        e_letter = {}
        # дождаться загрузки контента
        letter_content = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app-canvas"]')))

        # Парсим письмо
        e_letter['from'] = letter_content.find_element_by_xpath('//span[@class="letter-contact"]').get_attribute('title')
        e_letter['date'] = letter_content.find_element_by_xpath('//div[@class="letter__date"]').text
        e_letter['subject'] = letter_content.find_element_by_xpath('//h2[@class="thread__subject"]').text
        e_letter['body'] = letter_content.find_element_by_xpath('//div[@class="letter-body"]').text

        e_letters.append(e_letter)
        
        # вернуться назад
        driver.back()

    return e_letters


def insert_collections(docs, collection_name):
    collection = data_collection_base[collection_name]
    collection.insert_many(docs)


def task_1():
    emails_data = get_emails()
    insert_collections(emails_data, 'email')


def get_mvideo_hits():
    gadgets_hits = []
    driver.get('https://www.mvideo.ru/ger_tech')
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # получаем все товары
    gadgets_items = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.XPATH, '//div[@class="product-tile-info"]//a[contains(@class, "product-tile-title-link")]')))
    
    # преобразуем в статичный массив урлов
    urls = [urljoin(driver.current_url, l_url.get_attribute('href')) for l_url in gadgets_items]

    for url in urls:
        driver.get(url)
        gadget = {}

        gadget_content = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="main-holder"]')))
        
        # Парсим товар
        gadget['name'] = gadget_content.find_element_by_xpath('//h1[@class="fl-h1"]').text
        gadget['url'] = url
        gadget['price'] = gadget_content.find_element_by_xpath('//div[@class="fl-pdp-price"]').text

        # Название характеристик
        char_keys = gadget_content.find_elements_by_xpath('//span[@class="c-specification__name-text"]')
        # Значение характеристик
        char_vals = gadget_content.find_elements_by_xpath('//span[@class="c-specification__value"]')
        
        # Сводим список названий со списком значений что бы получить словарь характеристик
        gadget['characteristics'] = {char[0].text: char[1].text for char in zip(char_keys, char_vals)}

        gadgets_hits.append(gadget)
        driver.back()

    return gadgets_hits
   
    
def task_2():
    hits = get_mvideo_hits()
    insert_collections(hits, 'm_video')
    
    
if __name__ == '__main__':
    driver = webdriver.Chrome(path_to_driver)
    task_1()
    driver.close()
    
    driver = webdriver.Chrome(path_to_driver)
    task_2()
    driver.close()