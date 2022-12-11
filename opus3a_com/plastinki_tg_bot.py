# Первое, что нужно сделать это импортировать нашу библиотеку и подключить токен бота:

import telebot
import db
import re


# создаем экземпляр класса TeleBot
bot = telebot.TeleBot('5714906467:AAGQWZiaCNSrIHYn8pPRVeyrozPoNKBK1rU')

# Теперь добавим метод для обработки команды start:
@bot.message_handler(commands=['start'])
def start_message(message):
	bot.send_message(message.chat.id,'Привет! Здесь ты можешь купить виниловые пластинки и CD-диски с доставкой. \nНаши цены ниже озона на 50%\n\n/artist - поиск по артисту\n/album - поиск по названию альбома')



# метод для обработки команды /new
@bot.message_handler(commands=['artist'])
def artist_message(message):
	bot.send_message(message.chat.id,'Напиши имя артиста или название группы для поиска')

@bot.message_handler(content_types=['text'])
def search_artist(message):
	for item in db.search_in_db(message.text):

		bot.send_photo(message.chat.id, item[2], "{} - {}\n{}\n{} руб\n\nЗаказать: @arotos".format(item[0], item[1],item[4],5*int(re.sub('\.00.*', '',item[7]))))





bot.polling(none_stop=True, interval=1)