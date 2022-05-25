# TelegramSchoolBotTemplate
Это готовый бот для мессенджера Телеграмм для дублирования информации об учебном процессе с сайта любой школы, такой как расписание для каждого класса по парралелям, контактные даты и информация о преподователе выбранного профиля и т.д.

Основная идея - Предоставить информацию с сайта школы в более интуитивно понятном виде, такм как чат бот в популярном Мессенджере. Цель достигнута при помощи использования языка python, библиотек telebot(работа с API telegram), requests и BeautifulSoup (для сбора информации с сайта школы). 

Все, что необходимо для работы бота - это сохранить при помощи программ парсеров (прилагаются к проекту) профили учителей и классы выбранных парралелей (изначально парсятся данные о классах с 5 по 9 парралель и с 10 по 11 парралель)в удобный вам формат файла (изначально используются текстовые файлы для хранения перечисленных данных). Затем эти данные, включая ссылки на разные разделы сайта выбранной школы можно подставлять в код и бот будет работать с сайтом вашей школы.



