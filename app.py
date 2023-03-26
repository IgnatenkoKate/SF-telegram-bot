"""ConvertValue"""
"""@ConvertValuesBotBot"""

import telebot
from config import keys, TOKEN
from extensions import APIException, Converter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start_help(message: telebot.types.Message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! Чтобы начать работу введите команду боту в следующем формате: \n<имя валюты цену которой хотите узнать> \
<в какую валюту перевести> \
<количество переводимой валюты> \n Увидеть список всех доступных валют: /values')


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        value = message.text.split(' ')

        if len(value) != 3:
            raise APIException('Слишком много или слишком мало параметров. Введите три параметра.')

        quote, base, amount = value
        total_base = Converter.get_price(quote.lower(), base.lower(), amount)

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n Не знаю валюту {amount}. Нажми /help')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}. Нажми /help')

    else:
        text = f'Цена {abs(int(amount))} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

@bot.message_handler()
def info(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! \
Чтобы начать работу, введите команду боту в следующем формате: \n <имя валюты цену которой хотите узнать> \
<в какую валюту перевести> <количество переводимой валюты> '
f'\n Увидеть список всех доступных валют: /values')
    else:
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! Я бот для конвертации валют. \n'
                                          f'Чтобы начать работу введите команду боту в следующем формате: \
                                          <имя валюты цену которой хотите узнать> <в какую валюту перевести> \
                                          <количество переводимой валюты> \n Увидеть список всех доступных валют: /values')


bot.infinity_polling()