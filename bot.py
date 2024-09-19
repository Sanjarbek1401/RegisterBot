import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from keyboards import phone_number_kb, greet_kb
from database import create_table, save_user_info

API_TOKEN = '7351526845:AAGFOFQsnrl96bLTkUmjUdfgI8XEuukEobw'

# Initialize bot and dispatcher with memory storage for FSM
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()  # Memory storage for FSM
dp = Dispatcher(storage=storage)


# Define the states
class UserData(StatesGroup):
    first_name = State()
    last_name = State()
    phone_number = State()


# Start command handler
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Hello guys!", reply_markup=greet_kb)


# Inline button callback to greet user and request first name
@dp.callback_query(lambda c: c.data == "greet")
async def greet_user(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Please enter your first name:")
    await bot.answer_callback_query(callback_query.id)
    await state.set_state(UserData.first_name)  # Set the FSM state to first_name


# First name handler
@dp.message(UserData.first_name)
async def first_name_handler(message: Message, state: FSMContext):
    first_name = message.text
    await state.update_data(first_name=first_name)  # Save first name in FSM context
    await message.answer("Great! Now, enter your last name:")
    await state.set_state(UserData.last_name)  # Move to the next state


# Last name handler
@dp.message(UserData.last_name)
async def last_name_handler(message: Message, state: FSMContext):
    last_name = message.text
    await state.update_data(last_name=last_name)  # Save last name in FSM context
    await message.answer("Now, please share your phone number.", reply_markup=phone_number_kb)
    await state.set_state(UserData.phone_number)  # Move to the next state


# Phone number handler
@dp.message(UserData.phone_number, lambda message: message.contact)
async def phone_number_handler(message: Message, state: FSMContext):
    phone_number = message.contact.phone_number
    user_id = message.from_user.id

    # Retrieve first name and last name from the FSM context
    user_data = await state.get_data()
    first_name = user_data.get("first_name")
    last_name = user_data.get("last_name")

    # Save the information in the database
    await save_user_info(user_id, first_name, last_name, phone_number)
    await message.answer("Your information has been saved. Thank you!")

    # Finish the FSM state
    await state.clear()


# Main function to run the bot
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await create_table()  # Ensure table exists before starting the bot
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
