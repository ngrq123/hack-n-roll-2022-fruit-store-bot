# Hack&Roll 2022: Creating Telegram Bots

## Getting Started

### Replit

1. Create an account and login to Replit (repl.it)
2. Create a Python Repl 
3. Add the source code to the repl
    * On the left sidebar, click "Version Control"
    * Click "Existing Git Repository", then enter this repo's git link (https://github.com/ngrq123/hack-n-roll-2022-fruit-store-bot.git) 
4. Configure the repl 
    * Select language: Python
    * Configure the run button: `python main.py`
5. Install `pyTelegramBotAPI` 
    * On the left sidebar, click "Packages"
    * Search for `pyTelegramBotAPI` and click the "+" button to install the package
6. Setup new bot
    * Search **BotFather** on Telegram
    * Create a new bot using `/newbot` (take note of your bot's username)
    * Save the generated HTTP API key (this will be your `API_KEY`)
7. Setup payment provider
    * Generate a payment provider key using `/mybots`
    * Click "Payments" and select "Stripe"
    * Click "Connect Stripe Test" and you will be directed to Stripe's website
    * Click "Skip this form", then return back to BotFather on Telegram
    * Save the generated payment provider key (this will be your `PAYMENT_KEY`)
8. Add secrets (`API_KEY` and `PAYMENT_KEY`) on Replit
    * On the left sidebar, click "Secrets"
    * Add key `API_KEY` and enter the your `API_KEY` in the value textbox
    * Add key `PAYMENT_KEY` and enter the your `PAYMENT_KEY` in the value textbox
9. On Replit, locate the "Run" button and click it
10. On Telegram, search for your bot's username and interact with it

### Local Environment

1. Install Python and Git
2. Install pyTelegramBotAPI (using `pip`) `pip install -–upgrade pyTelegramBotAPI`
3. Clone the repository `git clone https://github.com/ngrq123/hack-n-roll-2022-fruit-store-bot.git`
4. Setup new bot
    * Search **BotFather** on Telegram
    * Create a new bot using `/newbot` (take note of your bot's username)
    * Save the generated HTTP API key (this will be your `API_KEY`)
5. Setup payment provider
    * Generate a payment provider key using `/mybots`
    * Click "Payments" and select "Stripe"
    * Click "Connect Stripe Test" and you will be directed to Stripe's website
    * Click "Skip this form", then return back to BotFather on Telegram
    * Save the generated payment provider key (this will be your `PAYMENT_KEY`)
6. Add secrets (`API_KEY` and `PAYMENT_KEY`) in `.env` file
```
API_KEY=your_API_KEY
PAYMENT_KEY=your_PAYMENT_KEY
```
7. On Telegram, search for your bot's username and interact with it

## Link to Workshop Recording
https://youtu.be/y3dCEEjM3sg
