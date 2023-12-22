import asyncio
import collections
import os
from datetime import datetime, time

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import state
from dotenv import load_dotenv
from aiogram.types import ReplyKeyboardMarkup, Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage  # Import MemoryStorage
from projectFiles.booking import Booking
from projectFiles.booking_details import BookingDetails
from projectFiles.booking_system import BookingSystem
from projectFiles.random_booking_strategy import RandomBookingStrategy
from projectFiles.choose_place_strategy import ChoosePlaceStrategy
from projectFiles.booking_data_access import BookingDataAccess
from projectFiles.choose_number_strategy import ChooseNumberStrategy
from projectFiles.concrete_observer import ConcreteObserver
from projectFiles.file_booking_data_access import FileBookingDataAccess
from aiogram.types import BotCommand

load_dotenv()
bot = Bot(token='6188044140:AAH0oh7hG2HYnJo5ibPWc9v2JJX9rmM-70M')
dp = Dispatcher(bot=bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add('📚 Book a Place').add('📍 My Booked Place').add('🌐 View Available Places')
keyboard = InlineKeyboardMarkup(row_width=2)
keyboard.add(InlineKeyboardButton(text='🎲 Book Randomly', callback_data='random'),
             InlineKeyboardButton(text='🔢 Book by Number', callback_data='number'),
             InlineKeyboardButton(text='📋 Book by Requirements', callback_data='requirements'))
IaIaZhokZhok = InlineKeyboardMarkup(row_width=2)
IaIaZhokZhok.add(InlineKeyboardButton(text='Yes', callback_data='YESYES'),
                 InlineKeyboardButton(text='No', callback_data='NONO'))

user_states = collections.defaultdict(int)
reply = closed = False


class UserState:
    def __init__(self):
        self.booked_seats = 0


class BookingForm(StatesGroup):
    booking_random = State()
    booking_requirements = State()
    booking_number = State()
    cancel_booking = State()
    do_notify = State()
    undo_notify = State()


bks = BookingSystem()

chat_id = ''


def check_time_and_do_something():
    global closed
    current_time = datetime.now().time()

    if current_time.hour == 8 and current_time.minute == 0:
        closed = False
        temp = "📚 Library is open! 📚"
        bks.notify_observers(temp)
        return [True, temp]

    elif current_time.hour<8 or current_time.hour > 18 and current_time.minute == 0:
        closed = True
        temp = "📚 Library is closed! 🚪"
        bks.notify_observers(temp)
        return [False, temp]
    else:
        return [True, '']

@dp.message_handler(commands=['start'])
async def cmd_start(message: Message):
    global closed, reply
    user_states[message.from_user.id] = len(FileBookingDataAccess().find_from_txt(str(message.from_user.id)))
    client = ConcreteObserver(str(message.from_user.id))
    if message.from_user.id not in bks.observers:
        bks.add_observer(client)
    res = check_time_and_do_something()

    if res[0]:
        closed = False
        if res[1] and not reply:
            await message.answer(res[1])
        await message.answer(
            "🌅 The Sunrise Bot! \nReserve your spot effortlessly and immerse yourself in the world of books! \n#TheSunriseBot",
            reply_markup=main)
        reply = True
    elif not res[0]:
        await message.answer(res[1])
        closed = True


@dp.message_handler(text='📚 Book a Place')
async def book_place(message: Message):
    if not closed:
        if user_states[message.from_user.id] < 3:
            await message.answer("How you want to book place? 📚🌟", reply_markup=keyboard)
        else:
            await message.answer("You have already booked the maximum number of seats")
    else:
        await message.answer("📚 Library is closed! 🚪")


def number_to_emoji(num):
    emoji_numbers = {
        0: "0️⃣", 1: "1️⃣", 2: "2️⃣", 3: "3️⃣", 4: "4️⃣",
        5: "5️⃣", 6: "6️⃣", 7: "7️⃣", 8: "8️⃣", 9: "9️⃣"
    }

    emoji_str = ""
    for digit in str(num):
        emoji_str += emoji_numbers.get(int(digit), digit)

    return emoji_str


def yes_no_to_emoji(value):
    emoji_values = {"Yes": "✅", "No": "❌"}
    return emoji_values.get(value, value)


@dp.message_handler(text='📍 My Booked Place')
async def my_list(message: Message):
    if not closed:
        username = str(message.from_user.id)
        s = BookingSystem().my_bookings(username)

        if s == "You have no bookings":
            await message.answer("Your list is currently empty. 📜✨")
        else:
            temp = ''
            for i in s:
                lst = i.split()
                place_number = lst[0]
                if lst[2] == "True":
                    socket_val = "Yes"
                else:
                    socket_val = "No"
                if lst[3] == "True":
                    wide_val = "Yes"
                else:
                    wide_val = "No"
                start_time = lst[4]
                end_time = lst[5]
                if int(place_number) > 9:
                    temp += f"Place: {number_to_emoji(place_number)}, Socket: {yes_no_to_emoji(socket_val)}, Wide: {yes_no_to_emoji(wide_val)},\n⏰ Start time: {start_time}, End time: {end_time}\n"
                else:
                    temp += f"Place:      {number_to_emoji(place_number)}, Socket: {yes_no_to_emoji(socket_val)}, Wide: {yes_no_to_emoji(wide_val)},\n⏰ Start time: {start_time}, End time: {end_time}\n"
            await message.answer(
                f"Your list:\n\n{temp}\n\nIf you want to cancel your reservation, write the place number 🗑️")
            await BookingForm.cancel_booking.set()
    else:
        await message.answer("📚 Library is closed! 🚪")


@dp.message_handler(text='🌐 View Available Places')
async def available_places(message: Message):
    if not closed:
        system = BookingSystem()
        s = ""
        for i in system.place_available():
            lst = i.split()
            if lst[1] == 'available':
                if lst[2] == "True":
                    socket_val = "Yes"
                else:
                    socket_val = "No"
                if lst[3] == "True":
                    wide_val = "Yes"
                else:
                    wide_val = "No"
                if int(lst[0]) > 9:
                    s += f"Place: {number_to_emoji(lst[0])}, Socket: {yes_no_to_emoji(socket_val)}, Wide: {yes_no_to_emoji(wide_val)}\n"
                else:
                    s += f"Place:      {number_to_emoji(lst[0])}, Socket: {yes_no_to_emoji(socket_val)}, Wide: {yes_no_to_emoji(wide_val)}\n"
        await message.answer(f"Here is the list:\n\n{s}")
    else:
        await message.answer("📚 Library is closed! 🚪")


@dp.message_handler(state=BookingForm.booking_number)
async def number_booking(message: Message, state: FSMContext):
    try:
        bookingg = Booking(ChooseNumberStrategy())
        system = BookingSystem()
        system.set_booking(bookingg)
        place_number, start_time, end_time = map(str.strip, message.text.split(','))
        if not (place_number or start_time or end_time):
            await options(message, state)
            await state.finish()

        # if int(end_time.split(':')[0]) > 18 or int(end_time.split(':')[0]) - int(start_time.split(':')[0]) > 3:
        #     await message.answer("Write the correct time")
        #     await BookingForm.booking_number.set()
        #     return

        username = str(message.from_user.id)
        details = BookingDetails(place_number, username, start_time, end_time)

        user_id = message.from_user.id
        text = "This place is occupied by someone"
        result = system.make_booking(details)
        if user_states[user_id] < 3:
            if text != result:
                user_states[user_id] += 1
            await message.answer(result)
        else:
            await message.answer("You have already booked the maximum number of seats")
        await state.finish()
    except:
        await state.finish()
        await options(message, state)


@dp.message_handler(state=BookingForm.booking_requirements)
async def requirements_booking(message: Message, state: FSMContext):
    try:
        bookingg = Booking(ChoosePlaceStrategy())
        system = BookingSystem()
        system.set_booking(bookingg)
        id, sockett, wide, start_time, end_time = map(str.strip, message.text.split(','))
        if not (id or sockett or wide or start_time or end_time):
            await options(message, state)
            await state.finish()

        # if int(end_time.split(':')[0]) > 18 or int(end_time.split(':')[0]) - int(start_time.split(':')[0]) > 3:
        #     await message.answer("Write the correct time")
        #     await BookingForm.booking_requirements.set()
        #     return

        if sockett == 'Yes':
            sockett = 'True'
        else:
            sockett = 'False'
        if wide == 'Yes':
            wide = 'True'
        else:
            wide = 'False'
        details = BookingDetails(id, message.from_user.id, sockett, wide, start_time, end_time)
        user_id = message.from_user.id
        text = "This place is occupied by someone"
        result = system.make_booking(details)

        if user_states[user_id] < 3:
            if text != result:
                user_states[user_id] += 1
            await message.answer(result)
        else:
            await message.answer("You have already booked the maximum number of seats")
        await state.finish()
    except:
        await state.finish()
        await options(message, state)


@dp.message_handler(state=BookingForm.booking_random)
async def random_booking(message: Message, state: FSMContext):
    try:
        bookingg = Booking(RandomBookingStrategy())
        system = BookingSystem()
        system.set_booking(bookingg)
        start_time, end_time = map(str.strip, message.text.split(','))
        if not (start_time or end_time):
            await state.finish()
            await options(message, state)
        username = str(message.from_user.id)
        details = BookingDetails(username, start_time, end_time)
        user_id = message.from_user.id
        result = system.make_booking(details)
        text = "This place is occupied by someone"
        if user_states[user_id] < 3:
            if text != result:
                user_states[user_id] += 1
            await message.answer(result)
        else:
            await message.answer("You have already booked the maximum number of seats")
        await state.finish()
    except:
        await state.finish()
        await options(message, state)


@dp.message_handler(state=BookingForm.cancel_booking)
async def cancel_booking(message: Message, state: FSMContext):
    if not message.text or len(message.text.split()) > 1:
        await options(message, state)
        await state.finish()
    else:
        try:
            id = str(message.text.strip())
            text = BookingSystem().cancel_booking(BookingDetails(id, str(message.from_user.id)))
            if text == "Deleted successfully":
                user_states[message.from_user.id] -= 1
            await message.answer(text)
            await state.finish()
        except:
            await state.finish()


@dp.callback_query_handler(text='random')
async def handle_random(callback_query: types.CallbackQuery):
    if not closed:
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text="Write the details in the following format:\n\n🕒 Start time, End time (max 18:00)\n")
        await BookingForm.booking_random.set()
    else:
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text="📚 Library is closed! 🚪")


