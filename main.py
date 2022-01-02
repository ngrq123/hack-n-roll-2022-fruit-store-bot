import os

import telebot
from telebot.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice
from database import cart, fruits


# HackNRollFruitStoreBot
API_KEY = os.getenv('API_KEY') 
PAYMENT_KEY = os.getenv('PAYMENT_KEY') 
bot = telebot.TeleBot(API_KEY)

# bot.set_my_commands([])


def request_start(chat_id):
  """A helper function to request user to execute command /start"""
  if chat_id not in cart:
    bot.send_message(chat_id=chat_id, text='Please start the bot by sending /start')
  
  return


@bot.message_handler(commands=['parrot'])
def parrot(message):
  """The command that replies the user with the text message it recieves."""

  pass


@bot.message_handler(commands=['start'])
def start(message):
  """The command that welcomes the user and configures the required initial setup."""

  pass


@bot.message_handler(commands=['items'])
def items(message):
  """The commnad that lists all available items for sale."""

  chat_id = message.chat.id
  if chat_id not in cart: 
    request_start(chat_id)
    return

  pass


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
  """Handles the execution of the respective functions upon reciept of the callback query."""

  pass


def view_item_details(chat_id, data):
  """Displays the item details and an inline keyboard to add the item."""

  pass


def add_to_cart(chat_id, data):
  """Increments the item's quanity in the cart."""

  if chat_id not in cart: 
    request_start(chat_id)
    return

  pass


@bot.message_handler(commands=['cart'])
def view_cart(message):
  """The command that lists all items currently present in cart."""

  chat_id = message.chat.id
  if chat_id not in cart: 
    request_start(chat_id)
    return

  pass


@bot.message_handler(commands=['clear'])
def clear_cart(message):
  """The command that removes all previously add items in the cart."""

  chat_id = message.chat.id
  if chat_id not in cart: 
    request_start(chat_id)
    return

  pass


@bot.pre_checkout_query_handler(func=lambda query: True)
def pre_checkout(pre_checkout_query):
  """Handles the pre checkout payment process event."""

  pass


@bot.message_handler(commands=['checkout'])
def checkout_cart(message):
  """The command that creates an invoice based on the items added to cart."""

  chat_id = message.chat.id
  if chat_id not in cart: 
    request_start(chat_id)
    return
  
  pass


@bot.message_handler(content_types=['successful_payment'])
def payment_success(message):
  """Handles the event upon successful reciept of payments"""
  
  pass


bot.infinity_polling()
