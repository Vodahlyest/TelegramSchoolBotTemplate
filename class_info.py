"""  Парсер классов """

import requests       # импорт нужных бибилиотек
from bs4 import BeautifulSoup

links = ['link1', 'link2']  # массив с ссылками, откуда нужно парсить классы школы
clases = []      """ Здесь будут сохранены наши классы """
for link in links:   """ перебор ссылок из массива """
    source = requests.get(link)      
    soup = BeautifulSoup(source.text, 'html.parser')    """Создается объект класса BeautifulSoup для парсинга нужных разделов сайта"""
    main_table = soup.find_all('td', width="150px")     """Ищем все теги на нужном разделе сайта, где хранятся названия классов"""
    for tag in main_table:             """Перебираем теги"""
        class_name = tag.get_text()    """Получаем название класса"""
        print(class_name)
        clases.append(class_name)      """И заносим его в массив"""

with open("классы", 'w') as f:         """открываем файл для хранения классов школы и при помощи цикла записываем в него классы"""
    for class_name in clases:
        f.writelines(class_name + ":")
