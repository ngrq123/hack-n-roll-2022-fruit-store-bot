'''
A database storing the cart for each chat.
cart {
  chat_id: {
    item: quantity
  }
}
'''
cart = {}


'''
A database storing the available items in the store.
'''
fruits = {
  'Apple': {
    'description': 'An apple',
    'price': 1.50,
    'img': 'https://images.unsplash.com/photo-1619546813926-a78fa6372cd2?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80'
  },
  'Pear': {
    'description': 'A pear',
    'price': 1.00,
    'img': 'https://images.unsplash.com/photo-1615484477778-ca3b77940c25?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=735&q=80'
  },
  'Orange': {
    'description': 'An orange',
    'price': 2.50,
    'img': 'https://images.unsplash.com/photo-1603664454146-50b9bb1e7afa?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80'
  },
}
