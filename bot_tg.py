import logging
import random
import google.generativeai as genai
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Токены (замени на свои)
TELEGRAM_BOT_TOKEN = "7449130360:AAFQbDb-lD_W9vwGysj4STdUpc1ADj719ro"
GEMINI_API_KEY = "AIzaSyDZ8n5GAU1SIFVhi8n4nAZHazUtJK6rK6A,"

genai.configure(api_key=GEMINI_API_KEY)
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# Состояния для FSM
class GreetingState(StatesGroup):
    waiting_for_name = State()

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Стили поздравлений
GREETING_STYLES = ["Классика", "Шутливое", "Официальное", "Рэп", "Романтика"]

# Главная клавиатура
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🚀 Начать")],
        [KeyboardButton(text="🎁 Получить приз")],
        [KeyboardButton(text="💰 Забери 100000$")]
    ],
    resize_keyboard=True
)

# Список случайных призов
PRIZES = [
    ("🏆 Поздравляем! Вы выиграли 1 000 000$!", "https://www.youtube.com/watch?v=dQw4w9WgXcQ"),
    ("🎟 Вам достался билет в кино!", "https://www.youtube.com/watch?v=dQw4w9WgXcQ"),
    ("🚗 Вы выиграли новый автомобиль!", "https://www.youtube.com/watch?v=dQw4w9WgXcQ"),
    ("💎 Поздравляем! Вы нашли клад с бриллиантами!", "https://www.youtube.com/watch?v=dQw4w9WgXcQ")
]

async def generate_greeting(name):
    style = random.choice(GREETING_STYLES)
    prompt = f"Создай {style.lower()} поздравление с 8 марта для {name}:"
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        logging.error(f"Ошибка при запросе к Gemini AI: {e}")
        return "Извините, произошла ошибка при генерации поздравления. Попробуйте еще раз позже."

@dp.message(Command("start"))
async def start_command(message: types.Message):
    photo_url = "https://memi.klev.club/uploads/posts/2024-04/memi-klev-club-k6el-p-memi-kot-s-rozoi-1.jpg"
    await message.answer_photo(photo_url, caption="Привет! Нажми '🚀 Начать' для создания поздравления.", reply_markup=main_keyboard)
    logging.info(f"{message.from_user.id} нажал /start")

@dp.message(F.text == "🚀 Начать")
async def ask_name(message: types.Message, state: FSMContext):
    logging.info(f"{message.from_user.id} выбрал 'Начать'")
    await state.set_state(GreetingState.waiting_for_name)
    await message.answer("Кого будем поздравлять? Введи имя:")

@dp.message(GreetingState.waiting_for_name)
async def get_greeting(message: types.Message, state: FSMContext):
    name = message.text
    await message.answer(f"Генерируем поздравление для {name}...")
    await state.clear()
    logging.info(f"{message.from_user.id} ввел имя: {name}")
    greeting = await generate_greeting(name)
    await message.answer(greeting)

@dp.message(F.text == "🎁 Получить приз")
async def get_prize(message: types.Message):
    logging.info(f"{message.from_user.id} выбрал 'Получить приз'")
    prize_text, prize_link = random.choice(PRIZES)
    button = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔗 Забрать приз", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")]])
    await message.answer(prize_text, reply_markup=button)

@dp.message(F.text == "💰 Забери 100000$")
async def claim_money(message: types.Message):
    logging.info(f"{message.from_user.id} выбрал 'Забери 100000$'")
    button = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Нажми на меня", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")]])
    await message.answer("Поздравляем! Ты можешь забрать свой выигрыш! 😆", reply_markup=button)

@dp.message()
async def log_user_messages(message: types.Message):
    logging.info(f"Сообщение от {message.from_user.id}: {message.text}")

async def main():
    logging.info("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
