import telebot
from config import keys, TOKEN
from extensions import Converter, APIException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(massage: telebot.types.Message):
    text = "Что бы начать работу с ботом введи команду следующим образом:\n\n<имя валюты> <в какую валюту перевести> <количество переводимой валюты>\"" \
           "\n\nУвидеть список всех доступных валют: /values" \
           "\n\nЧто бы ввести не целое число валюты, (например 1.5) используй < . > для корректной работы бота" \
           "\nЕсли бот не отвечает, значит либо сервер устал и отдыхает, либо боту не нравятся введенные данные. \n*Подумай над своим поведением*"
    bot.reply_to(massage, text)


@bot.message_handler(commands='values')
def values(massage:telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(massage, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Неверное количество параметров.')

        quote, base, amount = values

        quote_ticer, base_ticer = quote, base
        total_base = Converter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду \n{e}')
    else:
        total_pay = float(amount) * float(total_base)
        text = f'Цена {amount} {quote} в {base} - {total_pay}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
