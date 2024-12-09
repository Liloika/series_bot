import json
import random
import asyncio
import requests
from aiogram import Bot, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage


# Считываем токен и ключ из config.json
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

TOKEN = config["token"]
GIPHY_API_KEY = config["giphy_api_key"]

# Создаём бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Загрузка данных из JSON
with open("series_data.json", "r", encoding="utf-8") as f:
    series_data = json.load(f)

# Функция для создания клавиатуры с жанрами
def create_genres_keyboard(genres):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=genre, callback_data=f"genre_{genre}")] for genre in genres
    ])
    return keyboard


# Функция для поиска GIF (через GIPHY API)
def search_gif(query):
    url = f"https://api.giphy.com/v1/gifs/search?api_key={GIPHY_API_KEY}&q={query}&limit=10"
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json().get("data", [])
        if results:
            gif_url = random.choice(results)["images"]["original"]["url"]
            return gif_url
    return None


# Обработчик команды /start
@dp.message(Command("start"))
async def start_command(message: Message):
    keyboard = create_genres_keyboard(series_data.keys())  # Создаём клавиатуру
    await message.answer("Привет! Выбери жанр из списка:", reply_markup=keyboard)


# Обработчик сообщений
@dp.message()
async def handle_message(message: Message):
    user_text = message.text.lower()
    if user_text in ["сосал", "сосала", "сосал?", "сосала?"]:
        gif_url = search_gif("да")
        if gif_url:
            await bot.send_animation(message.chat.id, gif_url)
        else:
            await message.reply("Не удалось найти GIF, но я всё равно говорю 'да'!")
    else:
        await message.reply("Я пока не знаю, что ответить на это.")


# Основная функция для запуска бота
async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
