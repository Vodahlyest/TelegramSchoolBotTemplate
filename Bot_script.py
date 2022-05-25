# ипортируем нужные модули
from bs4 import BeautifulSoup
import requests
import telebot
from telebot import types

# создается бот (в конструкторе класса telebot.TeleBot указывается токен для связки с ботом. его можно получить у бота BotFather в телеграм)
bot = telebot.TeleBot("your_token")

secondary_signs = ['5', '6', '7', '8', '9'] # - Массивы для сортировки классов по парралелям: первый массив 5-9 парралель, второй 10-11.
high_signs = ['10', '11']

teacher_categories_dict = {         # - словарь хранящий профили учителей и ссылки с ним связанные в формате ключ-значение. Профили учителей парсятся при помощи программы парсера профилей, ссылки берутся с сайта школы
    'Учителя русского языка и литературы':'link_to_teachers_gallery',
    'Учителя математики и информатики':'link_to_teachers_gallery',
    'Учителя иностранного языка':'link_to_teachers_gallery',
    'Учителя естественно-научных предметов':'link_to_teachers_gallery',
    'Учителя истории и обществознания':'link_to_teachers_gallery',
    'Учителя физической культуры, технологии и ОБЖ':'link_to_teachers_gallery',
    'Учителя творческих дисциплин':'link_to_teachers_gallery'
}

def sort_button_signs(class_type, sorted_sign_list):              #функция для сортировки названий классов по парралелям
    with open("file_name") as f:
        text = f.read()
        for line in text.split(':'):     #каждый класс записан не через пробел, а через выбранный вами знак в файле для удобной работы с ними. в методе split() укажите соответствующий знак
            for clas in class_type:
                if clas in line:
                    sorted_sign_list.append(line)

signs_high = []          #назания классов с 10 по 11
signs_secondary = []     #названия классов с 5 по 9
sort_button_signs(secondary_signs, signs_secondary)
sort_button_signs(high_signs, signs_high)


def give_timetable(message, link):          #функция выдает расписание для класса. Передаваемые аргументы - название класса и ссылка на раздел сайта с расписанием для этого класса
    content = requests.get(link)            # для работы с ссылками URL используется модуль requests
    formatted_timetable = ''     #здесь будет отформатированное распсание для класса
    soup = BeautifulSoup(content.text, 'html.parser')    # объект класса BeautifulSoup для парсинга нужней нам информации с указанного раздела сайта. здесь - таблицы с расписанием.
    tables = soup.find_all('table', style="height: 780px; margin-right: 10px; border-collapse: collapse; font-family:Arial Narrow; font-size:14px;")   #парсим все таблицы для классво указанной паралелли (Необходимые теги и их аттрибуты указывайте при вызове метода в соответствии с сайтом вашей школы)
    for table in tables:         # перебор всех тегов с расписанием
        if message in table.text:            #если в таблице есть упоминание искомого класса:
            text_tags = table.find_all('tr')       #пролистываем все табличные тэги
            for text_tag in text_tags:
                if text_tag.text.startswith('td') == False:      #если текст внутри табличного тэга не пустышка ( шаблон, зависит от того как выполнена ваша таблица на сайте вашей школы, это условие не обязательно :) )
                    formatted_timetable += text_tag.text + '\n'   #добавляем и форматируем как надо в нужную переменную
    return formatted_timetable    #возвращаем отформаченное расписание

def give_all_teachers(message, markup):    """функция отвечает за предоставление списка учителей выбранного профиля"""
    global teacher_names              """сюда будут также сохранятся ФИО учителей выбранного профиля"""
    teacher_names = []
    contents = requests.get(teacher_categories_dict[message])  """обрабатываем ссылку на страницу со списком учителей выбранного профиля"""
    soup = BeautifulSoup(contents.text, 'html.parser')
    tags = soup.find_all('h2', style="font-size:20px;")     """теги для поиска в дальнейшем можно менять в зависимости от сайта школы. Дальнейший код - попытка преобразовать список учителей в читаемый вид ( меняется в зависимости от ваших нужд )"""
    for tag in tags:
        formatted_name = ''
        text = tag.text
        for i in range(len(text) - 1):
            count = 0
            if i != 0 and text[i].isupper() and text[i - 1] != ' ':
                formatted_name += (' ')
            formatted_name += text[i]
        if '.\r\n\t\t' in formatted_name:
            teacher_names.append(formatted_name.replace('.\r\n\t\t', '')) """Отформатированное имя заполняется в массив и в контейнер с кнопками"""
            button = types.KeyboardButton(formatted_name.replace('.\r\n\t\t', ''))
            markup.add(button)
    back_button_one_more = types.KeyboardButton('Назад')
    markup.add(back_button_one_more)

def give_teacher_info(name, link):       #функция отвечает за предоставление информации о выбранном преподователе. На вход подаются имя учителя, а также ссылка на страницу преподователей выбранного ранее профиля
    source = link     """ дальнейший код отвечает за получение ссылки на страницу выбранного преподователя, откуда мы будем собирать информацию о нем. Код меняется в зависимости от ваших нужд и требований"""
    teacher = name
    school_buildings = ['left', 'right']
    contents = requests.get(source)
    soup = BeautifulSoup(contents.text, 'html.parser')
    for building in school_buildings:
        divs = soup.find_all('div', align=building)
        for div in divs:
            second_name = teacher.split(' ')
            if second_name[0] in div.text:
                text = div.find_all('a')
                for text_tag in text:
                    bio_link = 'http://www.sch2001.ru' + text_tag.get('href')
                   
    full_bio = ''       """здесь сохраняется полная информация о преподоваетеле. Дальнейший код собирает информацию о преподователе, и в зависимости от ваших требований, код меняется."""
    bio_list = requests.get(bio_link)                
    bio_soup = BeautifulSoup(bio_list.text, 'html.parser')
    h1s = bio_soup.find_all('h1')
    div_tag = bio_soup.find('div', style="margin-left: 10;")

    for h1 in h1s:
        if name in h1.text:
            full_bio += h1.text + '\n'

    for line in div_tag:
        piece_of_bio = line.text
        if "Электронная" in piece_of_bio:
            full_bio += piece_of_bio.lstrip()

    return full_bio   """Возвращаем информацию о преподователе"""
    

