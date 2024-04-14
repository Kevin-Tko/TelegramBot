import telebot
import CONFIG
from telebot.types import Message
from currencydata import search_currency, trade_check

# Creating the bot
bot = telebot.TeleBot(CONFIG.TOKEN, parse_mode=None)
print('bot started')


# defining a message handler which handles incoming /start and /help commands
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(chat_id=message.chat.id,
                     text='Greatings from Njogu 👋,\n\n'
                          'Welcome!! 🤝\n\n'
                          'We will get you an hourly update of exchange rates.\n\n'
                          'Type /exchange to get today\'s USD/KES, EUR/KES, GBP/KES & AUD/KES rates\n\n'
                          'Type /currency to get today\'s rate for any other currency in the world\n\n'
                          'Type /trading to get advice on whether to buy or sell a currency\n\n'
                          'Type /help for more help'
                     )


@bot.message_handler(commands=['help'])
def help_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton(text='Message Kevin for Help',
                                                    url='https://www.linkedin.com/in/kevin-njogu-aci-72565087/'))
    bot.send_message(message.chat.id,
                     'The available commands are /exchange,/currency,/trading,& /help.\n\n'
                     'If a command is not working, recheck and ensure you are typing correctly and in lowercase\n\n'
                     'if you have any other issue click on Message kevin for help and text me',
                     reply_markup=keyboard)


@bot.message_handler(commands=['exchange'])
def exchange_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(telebot.types.InlineKeyboardButton('USD', callback_data='get-USD'),
                 telebot.types.InlineKeyboardButton('EUR', callback_data='get-EUR'),
                 telebot.types.InlineKeyboardButton('GBP', callback_data='get-GBP'),
                 telebot.types.InlineKeyboardButton('AUD', callback_data='get-AUD'))
    bot.send_message(message.chat.id, 'Click on the Currency of choice:', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    data = query.data
    if data.startswith('get-'):
        get_ex_callback(query)


def get_ex_callback(query):
    bot.answer_callback_query(query.id)
    send_exchange_results(query.message, query.data[4:])


def send_exchange_results(message, curr_code):
    bot.send_chat_action(message.chat.id, 'typing')
    ex = search_currency(curr_code)
    bot.send_message(message.chat.id,
                     f'The exchange rate for {curr_code}/KES is: {ex}',
                     parse_mode='HTML')


@bot.message_handler(commands=['currency'])
def other_currency_command(message):
    bot.send_message(chat_id=message.chat.id, text='Enter another currency', parse_mode='HTML')
    bot.register_next_step_handler(message, process_currency_input)


def process_currency_input(message: Message):
    user_input = message.text
    result = search_currency(user_input.upper())
    bot.send_message(message.chat.id, result)


@bot.message_handler(commands=['trading'])
def other_currency_command(message):
    bot.send_message(chat_id=message.chat.id, text='Enter the currency you want to trade', parse_mode='HTML')
    bot.register_next_step_handler(message, process_trading)


def process_trading(message: Message):
    user_input = message.text
    result = trade_check(user_input.upper())
    bot.send_message(message.chat.id, result)


if __name__ == '__main__':
    bot.infinity_polling()
