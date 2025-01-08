from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

from crud_functions import *

initiate_db()
products = get_all_products()

API_TOKEN = '8072626651:AAEmzENm9kkjQPlIThCfafpCksaTogrWrNw'

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text = 'Рассчитать')
button2 = KeyboardButton(text = 'Информация')
button3 = KeyboardButton(text = 'Купить')
kb.row(button1, button2)
kb.add(button3)

kb2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')],
        [InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')]
    ], resize_keyboard=True
)

kb3 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Продукт1', callback_data='product_buying')],
        [InlineKeyboardButton(text='Продукт2', callback_data='product_buying')],
        [InlineKeyboardButton(text='Продукт3', callback_data='product_buying')],
        [InlineKeyboardButton(text='Продукт4', callback_data='product_buying')]
    ], resize_keyboard=True
)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text='Купить')
async def get_buying_list(message):

    for pr in products:
        await message.answer(f"Название: {pr[1]} | "
                             f"Описание: Описание {pr[2]} | "
                             f"Цена: {pr[3]}")
        with open(f"турбо {pr[0]}.jpg", "rb") as img:
            await message.answer_photo(img)
    await message.answer("Выберите продукт для покупки:", reply_markup=kb3)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()

@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=inline_kb)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call: CallbackQuery):
    formula_text = """
    Формула Миффлина-Сан Жеора:

    Для мужчин: (10 × вес в кг) + (6.25 × рост в см) − (5 × возраст в годах) + 5
    Для женщин: (10 × вес в кг) + (6.25 × рост в см) − (5 × возраст в годах) − 161
    """
    await call.message.answer(formula_text)


@dp.callback_query_handler(text='calories')
async def set_age(call: types.CallbackQuery, state: FSMContext):
    await call.message.reply("Введите ваш возраст:")
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = int(message.text)

    await message.answer('Введите свой рост:')
    await UserState.next()


@dp.message_handler(state=UserState.growth)
async def set_growth(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['growth'] = float(message.text)

    await message.answer('Введите ваш вес:')
    await UserState.next()


@dp.message_handler(state=UserState.weight)
async def set_weight(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['weight'] = float(message.text)

    user_data = await state.get_data()
    age = user_data['age']
    growth = user_data['growth']
    weight = user_data['weight']

    bmr = 10 * weight + 6.25 * growth - 5 * age - 161
    tdee = bmr * 1.55

    await message.answer(f'Ваша норма калорий {int(tdee)} ')
    await state.finish()

@dp.message_handler(text=['/start'])
async def all_message(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью!", reply_markup = kb)

@dp.message_handler()
async def all_message(message):
    await message.answer("Введите команду /start, чтобы начать общение")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
