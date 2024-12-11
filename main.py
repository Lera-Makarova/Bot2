import asyncio
import sqlite3
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from keyboards import get_main_menu
from person import person_router as profile_router

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        district TEXT,
        gender TEXT,
        age INTEGER
    )
    """)
    conn.commit()
    conn.close()

@dp.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username or ""

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT OR IGNORE INTO users (user_id, username, district, gender, age) 
    VALUES (?, ?, ?, ?, ?)
    """, (user_id, username, None, None, None))
    conn.commit()
    conn.close()

    photo = FSInputFile("images/pup2.jpg")
    caption = "Профилю нужно дописать красивые слова"
    await message.answer_photo(photo=photo, caption=caption, reply_markup=get_main_menu())

async def main():
    init_db()
    dp.include_router(profile_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
