import random
import requests
import telebot
from bs4 import BeautifulSoup as bs

URL = 'https://www.anekdot.ru/last/good/'
TOKEN = '6109136967:AAFLFIcMe3QTfCL056sa40T5A7AFkZXgnC4'


def anekdot_parser(url):
    request = requests.get(url)
    soup = bs(request.text, 'html.parser')
    anekdots = soup.find_all('div', class_='text')

    return [c.text for c in anekdots]


list_jokes = anekdot_parser(URL)
random.shuffle(list_jokes)

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Чтобы посмеятся введите любое число от 1 до 9")


@bot.message_handler(content_types='text')
def joke(message):
    if message.text in '123456789':
        if list_jokes:
            bot.send_message(message.chat.id, list_jokes[0])
            del list_jokes[0]
        else:
            bot.send_message(message.chat.id, 'На сегодня все')


bot.polling()
