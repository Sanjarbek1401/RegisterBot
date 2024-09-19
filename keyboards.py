from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# Inline keyboard with a "Greet" button
greet_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Greet", callback_data="greet")]
])

# Keyboard for phone number request
phone_number_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Share phone number", request_contact=True)]
], resize_keyboard=True)
