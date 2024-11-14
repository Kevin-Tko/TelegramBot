import telebot
import CONFIG
from telebot.types import Message
from typing import Final
from telegram import Update
from  telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
# from currencydata import search_currency, trade_check

TOKEN: Final = '7902047681:AAFPXJbXun-_ALXxAhCMiXTwCAf9T607MP4'
BOT_USERNAME = '@thisawesomecurrency_bot'

import requests
from datetime import datetime, timedelta


URL = f"https://api.currencybeacon.com/v1/latest?api_key=1nko4HZnvIDkqQnnJSmxRJuoKUNaTNmE"

today = datetime.now()
yesterday = today - timedelta(days=1)
formatted_yesterday = yesterday.strftime('%Y-%m-%d')
past_url = f'https://api.currencybeacon.com/v1/historical?base=USD&date={formatted_yesterday}&api_key=1nko4HZnvIDkqQnnJSmxRJuoKUNaTNmE'


# COMMANDS
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello, Thanks for chatting.\n\n'
                                    'Type /help to learn how I work'
                                    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('I an FX rates bot and I use USD as the base currency.\n\n'
                                    'Please type /exchange to get today\'s rates for any currency'
                                    )

async def exchange_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text( 'I an FX rates bot and I use USD as the base currency.\n\n' )


# RESPONSES
def handle_response(text: str) -> str:
    ccy_key: str = text.upper().strip()
    response = requests.get(url=URL)
    if response.status_code == 200:
        output = response.json()['response']['rates']
        currencies = list(output.keys())
        if ccy_key in currencies:
            rate = output[ccy_key]
            return str(rate)
        else:
            return f'{ccy_key} is invalid!'
    else:
        return False



def trade_check(text: str) -> str:
    ccy: str = text.upper().strip()
    response = requests.get(url=past_url)
    if response.status_code == 200:
        output = response.json()['response'][1]['rates']
        currencies = list(output.keys())
        if ccy in currencies:
            past_rate = output[ccy]
            today_rate = int(handle_response(ccy))
            if today_rate > past_rate:
                return (f'Right now USD/{ccy} --> {today_rate}\n\n'
                        f'is higher than yesterday\'s rate --> {past_rate}.\n\n'
                        f' PLEASE SELL {ccy}')
            elif today_rate == past_rate:
                return (f'Right now USD/{ccy} --> {today_rate}\n\n'
                        f'is equal to yesterday\'s rate --> {past_rate}.\n\n'
                        f'Maybe it\'s a weekend or a holiday\n\n'
                        f' PLEASE HOLD{ccy}')
            else:
                return (f'Right now USD/{ccy} --> {today_rate}\n\n'
                        f'is lower than yesterday\'s rate {past_rate}.\n\n'
                        f' PLEASE BUY {ccy}')
        else:
            return False

    else:
        return False
    


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: {text}')


    response: str = handle_response(text)


    print('Bot:', response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update caused  error {context.error}')

async def clear_last_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Delete the latest message
    await context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)



if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('exchange', exchange_command ))

    # messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print('polling......')
    app.run_polling(poll_interval=1)



# ****************CODE FOR GROUP CHATS
    # if message_type == 'group':
    #     if BOT_USERNAME in text:
    #         new_text: str = text.replace(BOT_USERNAME, '').strip()

    #         if new_text.startswith('TREND') and '-' in new_text:
    #             try:
    #                 currency = new_text.split('-')[1].strip()
    #                 response: str = trade_check(currency)
    #             except IndexError:
    #                 response: str = "Please provide a currency code after 'TREND-'."
    #     else:
    #         return
    # else:
    #     if text.startswith('TREND'):
    #         use_curr: str = text.split('-')[1].strip()
    #         response: str =  trade_check(use_curr)
    #     else:
    #         response: str = handle_response(text)



# def search_currency(ccy):
#     response = requests.get(url=URL)
#     if response.status_code == 200:
#         output = response.json()['response']['rates']
#         currencies = list(output.keys())
#         if ccy in currencies:
#             rate = output[ccy]
#             return rate
#         else:
#             return f'{ccy} is invalid!'
#     else:
#         return False



# today = datetime.now()
# yesterday = today - timedelta(days=1)
# formatted_yesterday = yesterday.strftime('%Y-%m-%d')
# past_url = f'https://api.currencybeacon.com/v1/historical?base=USD&date={formatted_yesterday}&api_key=1nko4HZnvIDkqQnnJSmxRJuoKUNaTNmE'


