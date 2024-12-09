import json
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage

# Считываем токен из config.json
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

TOKEN = config["token"]

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

# Обработчик команды /start
@dp.message(Command("start"))
async def start_command(message: Message):
    keyboard = create_genres_keyboard(series_data.keys())  # Создаём клавиатуру
    await message.answer("Привет! Выбери жанр из списка:", reply_markup=keyboard)

# Обработчик нажатий на кнопки
@dp.callback_query()
async def handle_genre_callback(callback: CallbackQuery):
    genre = callback.data.split("_")[1]
    if genre in series_data:
        # Формируем список ссылок с нумерацией и отступами
        links = "\n\n".join([f"{i + 1}. {link}" for i, link in enumerate(series_data[genre])])
        await callback.message.answer(f"Вот лучшие сайты с сериалами по жанру \"{genre}\":\n\n{links}")
    else:
        await callback.message.answer("Извините, я не нашёл сериалы по такому жанру.")
    
    # Отображаем клавиатуру с жанрами снова
    keyboard = create_genres_keyboard(series_data.keys())
    await callback.message.answer("Выбери следующий жанр:", reply_markup=keyboard)

    # Закрываем всплывающее сообщение
    await callback.answer()

# Основная функция для запуска бота
async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