@dp.callback_query_handler(text='number')
async def handle_number(callback_query: types.CallbackQuery):
    if not closed:
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text="Write the details in the following format:\n\n🔢 Number (1-30), Start time, End time (max 18:00)\n\nExample:\n30, 15:00, 18:00")
        await BookingForm.booking_number.set()
    else:
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text="📚 Library is closed! 🚪")


@dp.callback_query_handler(text='requirements')
async def handle_requirements(callback_query: types.CallbackQuery):
    if not closed:
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text="Write the details in the following format:\n\n📋 Number (1-30), Socket (Yes/No), Wide table (Yes/No), Start time, End time (max 18:00)\n\nExample:\n30, Yes, No, 15:00, 18:00")
        await BookingForm.booking_requirements.set()
    else:
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text="📚 Library is closed! 🚪")


async def options(message: Message, state: FSMContext):
    if message.text == '🎲 Book Randomly':
        await book_place(message)
    elif message.text == '🔢 Book by Number':
        await my_list(message)
    elif message.text == '📋 Book by Requirements':
        await available_places(message)
    elif message.text == '📚 Book a Place':
        await book_place(message)
    elif message.text == '📍 My Booked Place':
        await my_list(message)
    elif message.text == '🌐 View Available Places':
        await available_places(message)
    else:
        await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