main_markup = types.ReplyKeyboardMarkup(resize_keyboard = True)    #основное меню (главное)
timetable_btn = types.KeyboardButton('/timetable') # кнопка для получения расписания
teachers_button = types.KeyboardButton("/teacher_info") # кнопка для получения информации об учителях
main_markup.add(timetable_btn, teachers_button)

class_markup_main = types.ReplyKeyboardMarkup(resize_keyboard = True)    #выбор паралелли
secondary_grades = types.KeyboardButton('/5_9')        #выбор классов с 5 по 9
high_grades = types.KeyboardButton('/10_11')           #выбор классов с 10 по 11
back_button = types.KeyboardButton('Назад')
class_markup_main.add(high_grades, secondary_grades, back_button)

class_markup_secondary = types.ReplyKeyboardMarkup(resize_keyboard = True)    #выбор классов (5-9 парралель)
for button_name in signs_secondary:   #заполняем при помощи цикла меню выбора классов кнопками из массива с кнопками для 5-9 классов
    button = types.KeyboardButton(button_name)
    class_markup_secondary.add(button)
back_menu_button1 = types.KeyboardButton('Назад')
class_markup_secondary.add(back_menu_button1)

class_markup_high = types.ReplyKeyboardMarkup(resize_keyboard = True)         #выбор классов (10-11 паралелль)
for button_name in signs_high:
    button = types.KeyboardButton(button_name)
    class_markup_high.add(button)
back_menu_button2 = types.KeyboardButton('Назад')
class_markup_high.add(back_menu_button2)

teacher_markup = types.ReplyKeyboardMarkup(resize_keyboard = True)    """контейнер с кнопками выбора профиля преподователя"""
all_categories = list(teacher_categories_dict.keys())      
for category in all_categories:
    button = types.KeyboardButton(category)
    teacher_markup.add(button)
back_button_teacher = types.KeyboardButton('Назад')
teacher_markup.add(back_button_teacher)

@bot.message_handler(commands = ['start', 'help'])       #обрабатывает комманды start и help
def send_greets(messege):
    bot.send_message(messege.chat.id, "Привет, это бот-помощник школы 2001!", reply_markup = main_markup)

@bot.message_handler(commands = ['timetable'])
def timetable_menu(message):
    bot.send_message(message.chat.id, "Для какой паралелли найти расписание? ", reply_markup = class_markup_main)   """Обрабатывает команду timetable"""

@bot.message_handler(commands = ['10_11'])     """Команда 10_11 предоставляет пользоателю выбор класса с 10 по 11 парралель"""
def parallel_options_high(message):
    bot.send_message(message.chat.id, "Выбери нужный класс:", reply_markup = class_markup_high)

@bot.message_handler(commands = ['5_9'])       """Команда 5_9 предоставляет пользоателю выбор класса с 5 по 9 парралель"""
def parallel_options_secondary(message):
    bot.send_message(message.chat.id, "Выбери нужный класс:", reply_markup = class_markup_secondary)

@bot.message_handler(commands = ['teacher_info'])     """Команда teacher_info отвечает за предоставление пользователю выбор профиля преподователя"""
def teacher_categories(message):
    bot.send_message(message.chat.id, "Выбери профиль преподователя:", reply_markup = teacher_markup)

@bot.message_handler(content_types = ['text'])           #обрабатывает кнопки при помощи отправляемого ими текста
def getting_other_stuff(message):
    if message.text in signs_secondary:     """Если пользователь выбрал класс с 5 по 9 парралель:"""
        awnser = give_timetable(message.text, 'http://www.sch2001.ru/index.php?sid=1080')     """получаем расписания для данного класса и предоставляем его пользователю"""
        bot.send_message(message.chat.id, awnser)
    elif message.text in signs_high:        """Если пользователь выбрал класс с 10 по 11 парралель:"""
        awnser = give_timetable(message.text, link = 'http://www.sch2001.ru/index.php?sid=1378')   """получаем расписания для данного класса и предоставляем его пользователю"""
        bot.send_message(message.chat.id, awnser)
    elif message.text == 'Назад':
        bot.send_message(message.chat.id, "Что вы ходите сделать?", reply_markup = main_markup)
    elif message.text in teacher_categories_dict.keys():      """Если пользователь выбрал профиль преподователя:"""
        global current_link
        current_link = teacher_categories_dict[message.text]      """сохраняем ссылку на страницу выбранного профиля"""
        teachers_by_category = types.ReplyKeyboardMarkup(resize_keyboard = True)    """Здесь будут хранится кнопки выбора преподователей указанного ранее профиля"""
        give_all_teachers(message.text, teachers_by_category)     """получаем список преподователей указанного профиля и предоставляем его пользователю"""
        bot.send_message(message.chat.id, "Выберите преподователя из списка предложенных: ", reply_markup = teachers_by_category)
    elif message.text in teacher_names:    """Если пользователь выбрал преподователя из списка преподователей указанного им профиля:"""
        all_info = give_teacher_info(message.text, current_link)       """получаем информацию о преподователе и предоставляем его пользователю"""
        bot.send_message(message.chat.id, all_info)

bot.infinity_polling()   
