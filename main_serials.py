import json
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message
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

# Функция для создания клавиатуры с фильмами, включая кнопку возврата в меню
def create_movies_keyboard(movies):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=movie["title"], url=movie["link"])] for movie in movies
    ])
    # Добавляем кнопку "Вернуться в меню выбора" в новую строку
    keyboard.inline_keyboard.append(
        [InlineKeyboardButton(text="Вернуться в меню выбора", callback_data="back_to_menu")]
    )
    return keyboard

# Обработчик команды /start
@dp.message(Command("start"))
async def start_command(message: Message):
    keyboard = create_genres_keyboard(series_data.keys())  # Создаём клавиатуру с жанрами
    await message.answer("Привет! Выбери жанр из списка:", reply_markup=keyboard)

# Обработчик нажатий на кнопки
@dp.callback_query()
async def handle_genre_callback(callback: CallbackQuery):
    data = callback.data.split("_")
    if data[0] == "genre":
        genre = data[1]
        if genre in series_data:
            movies = series_data[genre][:10]  # Берём только 10 первых фильмов
            keyboard = create_movies_keyboard(movies)
            await callback.message.answer(f"Вот топ-10 фильмов по версии сайта 'Кинопоиск' в жанре \"{genre}\":", reply_markup=keyboard)
        else:
            await callback.message.answer("Извините, я не нашёл фильмы по этому жанру.")
    elif data[0] == "back":
        # Возвращаем пользователя в главное меню
        keyboard = create_genres_keyboard(series_data.keys())
        await callback.message.answer("Выберите жанр:", reply_markup=keyboard)
    await callback.answer()


# Основная функция для запуска бота
async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
