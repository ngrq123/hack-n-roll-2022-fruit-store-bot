import os

import telebot
from telebot.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice
import database


# HackNRollFruitStoreBot
API_KEY = os.getenv('API_KEY') 
PAYMENT_KEY = os.getenv('PAYMENT_KEY') 
bot = telebot.TeleBot(API_KEY)

bot.set_my_commands([
  BotCommand('parrot', 'Sends back the same message'),
  BotCommand('items', 'Lists all items available in store'),
  BotCommand('cart', 'Lists all items added in cart'),
  BotCommand('clear', 'Clears all items in the cart'),
  BotCommand('checkout', 'Request for payment')
])

cart = {}


@bot.message_handler(commands=['parrot'])
def parrot(message):
  message_text = message.text
  print('Received message:', message_text)
  bot.reply_to(message, message_text)


@bot.message_handler(commands=['items'])
def items(message):
  print('Received items command')
  chat_id = message.chat.id

  buttons = []
  for fruit_name in database.fruits:
    row = []
    button = InlineKeyboardButton(
      fruit_name, 
      callback_data='items detail ' + fruit_name
    )
    row.append(button)
    buttons.append(row)
  
  bot.send_message(
    chat_id, 
    'Select the item you would like view in detail', 
    reply_markup=InlineKeyboardMarkup(buttons)
  )


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
  chat_id = call.message.chat.id
  data = call.data
  intent, data = data.split()[0], data.split()[1:]
  
  if intent == 'items':
    send_item_details(chat_id, data)
    return
  if intent == 'add':
    add_to_cart(chat_id, data)
    return

  bot.send_message(chat_id, 'Callback not implemented')


def send_item_details(chat_id, data):
  sub_intent, fruit_name = data
  img_url = database.fruits[fruit_name]['img']
  price = database.fruits[fruit_name]['price']
  caption = f'Item: {fruit_name}\nPrice: ${price}\n\nHow many would you like to add to cart?'

  buttons = []
  count = 0
  for i in range(1, 4):
    row = []
    for j in range(1, 4):
      count += 1
      quantity = str(count)
      button = InlineKeyboardButton(
        text=quantity,
        callback_data=f'add {quantity} {fruit_name}'
      )
      row.append(button)
      
    buttons.append(row)

  bot.send_photo(
    chat_id, 
    img_url, 
    caption=caption,
    reply_markup=InlineKeyboardMarkup(buttons)
  )


def add_to_cart(chat_id, data):
  quantity, fruit_name = data
  if fruit_name not in cart.keys():
    cart[fruit_name] = int(quantity)
  else:
    cart[fruit_name] += int(quantity)
  
  bot.send_message(chat_id, f'Added {quantity} {fruit_name}')


@bot.message_handler(commands=['cart'])
def view_cart(message):
  print('View cart')
  chat_id = message.chat.id
  cart_text = 'Cart:\n'

  if cart:
    for fruit, quantity in cart.items():
      cart_text += f'- {fruit}: {quantity}\n'
  else:
    cart_text = 'Cart is empty!'
  
  bot.send_message(
    chat_id=chat_id,
    text=cart_text
  )


@bot.message_handler(commands=['clear'])
def clear_cart(message):
  print('Clear cart')
  cart.clear()
  chat_id = message.chat.id
  cart_text = 'Cart has been cleared!'
  
  bot.send_message(
    chat_id=chat_id,
    text=cart_text
  )


@bot.message_handler(commands=['checkout'])
def checkout_cart(message):
  print('Checkout cart')
  chat_id = message.chat.id

  if not cart:
    bot.send_message(
      chat_id=chat_id,
      text='Cart is empty, nothing to checkout!'
    )
    return
  
  prices = []
  for fruit_name, quantity in cart.items():
    item_price = database.fruits[fruit_name]['price']
    total_item_price_cents = quantity * item_price * 100
    prices.append(
      LabeledPrice(
        label=f'{quantity}x {fruit_name}', 
        amount=f'{total_item_price_cents:.0f}'
      )
    )


  bot.send_invoice(
    chat_id=chat_id,
    title='Fruit Basket',
    description='100% Organic. Fresh and sourced locally.',
    invoice_payload='invoice_payload',
    provider_token=PAYMENT_KEY,
    currency='SGD',
    prices=prices
  )


bot.polling()
