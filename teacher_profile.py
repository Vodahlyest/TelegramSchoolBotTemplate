""" Парсер профилей учителей """

"""Импрот неоходимых Бибилиотек"""
import requests
from bs4 import BeautifulSoup

link = 'link'   """Указываем нужную ссылку с разделом сайта, откуда надо брать профили учителей"""
source_list = requests.get(link)                 
soup = BeautifulSoup(source_list.text, 'html.parser')      """Создается объект класса BeautifulSoup для парса необходимых нам даных"""
category_tags = soup.find_all('a', style="font-size: 18px; font-family: Monotype Corsiva; text-decoration: none;")    """Ищем все теги, в которых содержатся профили учителей"""
with open("name", 'w') as f:       """Открываем файл для хранения профилей преподователей для записи"""      
    for category in category_tags: """Перебор всех найденных Тегов и запись содержащейся в ней необходимой нам информации в файл для хранения
        text = category.get_text()
        f.writelines(text)