# def trade_check(ccy):
#     response = requests.get(url=past_url)
#     if response.status_code == 200:
#         output = response.json()['response'][1]['rates']
#         currencies = list(output.keys())
#         if ccy in currencies:
#             past_rate = output[ccy]
#             today_rate = search_currency(ccy)
#             if today_rate > past_rate:
#                 return (f'Right now USD/{ccy} --> {today_rate}\n\n'
#                         f'is higher than yesterday\'s rate --> {past_rate}.\n\n'
#                         f' PLEASE SELL {ccy}')
#             elif today_rate == past_rate:
#                 return (f'Right now USD/{ccy} --> {today_rate}\n\n'
#                         f'is equal to yesterday\'s rate --> {past_rate}.\n\n'
#                         f'Maybe it\'s a weekend or a holiday\n\n'
#                         f' PLEASE HOLD{ccy}')
#             else:
#                 return (f'Right now USD/{ccy} --> {today_rate}\n\n'
#                         f'is lower than yesterday\'s rate {past_rate}.\n\n'
#                         f' PLEASE BUY {ccy}')
#         else:
#             return False

#     else:
#         return False



# Creating the bot
# bot = telebot.TeleBot(CONFIG.TOKEN, parse_mode=None)
# bot = telebot.TeleBot('7902047681:AAFPXJbXun-_ALXxAhCMiXTwCAf9T607MP4', parse_mode=None)
# print('bot started')


# defining a message handler which handles incoming /start and /help commands
# @bot.message_handler(commands=['start'])
# def send_welcome(message):
#     bot.send_message(chat_id=message.chat.id,
#                      text='Greatings from Njogu 👋,\n\n'
#                           'Welcome!! 🤝\n\n'
#                           'We will get you an hourly update of exchange rates.\n\n'
#                           'Type /exchange to get today\'s USD/KES, EUR/KES, GBP/KES & AUD/KES rates\n\n'
#                           'Type /othercurrency to get today\'s rate for any other currency in the world\n\n'
#                           'Type /trading to get advice on whether to buy or sell a currency\n\n'
#                           'Type /help for more help'
#                      )


# @bot.message_handler(commands=['help'])
# def help_command(message):
#     keyboard = telebot.types.InlineKeyboardMarkup()
#     keyboard.add(telebot.types.InlineKeyboardButton(text='Message Kevin for Help',
#                                                     url='https://www.linkedin.com/in/kevin-njogu-aci-72565087/'))
#     bot.send_message(message.chat.id,
#                      'The available commands are /exchange,/othercurrency/trading,& /help.\n\n'
#                      'If a command is not working, recheck and ensure you are typing correctly and in lowercase\n\n'
#                      'if you have any other issue click on Message kevin for help and text me',
#                      reply_markup=keyboard)


# @bot.message_handler(commands=['exchange'])
# def exchange_command(message):
#     keyboard = telebot.types.InlineKeyboardMarkup()
#     keyboard.row(telebot.types.InlineKeyboardButton('USD', callback_data='get-USD'),
#                  telebot.types.InlineKeyboardButton('EUR', callback_data='get-EUR'),
#                  telebot.types.InlineKeyboardButton('GBP', callback_data='get-GBP'),
#                  telebot.types.InlineKeyboardButton('AUD', callback_data='get-AUD'))
#     bot.send_message(message.chat.id, 'Click on the Currency of choice:', reply_markup=keyboard)


# @bot.callback_query_handler(func=lambda call: True)
# def iq_callback(query):
#     data = query.data
#     if data.startswith('get-'):
#         get_ex_callback(query)


# def get_ex_callback(query):
#     bot.answer_callback_query(query.id)
#     send_exchange_results(query.message, query.data[4:])


# def send_exchange_results(message, curr_code):
#     bot.send_chat_action(message.chat.id, 'typing')
#     ex = search_currency(curr_code)
#     bot.send_message(message.chat.id,
#                      f'The exchange rate for USD/{curr_code} is: {ex}',
#                      parse_mode='HTML')


# @bot.message_handler(commands=['othercurrency'])
# def other_currency_command(message):
#     bot.send_message(chat_id=message.chat.id, text='Enter another currency', parse_mode='HTML')
#     bot.register_next_step_handler(message, process_currency_input)


# def process_currency_input(message: Message):
#     user_input = message.text
#     result = search_currency(user_input.upper())
#     bot.send_message(message.chat.id, result)


# @bot.message_handler(commands=['trading'])
# def other_currency_command(message):
#     bot.send_message(chat_id=message.chat.id, text='Enter the currency you want to trade', parse_mode='HTML')
#     bot.register_next_step_handler(message, process_trading)


# def process_trading(message: Message):
#     user_input = message.text
#     result = trade_check(user_input.upper())
#     bot.send_message(message.chat.id, result)


# if __name__ == '__main__':
#     bot.infinity_polling()
