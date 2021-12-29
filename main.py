import json
import os

import telebot
from telebot.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup

import database

# HackNRollFruitStoreBot
API_KEY = os.getenv('API_KEY') 
bot = telebot.TeleBot(API_KEY)

bot.set_my_commands([
  BotCommand('parrot', 'Sends back the same message')
])

@bot.message_handler(commands=['parrot'])
def parrot(message):
  message_text = message.text
  print('Received message:', message_text)
  bot.reply_to(message, message_text)

@bot.message_handler(commands=['catalogue'])
def catalogue(message):
  print('Received catalogue command')
  chat_id = message.chat.id

  buttons = []
  for fruit_name in database.fruits:
    row = []
    button = InlineKeyboardButton(fruit_name, 
      callback_data='catalogue detail ' + fruit_name)
    row.append(button)
    buttons.append(row)
  
  bot.send_message(chat_id, 
    'Catalogue', 
    reply_markup=InlineKeyboardMarkup(buttons))

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
  chat_id = call.message.chat.id
  # Find callback data (e.g. 'catalogue Apple detail')
  data = call.data
  intent, data = data.split()[0], data.split()[1:]
  
  if intent == 'catalogue':
    send_fruit_details(chat_id, data)
    return

  bot.send_message(chat_id, 'Callback not implemented')

def send_fruit_details(chat_id, data):
  sub_intent, fruit_name = data
  bot.send_message(chat_id, 'You tapped on fruit: ' + fruit_name)

bot.polling()
