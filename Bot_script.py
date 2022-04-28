# ипортируем нужные модули
from bs4 import BeautifulSoup
import requests
import telebot
from telebot import types

# создается бот и контейнер для кнопок действий
bot = telebot.TeleBot("5014044061:AAF952gfILnsysnH4Nqm0O8HTX-VfIzn-Qs")

secondary_signs = ['5', '6', '7', '8', '9']
high_signs = ['10', '11']

teacher_categories_dict = {
    'Учителя русского языка и литературы':'http://www.sch2001.ru/index.php?sid=1045',
    'Учителя математики и информатики':'http://www.sch2001.ru/index.php?sid=1046',
    'Учителя иностранного языка':'http://www.sch2001.ru/index.php?sid=1058',
    'Учителя естественно-научных предметов':'http://www.sch2001.ru/index.php?sid=1059',
    'Учителя истории и обществознания':'http://www.sch2001.ru/index.php?sid=1060',
    'Учителя физической культуры, технологии и ОБЖ':'http://www.sch2001.ru/index.php?sid=1063',
    'Учителя творческих дисциплин':'http://www.sch2001.ru/index.php?sid=1062'
}

def sort_button_signs(class_type, sorted_sign_list):              #функция для сортировки названий классов по парралелям
    with open("классы") as f:
        text = f.read()
        for line in text.split(':'):
            for clas in class_type:
                if clas in line:
                    sorted_sign_list.append(line)

signs_high = []          #назания классов с 10 по 11
signs_secondary = []     #названия классов с 5 по 9
sort_button_signs(secondary_signs, signs_secondary)
sort_button_signs(high_signs, signs_high)


def give_timetable(message, link):          #функция выдает расписание для класса. Передаваемые аргументы - название класса и ссылка на раздел сайта с расписанием для этого класса
    content = requests.get(link)
    formatted_timetable = ''     #здесь будет отформатированное распсание для класса
    soup = BeautifulSoup(content.text, 'html.parser')
    tables = soup.find_all('table', style="height: 780px; margin-right: 10px; border-collapse: collapse; font-family:Arial Narrow; font-size:14px;")   #парсим все таблицы для классво указанной паралелли
    for table in tables:
        if message in table.text:            #если в таблице есть упоминание искомого класса:
            text_tags = table.find_all('tr')       #пролистываем все табличные тэги
            for text_tag in text_tags:
                if text_tag.text.startswith('td') == False:      #если текст внутри табличного тэга не пустышка ( шаблон ):
                    formatted_timetable += text_tag.text + '\n'   #добавляем и форматируем как надо в нужную переменную
    return formatted_timetable    #возвращаем отформаченное расписание

def give_all_teachers(message, markup):
    contents = requests.get(teacher_categories_dict[message])
    soup = BeautifulSoup(contents.text, 'html.parser')
    tags = soup.find_all('h2', style="font-size:20px;")
    for tag in tags:
        formatted_name = ''
        text = tag.text
        for i in range(len(text) - 1):
            count = 0
            if text[i].isupper() and text[i - 1] != ' ':
                formatted_name += (' ')
            formatted_name += text[i]
        button = types.KeyboardButton(formatted_name)
        markup.add(button)
    back_button_one_more = types.KeyboardButton('Назад')
    markup.add(back_button_one_more)

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

teacher_markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
all_categories = list(teacher_categories_dict.keys())
for category in all_categories:
    button = types.KeyboardButton(category)
    teacher_markup.add(button)
back_button_teacher = types.KeyboardButton('Назад')
teacher_markup.add(back_button_teacher)

teachers_by_category = types.ReplyKeyboardMarkup(resize_keyboard = True)

@bot.message_handler(commands = ['start', 'help'])       #обрабатывает комманды start и help
def send_greets(messege):
    bot.send_message(messege.chat.id, "Привет, это бот-помощник школы 2001!", reply_markup = main_markup)

@bot.message_handler(commands = ['timetable'])
def timetable_menu(message):
    bot.send_message(message.chat.id, "Для какой паралелли найти расписание? ", reply_markup = class_markup_main)

@bot.message_handler(commands = ['10_11'])
def parallel_options_high(message):
    bot.send_message(message.chat.id, "Выбери нужный класс:", reply_markup = class_markup_high)

@bot.message_handler(commands = ['5_9'])
def parallel_options_secondary(message):
    bot.send_message(message.chat.id, "Выбери нужный класс:", reply_markup = class_markup_secondary)

@bot.message_handler(commands = ['teacher_info'])
def teacher_categories(message):
    bot.send_message(message.chat.id, "Выбери профиль преподователя:", reply_markup = teacher_markup)

@bot.message_handler(content_types = ['text'])           #обрабатывает кнопки при помощи отправляемого ими текста
def ask_grade(message):
    if message.text in signs_secondary:
        awnser = give_timetable(message.text, 'https://sch2001.ru/index.php?sid=1080')
        bot.send_message(message.chat.id, awnser)
    elif message.text in signs_high:
        awnser = give_timetable(message.text, link = 'https://sch2001.ru/index.php?sid=1378')
        bot.send_message(message.chat.id, awnser)
    elif message.text == 'Назад':
        bot.send_message(message.chat.id, "Что вы ходите сделать?", reply_markup = main_markup)
    elif message.text in teacher_categories_dict.keys():
        give_all_teachers(message.text, teachers_by_category)
        bot.send_message(message.chat.id, "Выберите преподователя из списка предложенных: ", reply_markup = teachers_by_category)


bot.infinity_polling()
