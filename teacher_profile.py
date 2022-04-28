import requests
from bs4 import BeautifulSoup

link = 'https://sch2001.ru/index.php?sid=1045'
source_list = requests.get(link)
soup = BeautifulSoup(source_list.text, 'html.parser')
a_all = soup.find_all('a', style="font-size: 18px; font-family: Monotype Corsiva; text-decoration: none;")
print(a_all)
with open("категории учителей", 'w') as f:
    all_categories = ''
    for a in a_all:
        text = a.get_text()
        f.writelines(text)
