import requests
from bs4 import BeautifulSoup
links = ['https://sch2001.ru/index.php?sid=1080', 'https://sch2001.ru/index.php?sid=1378']
clases = []
for link in links:
    source = requests.get(link)
    soup = BeautifulSoup(source.text, 'html.parser')
    main_table = soup.find_all('td', width="150px")
    for tag in main_table:
        class_name = tag.get_text()
        print(class_name)
        clases.append(class_name)

with open("классы", 'w') as f:
    for class_name in clases:
        f.writelines(class_name + ":")
