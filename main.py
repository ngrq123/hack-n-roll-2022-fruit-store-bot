import os

import telebot
from telebot.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice, ReplyKeyboardMarkup, KeyboardButton
from database import cart, fruits


# HackNRollFruitStoreBot
API_KEY = os.getenv('API_KEY') 
PAYMENT_KEY = os.getenv('PAYMENT_KEY') 
bot = telebot.TeleBot(API_KEY)

bot.set_my_commands([
  BotCommand('start', 'Starts the bot'),
  BotCommand('items', 'Lists all items available in store'),
  BotCommand('cart', 'Lists all items added in cart'),
  BotCommand('clear', 'Clears all items in the cart'),
  BotCommand('checkout', 'Request for payment')
])


@bot.message_handler(commands=['start'])
def start(message):
  chat_id = message.chat.id
  chat_user = message.chat.username
  message_text = f'Hi {chat_user}'
  
  cart[chat_id] = {}
  bot.reply_to(message, message_text)


@bot.message_handler(commands=['items'])
def items(message):
  chat_id = message.chat.id

  if chat_id not in cart:
    bot.send_message(chat_id=chat_id, text='/start')
    return

  chat_text='Select the item you would like view in detail'

  buttons = []
  for fruit_name in fruits:
    row = []
    button = InlineKeyboardButton(
      fruit_name, 
      callback_data='items detail ' + fruit_name
    )
    row.append(button)
    buttons.append(row)
  
  bot.send_message(
    chat_id=chat_id, 
    text=chat_text, 
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
  description = fruits[fruit_name]['description']
  price = fruits[fruit_name]['price']
  img_url = fruits[fruit_name]['img']
  
  caption = (f'Item: {fruit_name}\n'
            f'Description: {description}\n'
            f'Price: ${price}\n\n'
            'How many would you like to add to cart?')

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
  if chat_id not in cart:
    bot.send_message(chat_id=chat_id, text='/start')
    return

  quantity, fruit_name = data

  if fruit_name not in cart[chat_id].keys():
    cart[chat_id][fruit_name] = int(quantity)
  else:
    cart[chat_id][fruit_name] += int(quantity)
  
  bot.send_message(chat_id, f'Added {quantity} {fruit_name}')


@bot.message_handler(commands=['cart'])
def view_cart(message):
  chat_id = message.chat.id
  
  if chat_id not in cart:
    bot.send_message(chat_id=chat_id, text='/start')
    return

  cart_text = 'Cart:\n'

  if cart[chat_id]:
    for fruit, quantity in cart[chat_id].items():
      cart_text += f'- {quantity}x {fruit}\n'
  else:
    cart_text = 'Cart is empty!'
  
  bot.send_message(
    chat_id=chat_id,
    text=cart_text
  )


@bot.message_handler(commands=['clear'])
def clear_cart(message):
  chat_id = message.chat.id

  if chat_id not in cart:
    bot.send_message(chat_id=chat_id, text='/start')
    return

  cart_cleared_text = 'Cart has been cleared!'
  cart[chat_id].clear()

  bot.send_message(chat_id=chat_id, text=cart_cleared_text)


@bot.message_handler(commands=['checkout'])
def checkout_cart(message):
  chat_id = message.chat.id
  
  if chat_id not in cart:
    bot.send_message(chat_id=chat_id, text='/start')
    return
  
  cart_empty_text = 'Cart is empty, nothing to checkout!'
  if not cart[chat_id]:
    bot.send_message(
      chat_id=chat_id,
      text=cart_empty_text
    )
    return
  
  prices = []
  for fruit_name, quantity in cart[chat_id].items():
    item_price = fruits[fruit_name]['price']
    total_item_price_cents = quantity * item_price * 100
    prices.append(
      LabeledPrice(
        label=f'{quantity}x {fruit_name}', 
        amount=f'{total_item_price_cents:.0f}'
      )
    )

  title = 'Fruit Basket'
  description = '100% Organic. Fresh and sourced locally.'
  invoice_payload = 'invoice_payload'
  currency = 'SGD'
  bot.send_invoice(
    chat_id=chat_id,
    title=title,
    description=description,
    invoice_payload=invoice_payload,
    provider_token=PAYMENT_KEY,
    currency=currency,
    prices=prices
  )


@bot.pre_checkout_query_handler(func=lambda query: True)
def pre_checkout(pre_checkout_query):
  bot.answer_pre_checkout_query(
    pre_checkout_query.id, 
    ok=True,
    error_message='For testing, use the following payment credentials:\n\n'
                  'Card Number:  5555 5555 5555 4444\n'
                  'CVV: 123'
                  'MM/YY: 12/34\n'
                  'Cardholder Name: John'
                  'Country: Singapore'
                  'Zip Code: 123456'
  )


@bot.message_handler(content_types=['successful_payment'])
def recieved_payment(message):
  chat_id = message.chat.id
  total_payment = message.successful_payment.total_amount / 100
  currency = message.successful_payment.currency
  chat_success_text = f'Payment success! We have recieved your payment of {currency} {total_payment:.2f}'

  bot.send_message(chat_id=chat_id, text=chat_success_text)

bot.infinity_polling()
