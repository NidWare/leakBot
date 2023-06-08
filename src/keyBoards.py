from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_welcome_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    search_button = InlineKeyboardButton("🔎 Search", callback_data='search')
    info_button = InlineKeyboardButton("🆘 Information", callback_data='info')
    keyboard.add(search_button, info_button)
    return keyboard


def get_search_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    phone_button = InlineKeyboardButton("📞Phone number", callback_data='phone')
    telegram_button = InlineKeyboardButton("👤Telegram", callback_data='telegram')
    instagram_button = InlineKeyboardButton("📷Instagram", callback_data='instagram')
    facebook_button = InlineKeyboardButton("🌐Facebook", callback_data='facebook')
    keyboard.add(phone_button, telegram_button, instagram_button, facebook_button)
    return keyboard


def get_buy_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    buy_button = InlineKeyboardButton("Buy 💳 | 590₹", callback_data='buy')
    unlimited_button = InlineKeyboardButton("Buy an unlimited service subscription  | 1190₹", callback_data='unlimited')
    keyboard.add(buy_button, unlimited_button)
    return keyboard


def get_check_payment_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    check_button = InlineKeyboardButton("Check Payment", callback_data='check_payment')
    cancel_button = InlineKeyboardButton("Cancel", callback_data='cancel')
    keyboard.add(check_button, cancel_button)
    return keyboard


def get_payment_keyboard(service_type):
    keyboard = InlineKeyboardMarkup(row_width=1)
    payment_button = InlineKeyboardButton("Payment", callback_data='payment_{}'.format(service_type))
    instructions_button = InlineKeyboardButton("Instructions", callback_data='instructions')
    keyboard.add(payment_button, instructions_button)
    return keyboard